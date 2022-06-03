from plc_comm import PLC
import time

PLC_IP_ADDRESS = "192.168.0.1"
PLC_RACK = 0
PLC_RACK_SLOT = 2
PLC_DATABLOCK = 2
PLC_DB_SIZE = 10

plc = PLC(PLC_IP_ADDRESS,0,2,2,10)

plc.clearDB()

plc.write_Vision_Result(2)
#plc.write_Start_main_process(1)

plc.write_Screw_Bandeja(3)

time.sleep(1)

#plc.write_Start_main_process(0)
plc.write_Vision_Result(0)