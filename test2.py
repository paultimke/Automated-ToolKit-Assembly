from plc_comm import PLC

PLC_IP_ADDRESS = "192.168.0.1"
PLC_RACK = 0
PLC_RACK_SLOT = 2
PLC_DATABLOCK = 2
PLC_DB_SIZE = 6

plc = PLC(PLC_IP_ADDRESS,0,2,2,6)

plc.clearDB()

plc.write_TestInt1(1)