# Constants
REF_IMG_PATH = "Images/Calibration/Ref-img_test.png"
REF_OBJ_SIZE = 2.76

KITS_DB_CSV_PATH = "Kits_DataBase.csv"

# Global variables
Calibration_size : int = None    # Dimensions (length, width) of the reference Calibration object
ref_sizes        : list = None   # List of tuples containing the length and width info of each screw type
                                 # inside the CSV file (KITS_DB_CSV_PATH)