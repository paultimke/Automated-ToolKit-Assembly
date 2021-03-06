import time
import Vision as vs
import main_UI as UI
import Global_vars as glob
import helper

# Debug Flag to use the PLC DataBlock Simulator
USING_PLC_DUMMY = False
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
    # Clear all on PLC DataBlock
    plc = helper.connect_to_plc()
    plc.clearDB()

    # Calibrate camera
    glob.Calibration_size = vs.calibrate_cam(glob.REF_IMG_PATH, glob.REF_OBJ_SIZE)
# END OF FUNCTION setup()

def Start_Assembly(name: str, ref_kit: dict) -> None:
    """
    Start Assembly Function
    This function starts the assembly process by sending commands to the 
    Robot and Conveyor PLCs

    @kit_info : String containing the desired Kit name
    @iterations: How many times you wish to assemble that kit

    @return -> None
    """
    # Hardware Setup
    plc = helper.connect_to_plc()
    plc.clearDB()
    time.sleep(1)

    # Mandar un pulso de 1 segundo para empezar proceso en PLC
    plc.write_Start_main_process(True)
    time.sleep(1)
    plc.write_Start_main_process(False)

    if name == 'Test kit 1':
        plc.write_Kit_ID(1)
    elif name == 'Test kit 2':
        plc.write_Kit_ID(2)
    else:
        plc.write_Kit_ID(5)

        plc.write_Grande_Cant(ref_kit['grande'])
        plc.write_Mediano_Cant(ref_kit['mediano'])
        plc.write_Flaco_Cant(ref_kit['flaco'])
        plc.write_Tuerca_Cant(ref_kit['tuerca'])

    #for i in range(4):
    #   plc.write_Screw(screwID, cuantos)

#END OF FUNCTION Start_Assembly()

def Verify_Kit(ref_kit : dict, kit_type:str, kit_num:int) -> None:

    # Get reference sizes from CSV file
    ref_sizes = helper.create_RefSizesList()

    # Take image, process and classify
    img, sizes, perims = vs.img_detectSizes()      
    _, assembled_kit = helper.classify(sizes, ref_sizes, perims)

    kit_ok = helper.compare_kits(assembled_kit, ref_kit, img, kit_type, kit_num)

    print(f"Current kit = {assembled_kit}")

    return kit_ok
#END OF FUNCTION Verify_Kit()


# ---------- Program Start ---------- #
if __name__ == "__main__":
    setup()
    root = UI.root()
    root.mainloop()
    
