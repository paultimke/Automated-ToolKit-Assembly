import helper
import time
import Vision as vs
from PLC_sim.plc_dummy import PLC
import pandas as pd

# Constants
REF_IMG_PATH = "Images/Calibration/Ref-img_test.png"
REF_OBJ_SIZE = 2.76

# ------ Main Function ------ #
def main() -> None:

    # ---------- SETUP ---------- #
    # Hardware Setup
    plc = PLC(6)
    plc.clearDB()   

    # Read Kits DataBase csv file
    df = pd.read_csv("Kits_DataBase.csv")

    # Calibrate camera
    Calibration_size = vs.calibrate_cam(REF_IMG_PATH, REF_OBJ_SIZE)
    # Ask user input for kit
    ref_kit, n_IDs = helper.create_Kit(df)
    # Get reference sizes from CSV file
    ref_sizes = helper.create_RefSizesList(df)

    # ------- KIT ASSEMBLY ------- #

    # ----- KIT VERIFICATION ----- #

    # Take image, process and classify
    img, sizes = vs.img_detectSizes(Calibration_size)      
    _, kit = helper.classify(sizes, ref_sizes, n_IDs, df)

    print(f"Current kit = {kit}")
    helper.compare_kits(kit, ref_kit, img)


# ------ Program Start ------ #
if __name__ == "__main__":
    main()
    
