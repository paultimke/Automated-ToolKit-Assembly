from logging import exception
from typing import Tuple
import enum

#import pywhatkit as wpp
import main
import pandas as pd
import Vision as vs
import csv

import time
from PLC_sim import plc_dummy
import plc_comm

import Global_vars as glob
from Global_vars import KITS_DB_CSV_PATH

import smtplib, ssl
from email.message import EmailMessage
import win32com.client as win32
from datetime import datetime

OUT_OF_STOCK_ITEMS = []

class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class Vision_Result(enum.Enum):
    waiting = 0
    Kit_OK = 1
    Kit_FAIL = 2


def create_RefSizesList() -> list:
    """ Create Reference Sizes List function.
    Creates a list containing the reference sizes of each kind of screw by reading
    the CSV file with this information

    Returns a list of tuples containing length and width information of each screw
    """
    df = pd.read_csv(KITS_DB_CSV_PATH)    # Read csv file with screw types and sizes

    ref_list = []
    for i in range(len(df.index)):
        # Column 1 is for length, Column 2 is for width
        ref_list.append((df.iloc[i][1], df.iloc[i][2]))

    return ref_list

def create_Kit(UI_kit: list) -> dict:
    """ Create Kit function.
    Creates a kit with the correct format needed for classification. Needs to be called from
    within the UI

    @UI_kit : User selected kit from the UI. Used to extract the item count for each screw
    
    @Kit return -> Kit in appropiate format for classification
                   (Dictionary containing the item count for each screw type)
    """
    df = pd.read_csv(KITS_DB_CSV_PATH)    # Read csv file with screw types and sizes
    n_IDs = len(df.index)
    strings = []
    Kit = {}

    # Extract ID tag names of each screw
    for i in range(n_IDs):
        strings.append(df.iloc[i][0])
    # Extract item count from selected kit
    for i in range(n_IDs):
        # Third item of the list is another list containing the item counts as strings
        Kit[strings[i]] = int(UI_kit[2][i])
    
    return (Kit)


def is_inRange(val: tuple, ref: tuple, precision: float) -> bool:
    maxA = ref[0] + (ref[0] * precision)
    minA = ref[0] - (ref[0] * precision)
    maxB = ref[1] + (ref[1] * precision)
    minB = ref[1] - (ref[1] * precision)
    
    exp1 = ((val[0]>minA and val[0]<maxA) and (val[1]>minB and val[1]<maxB))
    exp2 = ((val[0]>minB and val[0]<maxB) and (val[1]>minA and val[1]<maxA))

    return (exp1 or exp2)


def classify(obj_sizes: list, ref_sizes: list, perimeters: list) -> Tuple[list, list]:
    df = pd.read_csv(KITS_DB_CSV_PATH) # DataFrame with the reference sizes of screws
    n_screws = len(obj_sizes) # Number of objects detected
    n_types = len(df.index)   # Number of different types of screws
    objects = []              # List to store the classification of each object
    hist = {}                 # Dictionary to store the histogram
    IDs = []                  # String List of ID tags

    # Populate histogram
    for i in range(n_types):
        IDs.append(df.iloc[i][0])
    for i in range(n_types):
        hist[IDs[i]] = 0

    # Classify each object and make a histogram of each type
    for screw in range(n_screws):
        for id in range(n_types):
            if is_inRange(obj_sizes[screw], ref_sizes[id], 0.39):
                if IDs[id] == 'mediano' or IDs[id] == 'tuerca':
                    if perimeters[screw] < 149 :
                        objects.append((screw, 'tuerca'))
                        hist['tuerca'] += 1
                        break
                    else :
                        objects.append((screw, 'mediano'))
                        hist['mediano'] += 1
                        break
                else: 
                    objects.append((screw, IDs[id]))
                    hist[IDs[id]] += 1
                    break

    return (objects, hist)


def send_alert_email(kit_type:str, kit_num:int):
    kit_num = str(kit_num)
    receivers : list = glob.EMAIL_RECEIVERS
    
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = receivers[0]
    mail.CC=receivers[1]
    message = 'La estación de armado de kits del ModulaLift ha elaborado ' + kit_num + ' veces el kit ' + kit_type + '\n'
    mail.Subject = 'Kit'  + kit_type + 'Terminado'
    mail.Body = message
    #mail.HTMLBody = '<h2>HTML Message body</h2>' #this field is optional

    # To attach a file to the email (optional):
    #attachment  = "Path to the attachment"
    #mail.Attachments.Add(attachment)
    try:  
        #wpp.sendwhatmsg_instantly(glob.PHONE_NUM,message, 10, True, 5)
        mail.Send()
    except:
        print("Error: No se envio correo")           
#END OF FUNCTION send_alert_email()

