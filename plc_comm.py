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
    def write_TestBool1(self, value: bool) -> None:
        # TestBool1 is bit 0 of Byte 0
        if value:
            self.__DB[0] |= 0x01 # mask to set bit 0
        else:
            self.__DB[0] &= 0xFE # mask to clear bit 0
        self.__client.db_write(self.__DBnum, 0, self.__DB)

    def write_TestBool2(self, value: bool) -> None:
        # TestBool2 is bit 1 of Byte 0
        if value:
            self.__DB[0] |= 0x02 # mask to set bit 1
        else:
            self.__DB[0] &= 0xFD # mask to clear bit 1
        self.__client.db_write(self.__DBnum, 0, self.__DB)

    def write_TestInt1(self, value: int) -> None:
        # TestInt1 resides in Bytes 2 and 3, so start offset is 2
        snap7.util.set_int(self.__DB, 2, value)
        self.__client.db_write(self.__DBnum, 2, self.__DB[2:4])

    def write_TestInt2(self, value: int) -> None:
        # TestInt2 resides in Bytes 4 and 5, so start offset is 4
        snap7.util.set_int(self.__DB, 4, value)
        self.__client.db_write(self.__DBnum, 4, self.__DB[4:6])

    # Data Reading methods
    def read_TestBool1(self) -> bool:
        self.__DB = self.__client.db_get(self.__DBnum)
        return snap7.util.get_bool(self.__DB, 0, 0)

    def read_TestBool2(self) -> bool:
        self.__DB = self.__client.db_get(self.__DBnum)
        return snap7.util.get_bool(self.__DB, 0, 1)

    def read_TestInt1(self) -> int:
        self.__DB = self.__client.db_get(self.__DBnum)
        return snap7.util.get_int(self.__DB, 2)

    def read_TestInt2(self) -> int:
        self.__DB = self.__client.db_get(self.__DBnum)
        return snap7.util.get_int(self.__DB, 4)


