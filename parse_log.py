#!/usr/bin/env python3
import struct

with open("lv6548-home.log", "r") as f:
    for line in f:
        a = line.strip().split(" ", 4)
        if len(a) == 4:
            (f_time, f_level, f_name, f_data, ) = a
            r = bytearray.fromhex(f_data)
            #print(a, r)
            seq = struct.unpack('>H', r[0:2])
            protocol = struct.unpack('>H', r[2:4])
            header = f_data[4:4+6*2]
            #print(f_name, r[2:4], a[2].strip()[0:], r[2:])
            if f_name.startswith('SERVER-'):
                if header == '00010070ff04': # Periodic Stream Data
                    (AC_volt1, hz1, v2, hz2, AV_Output_VA, AC_Output_Watt, System_Output_Cap, Bus_Voltage, Battery_Volt, UNK2, Battery_Cap, UNK3, UNK4, PV1_Volt, UNK5, UNK6, Flags, UNK8, UNK9,  PV1_Watt, UNK10 ) = r[2+6+1:115].split(b" ")
                    if Flags[6] == 49: # NO SOLAR ?
                        flag_solar = True
                    else:
                        flag_solar = False
                    print('R1: POWER', 'AC Volt', AC_volt1, 'SOLAR VOLT',  PV1_Volt, 'SOLAW WATT', PV1_Watt, 'AC OUT WATT', AC_Output_Watt, flag_solar, Bus_Voltage)
                    #print(a[2][4:999].strip(), r[2:9999])
                elif header == '01020010ff01': # Wifi_Module_PN
                    Wifi_Module_PN = r[2+6:22]
                    print("WIFI Part Number", Wifi_Module_PN)
                elif header == '0001000fff04': # Some Model Number
                    Unknown_Model_No = r[2+6:-3]
                    print("Unknown Model No", Unknown_Model_No)
                elif header == '00010014ff04': # Secondary CPU Firmware, Main CPU Firmware and Serial Number ???????????????????????????????????? 
                    Firmware_CPU_Secondary = r[2+6+1:-3]
                    print("CPU Secondary", Firmware_CPU_Secondary)
                elif header == '0001000eff04': # Total Generated Wh
                    Total_Gen_Wh = r[2+6+1:-3]
                    print('GENERATED Wh Total', Total_Gen_Wh)
                elif header == '0001001cff04': # Serial & Other Info
                    t = r[2+6+1:-3]
                    Unit_SN = t[2:16]
                    Unknown = t[0:2]
                    Unknown2 = t[16:]
                    print("Some Unknown", Unit_SN, Unknown, Unknown2)
                elif header == '0001006f0104':
                    (Grid_Rating_Voltage, Grid_Rating_Current, AC_Output_Rating_Volt, AC_Output_Rating_Frequency, AC_Output_Rating_Current, AC_Output_Rating_VA, AC_Output_Rating_Watt, Battery_Rating_Voltage, Battery_Rating_Voltage2, Battery_CutOff_Volt, Battery_Bulk_Charging_Voltage, Battery_Float_Charging_Volt, Battery_Type, Max_AC_Charging_Current, UNKNOWN_030, UNKNOWN_1A, Output_Source_Priority, UNKNOWN_2I, Parallel_Max_Num, UNKNOWN_01, UNKNOWN_0t, UNKNOWN_0o, Battery_Back_to_Discharge_Volt, UNKNOWN_0s, UNKNOWN_1f, UNKNOWN_480, UNKNOWN_0f, UNKNOWN_100b ) = r[2+6+1:-3].split(b" ")
                    print('BigData', Max_AC_Charging_Current, Battery_Type, Battery_Back_to_Discharge_Volt, Grid_Rating_Voltage, Grid_Rating_Current, AC_Output_Rating_Volt, AC_Output_Rating_Frequency, AC_Output_Rating_Current, AC_Output_Rating_VA, AC_Output_Rating_Watt)
                    # Battery_Type : 0 = AGM, 2 = User
                    print(Output_Source_Priority) # 0 Utility Solar Bat, 1 Solar Utility Bat, 2 Solar Bat Utility
                elif header == '0001002b0104': # Led Setting
                    (Led_Status, Led_Speed, Led_Effect, Led_Brightness, Led_3, Led_Color_1) = r[2+6+1:-3].split(b" ")
                    print("LED Settings",Led_Status, Led_Speed, Led_Effect, Led_Brightness, Led_3, Led_Color_1)
                    # Violet-White-Sky Blue = 148000211255255255000255255
                    # White-Yellow-Green = 255255255255205032000255000
                    # Led Brightness : 5 = Normal, 9 = High, 1 = Low
                    # Led Effect: 0 = Means Breathing, 2 = Means Solid, 3 = Means Right Scrolling
                    # Led Speed : 1 = Normal, 2 = High, 0 = Low
                elif header == '000100110104':
                    pass
                    #UUU 0001001101042845626b7576787a44616a791cb90d bytearray(b'\x00\x01\x00\x11\x01\x04(EbkuvxzDajy\x1c\xb9\r') Buzzer disable
                    #UUU 000100110104284561626b7576787a446a7933290d bytearray(b'\x00\x01\x00\x11\x01\x04(EabkuvxzDjy3)\r') Buffer Enable
                elif header == '0001006fff04':
                    pass
                    #(120.0 54.1 120.0 60.0 54.1 6500 6500 48.0 48.0 44.0 58.4 54.0 2 002 030 1 2 2 9 01 0 0 56.0 0 1 480 0 100\x83\x08\r')
                else:
                    pass
                    #print('XXX', a[2][4:999].strip(), r[2:99999])
            elif f_name.startswith('CLIENT-'):
                #print('UUC', a[2][4:999].strip(), r[2:99999])

                if header == '00010010ff04': # Date Only ???  INFO SENT FROM THE SERVER.... SET THE TIME REMOTELY ON THE UNIT
                    Date_Unknown = r[2+6+1:-3]
                    print("DATE INFORMATION", Date_Unknown) # ED Eastern Day Time ? YYYYMMDD


            else:
                pass#print(a[2][4:999].strip(), r[2:99999]) # , r[2:9999].decode("utf-8", errors="ignore"))