def send_Out_of_Stock_email():
    KitID = ''
    
    for items in OUT_OF_STOCK_ITEMS:
        KitID += items + ', '
    KitID = KitID[:-2]

    receivers : list = glob.EMAIL_RECEIVERS
    
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = receivers[0]
    mail.CC=receivers[1]
    message = 'La(s) pieza(s)  ' + KitID + ' se ha(n) agotado en el sistema de almacenaje ModulaLift. \n Favor de actualizar el inventario disponible lo antes posible\n'
    mail.Subject = 'Piezas fuera de stock en almacén ModulaLift '
    mail.Body = message
    #mail.HTMLBody = '<h2>HTML Message body</h2>' #this field is optional

    # To attach a file to the email (optional):
    #attachment  = "Path to the attachment"
    #mail.Attachments.Add(attachment)
    try: 
        #wpp.sendwhatmsg_instantly(glob.PHONE_NUM,message, 10, True, 5)
        mail.Send()
    except:
        print("Error: No se envio correo")

#END OF FUNCTION send_Out_of_Stock_email()


def compare_kits(cmp: dict, ref: dict, img: vs.Mat, kit_type:str, kit_num:int):
    plc = connect_to_plc()

    if cmp == ref:
        print(f"{bcolors.OKGREEN}Kit OK{bcolors.ENDC}")
        vs.save_image(img, "Test", "Images/Passed_Kits")
        plc.write_Vision_Result(Vision_Result.Kit_OK.value)
        update_stock(ref)
        #send_alert_email(kit_type, kit_num)

        return True
    else:
        print(f"{bcolors.FAIL}Kit FAILED {bcolors.ENDC}")
        vs.save_image(img, "Test", "Images/Rejected_Kits")

        (screw_id, tray_id) = find_missing_screw(cmp, ref)

        if(screw_id == None):
            print("Problemas con Vision. Checar iluminacion")
        else:
            plc.write_Screw_ID(screw_id)
            plc.write_Screw_Bandeja(tray_id)

        plc.write_Vision_Result(Vision_Result.Kit_FAIL.value)
        time.sleep(0.5)
        plc.write_Vision_Result(Vision_Result.waiting.value)

        return False
#END OF FUNCTION compare_kits()

def find_missing_screw(cmp: dict, ref: dict) -> Tuple[int, int]:
    SCREW_ID_CSV_COL = 5
    TRAY_ID_CSV_COL  = 4

    df = pd.read_csv(KITS_DB_CSV_PATH)
    missing : int = None
    Screw_ID: int = None
    Tray_ID:  int = None

    for key in ref:
        if(cmp[key] < ref[key]):
            missing = key # Only returns the last missing

    for row in range(len(df.index)):
        if(df.iloc[row][0]) == missing:
            Screw_ID = df.iloc[row][SCREW_ID_CSV_COL]
            Tray_ID = df.iloc[row][TRAY_ID_CSV_COL]

    return (Screw_ID, Tray_ID)
#END OF FUNCTION find_missing_screw()

def update_stock(ref_kit: dict):
    in_stock: bool = True

    #'camilo: +526142184709'

    # List of screws used, to take them off the stock
    subtracts = []
    for key in ref_kit:
        subtracts.append(ref_kit[key])

    # Save the entire file in the 2d list rows
    with open(KITS_DB_CSV_PATH, 'r', newline="") as f:
        rows = [] # Entire csv
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            rows.append(row)

    # When opened, the file is erased, but we have its 
    # contents saved in rows, so we modify those and 
    # write back rows into the file
    with open(KITS_DB_CSV_PATH, 'w', newline="") as f:
        writer = csv.writer(f)
        screw_index = 0
        for row in rows:
            if row[3] != 'Stock':
                row[3] = str(int(row[3]) - subtracts[screw_index])
                if int(row[3]) <= 0:
                    row[3] = '0'
                    in_stock = False
                    OUT_OF_STOCK_ITEMS.append(row[0])
                screw_index += 1
                
        writer.writerows(rows)
    if not in_stock:
        #send_Out_of_Stock_email()
        #raise Exception(f"{bcolors.FAIL}OUT OF STOCK{bcolors.ENDC}")
        pass
#END OF FUNCTION update_stock()

def connect_to_plc():
    # Hardware Setup
    if main.USING_PLC_DUMMY:
        plc = plc_dummy.PLC(10)
    else:
        from Global_vars import (PLC_IP_ADDRESS, PLC_RACK, PLC_RACK_SLOT, 
                                PLC_DATABLOCK, PLC_DB_SIZE)

        plc = plc_comm.PLC(PLC_IP_ADDRESS, PLC_RACK, PLC_RACK_SLOT, 
                                PLC_DATABLOCK, PLC_DB_SIZE)

    return plc
#END OF FUNCTION connect_to_plc()

def prevention_Out_of_Stock(ref_kit:dict):
    df = pd.read_csv(KITS_DB_CSV_PATH)
    crt_Stock = []

    for i in range (len(df.index)):
        crt_Stock.append(df.iloc[i][3])

    f : int = 0
    for v in ref_kit.values():
        if v > crt_Stock[f]:
            raise Exception(f"{bcolors.FAIL}OUT OF STOCK{bcolors.ENDC}")
        f += 1 


def prevention_No_Capacity(ref_kit:dict):
    num_of_screws : int = 0
    for v in ref_kit.values():
        num_of_screws += v
    if num_of_screws > 14:
        raise Exception(f"{bcolors.FAIL}TRAY OUT OF SPACE{bcolors.ENDC}")




