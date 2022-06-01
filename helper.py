from typing import Tuple
import pandas as pd
import Vision as vs

from Global_vars import KITS_DB_CSV_PATH

import smtplib, ssl
from email.mime.text import MIMEText


class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def create_RefSizesList() -> list:
    """ Create Reference Sizes List function.
    Creates a list containing the reference sizes of each kind of screw by reading
    the CSV file with this information

    Returns a list of tuples containing length and width information of each screw
    """
    df = pd.read_csv(KITS_DB_CSV_PATH)    # Read csv file with screw types and sizes

    ref_list = []
    for i in range(len(df.index)):
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


def classify(obj_sizes: list, ref_sizes: list) -> Tuple[list, list]:
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
            if is_inRange(obj_sizes[screw], ref_sizes[id], 0.25):
                objects.append((screw, IDs[id]))
                hist[IDs[id]] += 1

    return (objects, hist)

#------------------
def send_alert_email(kit_type:str, kit_num:int):
    kit_num = str(kit_num)
    email_pass : str = 'Robocop22'
    sender : str = 'modula.vision@gmail.com'
    receivers : list = ['A01566664@tec.mx','christianloyapena@hotmail.com']
    port : int = 587
    
    context = ssl.create_default_context()

    with smtplib.SMTP("smtp.gmail.com", port) as smtp:
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.ehlo()

        smtp.login(sender, email_pass)

        subject = 'Kit ' + kit_type + ' Terminado'
        body = 'La estacion de armado de kits del ModulaLift ha elaborado ' + kit_num + ' veces el kit ' + kit_type

        message = f'subject: {subject}\n\n{body}'
        #message = """ felicidades """
        smtp.sendmail(sender, receivers, message)
#--------------------


def compare_kits(cmp: list, ref: list, img: vs.Mat, kit_type:str, kit_num:int):
    if cmp == ref:
        print(f"{bcolors.OKGREEN}Kit OK{bcolors.ENDC}")
        vs.save_image(img, "Test", "Images/Passed_Kits")
        send_alert_email(kit_type,kit_num)
    else:
        print(f"{bcolors.FAIL}Kit FAILED {bcolors.ENDC}")
        vs.save_image(img, "Test", "Images/Rejected_Kits")
