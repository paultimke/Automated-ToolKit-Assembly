import snap7

# Works for only one Data Block per PLC
class PLC:

    #------ Class Attributes ------#
    __START_ADDRESS : int = 0
    __DB            : bytearray = None
    __DBnum         : int = None
    __DBsize        : int = None
    __client        : snap7.client.Client = None

    #------ Class Methods ------#

    def __init__(self, IP, rack, slot, DB_number, DB_size) -> None:
        self.__client = snap7.client.Client()
        self.__client.connect(IP, rack, slot)
        self.__DBnum = DB_number
        self.__DBsize = DB_size
        self.__DB = self.__client.db_read(DB_number, self.__START_ADDRESS, DB_size)
        return None

    # Erase all memory in PLC Data Block
    def clearDB(self) -> None:
        for i in range(self.__DBsize):
            self.__DB[i] = 0
        self.__client.db_write(self.__DBnum, 0, self.__DB)

    # Data Writing methods
    def write_Start_main_process(self, value: bool) -> None:
        # TestBool1 is bit 0 of Byte 0
        if value:
            self.__DB[0] |= 0x01 # mask to set bit 0
        else:
            self.__DB[0] &= 0xFE # mask to clear bit 0
        self.__client.db_write(self.__DBnum, 0, self.__DB)

    def write_Start_vision_cmd(self, value: bool) -> None:
        # TestBool2 is bit 1 of Byte 0
        if value:
            self.__DB[0] |= 0x02 # mask to set bit 1
        else:
            self.__DB[0] &= 0xFD # mask to clear bit 1
        self.__client.db_write(self.__DBnum, 0, self.__DB)

    def write_Screw_ID(self, value: int) -> None:
        # TestInt1 resides in Bytes 2 and 3, so start offset is 2
        snap7.util.set_int(self.__DB, 2, value)
        self.__client.db_write(self.__DBnum, 2, self.__DB[2:4])

    def write_kit_ID(self, value: int) -> None:
        # TestInt2 resides in Bytes 4 and 5, so start offset is 4
        snap7.util.set_int(self.__DB, 4, value)
        self.__client.db_write(self.__DBnum, 4, self.__DB[4:6])

    def write_Vision_Result(self, value: int) -> None:
        # TestInt2 resides in Bytes 6 and 7, so start offset is 6
        snap7.util.set_int(self.__DB, 6, value)
        self.__client.db_write(self.__DBnum, 6, self.__DB[6:8])

    def write_Screw_Bandeja(self, value: int) -> None:
        # TestInt2 resides in Bytes 8 and 9, so start offset is 8
        snap7.util.set_int(self.__DB, 8, value)
        self.__client.db_write(self.__DBnum, 8, self.__DB[8:10])

    # Data Reading methods
    def read_Start_vision_cmd(self) -> bool:
        self.__DB = self.__client.db_get(self.__DBnum)
        return snap7.util.get_bool(self.__DB, 0, 1)



