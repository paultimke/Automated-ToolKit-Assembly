import helper
import time
import Vision as vs
from PLC_sim.plc_dummy import PLC
import pandas as pd
import cv2

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

    # Calibrate camera
    ref_img = vs.get_ref_path("Images\Calibration_imgs\Ref-img_26cm.png", 2.79)
    # Ask user input for kit
    ref_kit, n_IDs = helper.create_Kit(df)
    # Get reference sizes from CSV file
    ref_sizes = helper.create_RefSizesList(df)
    # ----- KIT ASSEMBLY ----- #

    # Take image, process and classify
    img, sizes = vs.img_detectSizes(ref_img)      
    objects, kit = helper.classify(sizes, ref_sizes, n_IDs, df)

    print(f"Current kit = {kit}")
    helper.compare_kits(kit, ref_kit, img)
