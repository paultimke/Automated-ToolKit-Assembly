from typing import Tuple
import pandas as pd
import Vision as vs

class bcolors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def create_RefSizesList(df: pd.DataFrame) -> list:
    ref_list = []
    for i in range(len(df.index)):
        ref_list.append((df.iloc[i][1], df.iloc[i][2]))

    return ref_list

def create_Kit(df: pd.DataFrame) -> dict:
    n_IDs = len(df.index)
    strings = []
    Kit = {}

    for i in range(n_IDs):
        strings.append(df.iloc[i][0])
    for i in range(n_IDs):
        Kit[strings[i]] = int(input(f"Item count for Type {strings[i]}: "))
    
    return (Kit, n_IDs)


def is_inRange(val: tuple, ref: tuple, precision: float) -> bool:
    maxA = ref[0] + (ref[0] * precision)
    minA = ref[0] - (ref[0] * precision)
    maxB = ref[1] + (ref[1] * precision)
    minB = ref[1] - (ref[1] * precision)
    
    exp1 = ((val[0]>minA and val[0]<maxA) and (val[1]>minB and val[1]<maxB))
    exp2 = ((val[0]>minB and val[0]<maxB) and (val[1]>minA and val[1]<maxA))

    return (exp1 or exp2)


def classify(obj_sizes: list, ref_sizes: list, n_types: int, df: pd.DataFrame) -> Tuple[list, list]:
    n = len(obj_sizes) # Number of objects detected
    objects = []       # List to store the classification of each object
    hist = {}          # Dictionary to store the histogram
    IDs = []           # String List of ID tags

    # Populate histogram
    for i in range(n_types):
        IDs.append(df.iloc[i][0])
    for i in range(n_types):
        hist[IDs[i]] = 0

    # Classify each object and make a histogram of each type
    for i in range(n):
        for j in range(n_types):
            if is_inRange(obj_sizes[i], ref_sizes[j], 0.3):
                objects.append((i, IDs[j]))
                hist[IDs[j]] += 1

    return (objects, hist)

def compare_kits(cmp: list, ref: list, img: vs.Mat):
    if cmp == ref:
        print(f"{bcolors.OKGREEN}Kit OK{bcolors.ENDC}")
        vs.save_image(img, "Test", "Images/Passed_Kits")
    else:
        print(f"{bcolors.FAIL}Kit FAILED {bcolors.ENDC}")
        vs.save_image(img, "Test", "Images/Passed_Kits")



