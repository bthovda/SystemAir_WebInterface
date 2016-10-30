from DeviceClasses.SystemAir import SystemAirUnit
from DeviceClasses.MelCloud_Class import Varmepumpe
from DeviceClasses.Regnskvett import Vaerdata
from DeviceClasses.TestDataBase_Class import TestDataBase
from DeviceClasses.EVENTLIST_Class import EVENTLIST

import time

start_time = time.time()

Lokalt_Vaer = Vaerdata("http://www.regnskvett.com/clientraw.txt", "Randaberg")
Ventilasjon_8a = SystemAirUnit('/dev/ttyUSB0', 1, "Fjellmoveien 8a",'VENT8A')
VarmePumpe_Stue = Varmepumpe('bthovda@gmail.com','Torvastad7',47887,10126,'VP_STUE')
VarmePumpe_LoftStue = Varmepumpe('bthovda@gmail.com','Torvastad7',47868,10126,'VP_LOFT')
TESTLISTE = TestDataBase('192.168.1.31','bthovda','raspberry','IMS_FJELLMOVEIEN8','TestTabell')
LOKAL_EVENTLIST = EVENTLIST('192.168.1.31','bthovda','raspberry','IMS_FJELLMOVEIEN8','EVENTLIST')
#LOKAL_ALARMLIST =
print("Finished setting up devices:" + str((time.time() - start_time)))
#print ( 'Navn:                      : '+Ventilasjon_8a.Name)
#print ( 'Model                      : {0}'.format (Ventilasjon_8a.get_system_type()))
#print ( 'Last filter change         : {0} Days'.format (Ventilasjon_8a.get_filter_day()))
#print ( 'Temperatur setting         :   {0}'.format (Ventilasjon_8a.get_temp_lvl()))
#print ( 'Fan Setting                :   {0}'.format (Ventilasjon_8a.get_fan_lvl()))
#print ( 'Supply air temp            :  {0}C'.format (Ventilasjon_8a.get_supply_temp()))
#print ( 'Extract air temp           :  {0}C'.format (Ventilasjon_8a.get_extr_temp()))   
#print ( 'Exhaust air temp           :{0}C'.format (Ventilasjon_8a.get_exha_temp()))  
#print ( 'Overheat sensor            :  {0}C'.format (Ventilasjon_8a.get_heat_temp()))
#print ( 'Outdoor air                :   {0}C'.format (Ventilasjon_8a.get_out_temp()))

#print ('Regnskvett temp ute         : '+Lokalt_Vaer.Temperatur())
#print ('Regnskvett Luftfukt         : '+Lokalt_Vaer.LuftFuktighet())
#print ('Regnskvett VindRetn         : '+Lokalt_Vaer.VindRetning())

#print ('Varmepumpe Stue Temp        : '+str(VarmpePumpe_Stue.RoomTemperature()))
#print ('Varmepumpe LoftStue Temp    : '+str(VarmpePumpe_LoftStue.RoomTemperature()))
#Ventilasjon_8a.set_fan_lvl(2)
#Ventilasjon_8a.set_fan_lvl(1)
#Ventilasjon_8a.set_fan_lvl(3)
#Ventilasjon_8a.set_fan_lvl(1)
#Ventilasjon_8a.set_fan_lvl(2)
#Ventilasjon_8a.set_fan_lvl(3)
#Ventilasjon_8a.set_fan_lvl(1)
#Ventilasjon_8a.set_fan_lvl(2)
#Ventilasjon_8a.set_fan_lvl(1)
#Ventilasjon_8a.set_fan_lvl(3)
#Ventilasjon_8a.set_fan_lvl(1)
#Ventilasjon_8a.set_fan_lvl(2)
Ventilasjon_8a.set_fan_lvl(2)
#Ventilasjon_8a.set_fan_lvl(1)
#Ventilasjon_8a.set_fan_lvl(2)
#VarmePumpe_Stue.TurnPowerOn()
#VarmePumpe_Stue.SetFanspeed(3)
#Ventilasjon_8a.set_temp_lvl(4)
#TESTLISTE.Store_TestData('T001-Oregon',Lokalt_Vaer.VindRetning())
#LogEvent(self, Tag, OldValue, NewValue, Description):
#LOKAL_EVENTLIST.LogEvent('T-001', 4, 5, 'Manual change 4 to 5')


print("--- %s seconds ---" % (time.time() - start_time))