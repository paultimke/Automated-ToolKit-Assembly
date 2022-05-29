import helper
import time
import Vision as vs
from PLC_sim.plc_dummy import PLC
import main_UI as UI
import Global_vars as glob


def setup() -> None:
    """
    Setup Function
    This function sets up the hardware connections and initializes
    Reference and Calibration values

    @return -> None
    """
    # Hardware Setup
    plc = PLC(6)
    plc.clearDB()   

    # Calibrate camera
    glob.Calibration_size = vs.calibrate_cam(glob.REF_IMG_PATH, glob.REF_OBJ_SIZE)


def Start_Assembly(kit: str, iterations: int) -> None:
    """
    Start Assembly Function
    This function starts the assembly process by sending commands to the 
    Robot and Conveyor PLCs

    @kit_info : String containing the desired Kit name
    @iterations: How many times you wish to assemble that kit

    @return -> None
    """
    pass

def Verify_Kit(ref_kit : dict) -> None:

    # Get reference sizes from CSV file
    ref_sizes = helper.create_RefSizesList()

    # Take image, process and classify
    img, sizes = vs.img_detectSizes()      
    _, assembled_kit = helper.classify(sizes, ref_sizes)

    helper.compare_kits(assembled_kit, ref_kit, img)

    print(f"Current kit = {assembled_kit}")



# ------ Program Start ------ #
if __name__ == "__main__":
    setup()
    root = UI.root()
    root.mainloop()
    
