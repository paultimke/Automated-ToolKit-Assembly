import PLC_sim.plc_dummy as plc_dummy
import plc_comm
import helper
import time
import Vision as vs
import main_UI as UI
import Global_vars as glob

# Debug Flag to use the PLC DataBlock Simulator
USING_PLC_DUMMY = True
if not USING_PLC_DUMMY:
    from Global_vars import PLC_IP_ADDRESS, PLC_RACK, PLC_RACK_SLOT, PLC_DATABLOCK, PLC_DB_SIZE

# ---------- Start of Function Definitions ---------- #

def setup() -> None:
    """
    Setup Function
    This function sets up the hardware connections and initializes
    Reference and Calibration values

    @return -> None
    """

    # Hardware Setup
    if USING_PLC_DUMMY:
        glob.plc = plc_dummy.PLC(6)
        glob.plc.clearDB()
    else:
        glob.plc = plc_comm.PLC(PLC_IP_ADDRESS, PLC_RACK, PLC_RACK_SLOT, 
                                PLC_DATABLOCK, PLC_DB_SIZE)
        glob.plc.clearDB()

    # Calibrate camera
    glob.Calibration_size = vs.calibrate_cam(glob.REF_IMG_PATH, glob.REF_OBJ_SIZE)

# END OF FUNCTION setup()

def Start_Assembly(kit: str, iterations: int) -> None:
    """
    Start Assembly Function
    This function starts the assembly process by sending commands to the 
    Robot and Conveyor PLCs

    @kit_info : String containing the desired Kit name
    @iterations: How many times you wish to assemble that kit

    @return -> None
    """
    # Clear all previous Flags
    glob.plc.clearDB()

    while(glob.plc.read_TestBool1() == False):
        print("On Idle")
        time.sleep(1)

    print("Loop broken")
    print("Now doing more stuff")

    while(glob.plc.read_TestBool2() == False):
        print("On idle again")
        time.sleep(1)

    print("Condition passed again. Loop broken")
    print("Now doing more stuff again")

#END OF FUNCTION Start_Assembly()

def Verify_Kit(ref_kit : dict) -> None:

    # Get reference sizes from CSV file
    ref_sizes = helper.create_RefSizesList()

    # Take image, process and classify
    img, sizes = vs.img_detectSizes()      
    _, assembled_kit = helper.classify(sizes, ref_sizes)

    helper.compare_kits(assembled_kit, ref_kit, img)
    

    print(f"Current kit = {assembled_kit}")
#END OF FUNCTION Verify_Kit()


# ---------- Program Start ---------- #
if __name__ == "__main__":
    setup()
    root = UI.root()
    root.mainloop()
    
