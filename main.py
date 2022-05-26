import helper
import time
import Vision as vs
from PLC_sim.plc_dummy import PLC
import pandas as pd

# ------ Main Function ------ #
def main() -> None:
    while(plc.read_TestBool1() == False):
        print("On Idle")
        time.sleep(1)

    print("Loop broken")
    print("Now doing more stuff")

    while(plc.read_TestBool2() == False):
        print("On idle again")
        time.sleep(1)

    print("Condition passed again. Loop broken")
    print("Now doing more stuff again")

# ------ Program Start ------ #

if __name__ == "__main__":

    # ----- SETUP ----- #

    # Hardware Setup
    plc = PLC(6)
    plc.clearDB()   

    # Read Kits DataBase csv file
    df = pd.read_csv("Kits_DataBase.csv")

    # Ask user input for kit
    ref_kit, n_IDs = helper.create_Kit(df)

    # ----- KIT ASSEMBLY ----- #

    # Take image, process and classify
    img, sizes = vs.img_detectSizes()
    objects, kit = helper.classify(sizes, helper.create_RefList(df), n_IDs, df)

    print(f"Current kit = {kit}")
    helper.compare_kits(kit, ref_kit, img)
