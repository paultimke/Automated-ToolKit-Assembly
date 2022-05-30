import PLC_sim.plc_dummy as plc_dummy
import plc_comm
from tkinter import ttk

# ---------- CONSTANTS ---------- #
# Calibration Related
REF_IMG_PATH = "Images/Calibration/Ref-img_test.png"
REF_OBJ_SIZE = 2.76

# Path to the CSV file with each screw's size information
KITS_DB_CSV_PATH = "Kits_DataBase.csv"

# Default Background Color of UI
UI_BACKGROUND_COLOR = "#ECECEC" 

# Conveyor PLC IP Info
PLC_IP_ADDRESS = "192.168.0.1"
PLC_RACK = 0
PLC_RACK_SLOT = 2
PLC_DATABLOCK = 2
PLC_DB_SIZE = 6

# Global variables
Calibration_size : int = None    # Dimensions (length, width) of the reference Calibration object

StartProcess_Btn : ttk.Button = None # Button in UI to start the whole assembly and verification process

plc = None # PLC object, must be initialized either with plc_comm.PLC() or plc_dummy.PLC()
