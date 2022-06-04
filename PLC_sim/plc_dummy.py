import snap7
from PLC_sim.DB_dummy import dummy

# Works for only one Data Block per PLC
class PLC:

    #------ Class Attributes ------#
    START_ADDRESS : int = None
    DB            : bytearray = None
    DBsize        : int = None

    #------ Class Methods ------#

    def __init__(self, DB_size) -> None:
        self.DBsize = DB_size
        dummy.start("PLC_sim/DataBlock.txt", DB_size)
        self.DB = dummy.DB_read()
        return None

    # Erase all memory in PLC Data Block
    def clearDB(self) -> None:
        for i in range(self.DBsize):
            self.DB[i] = 0
        dummy.DB_write(self.DB)
        
    # --- Data Writing methods --- #
    def write_Start_main_process(self, value: bool) -> None:
        # TestBool1 is bit 0 of Byte 0
        if value:
            self.DB[0] |= 0x01 # mask to set bit 0
        else:
            self.DB[0] &= 0xFE # mask to clear bit 0
        dummy.DB_write(self.DB)

    def write_Start_vision_cmd(self, value: bool) -> None:
        # TestBool2 is bit 1 of Byte 0
        if value:
            self.DB[0] |= 0x02 # mask to set bit 1
        else:
            self.DB[0] &= 0xFD # mask to clear bit 1
        dummy.DB_write(self.DB)

    def write_Screw_ID(self, value) -> None:
        # TestInt1 resides in Bytes 2 and 3, so start offset is 2
        snap7.util.set_int(self.DB, 2, value)
        dummy.DB_write(self.DB)

    def write_Kit_ID(self, value) -> None:
        # TestInt2 resides in Bytes 4 and 5, so start offset is 4
        snap7.util.set_int(self.DB, 4, value)
        dummy.DB_write(self.DB)

    def write_Vision_Result(self, value) -> None:
        # Vision_Result resides in Bytes 6 and 7, so start offset is 6
        snap7.util.set_int(self.DB, 6, value)
        dummy.DB_write(self.DB)

    def write_Screw_Bandeja(self, value: int) -> None:
        # TestInt2 resides in Bytes 8 and 9, so start offset is 8
        snap7.util.set_int(self.DB, 8, value)
        dummy.DB_write(self.DB)

    # --- Data Reading methods --- #
    def read_Start_vision_cmd(self) -> bool:
        self.DB = dummy.DB_read()
        return snap7.util.get_bool(self.DB, 0, 1)


