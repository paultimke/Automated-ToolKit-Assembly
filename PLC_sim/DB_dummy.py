class dummy:

    path    : str = None
    DBsize  : int = None

    def start (file_path : str, DBsize : int) -> None:
        dummy.path = file_path
        dummy.DBsize = DBsize

    def DB_read() -> bytearray:
        Datablock = bytearray()
        with open(dummy.path) as f:
            for line in f:
                Datablock.append(int(line))
        return Datablock

    def DB_write (DB : bytearray) -> None:
        with open(dummy.path, 'w') as f:
            for i in range(dummy.DBsize):
                f.write(str(DB[i]))
                if i < dummy.DBsize:
                    f.write('\n')
