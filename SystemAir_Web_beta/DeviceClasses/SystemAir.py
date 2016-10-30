#!/usr/bin/env python3.4

from EVENTLIST_Class import EVENTLIST
from MySQLdb import OperationalError
import time
import minimalmodbus
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL=True
minimalmodbus.BAUDRATE = 9600
minimalmodbus.TIMEOUT = 0.5
minimalmodbus.PARITY = 'N'
MaxNumOfTry = 10

LOKAL_EVENTLIST = EVENTLIST('192.168.1.31','bthovda','raspberry','IMS_FJELLMOVEIEN8','EVENTLIST')


class SystemAirUnit( minimalmodbus.Instrument ):
    
    
    def __init__(self, portname, slaveaddress, LocationName, Tag):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
        self.Name = LocationName
        self.TagNr = Tag



    ## Registers for fan control
  
    def get_fan_lvl(self):
        """Return the fan speed level."""
        return self.Tolerant_read_register(100)
        
   
 
    def set_fan_lvl(self, value):
        """Sett the fan speed level. value = 1-3"""
        TAG_INSTR = 'Fan speed'
        EVENT_TEXT = 'Endret vifte hastighet'
        Confirmed = False
        Gammel_Verdi = self.Tolerant_read_register(100)
        minimalmodbus._checkInt(value, minvalue=1, maxvalue=3, description='fan value')
        if Gammel_Verdi != value:
            self.Tolerant_write_register(100, value)
            Confirmed = value == int(self.Tolerant_read_register(100))
            LOKAL_EVENTLIST.LogEvent(str(self.TagNr)+"-"+str(TAG_INSTR), Gammel_Verdi , value, EVENT_TEXT, 'Auto',Confirmed)
        return self.Tolerant_read_register(100)
    ## Registers for heater control

    def get_temp_lvl(self):
        """Return the temperatur level."""
        return self.Tolerant_read_register(206)
        
    def Check_DI3(self):
        """Return the temperatur level."""
        return self.Tolerant_read_register(700)
  
  
    def set_temp_lvl(self, value):
        """sett the temperatur level. value = 0-5"""
        TAG_INSTR = 'TEMP'
        EVENT_TEXT = 'Endret temperatur i tilf. luft (min:1 -> max:5)'
        Confirmed = False
        Gammel_Verdi = self.Tolerant_read_register(206)
        minimalmodbus._checkInt(value, minvalue=0, maxvalue=5, description='temp value')
        if Gammel_Verdi != value:
            self.Tolerant_write_register(206, value)
            Confirmed = value == int(self.Tolerant_read_register(206))
            try:
               LOKAL_EVENTLIST.LogEvent(str(self.TagNr)+"-"+str(TAG_INSTR), Gammel_Verdi , value, EVENT_TEXT, 'Auto',Confirmed)
            except OperationalError:
            #do what you want to do on the error
             LOKAL_EVENTLIST.Connect()
                
        return self.Tolerant_read_register(206)


    def get_supply_temp(self):
        """Supply air sensor"""
        return self.Tolerant_read_register(213, 1)


    def get_extr_temp(self):
        """Extract air sensor"""
        return self.Tolerant_read_register(214, 1)


    def get_exha_temp(self):
        """Exhaust air sensor"""
        return self.Tolerant_read_register(215, 1)


    def get_heat_temp(self):
        """Overheat sensor"""
        return self.Tolerant_read_register(216, 1)


    def get_out_temp(self):
        """Outdoor air sensor"""
        return self.Tolerant_read_register(217, 1)


    ## Registers for system parameters

    def get_system_type(self):
        """Check Model name"""
        model_list = ['VR400', 'VR700', 'VR700DK', 'VR400DE', 'VTC300','VTC700',6,7,8,9,10,11,'VTR150K',
                      'VTR200B', 'VSR300', 'VSR500', 'VSR150', 'VTR300', 'VTR500', 'VSR300DE', 'VTC200']
        model = self.Tolerant_read_register(500)
        return model_list[model]


	## Registers for the filter

    def get_filter_day(self):
        """Check days since last filter change"""
        return self.Tolerant_read_register(601)

## Alternative read and write. Tries 10 times before giving up.
    def Tolerant_read_register(self, RegNum, NumDec=0):
        result = None
        NumOfTry = 0
        while result is None and NumOfTry < MaxNumOfTry:
            try:
                result = self.read_register(RegNum, NumDec)
                return result
            except IOError:
                NumOfTry = NumOfTry + 1
                print(str(NumOfTry)+" IOERROR, prover igjen")
                pass
            
    def Tolerant_write_register(self, RegNum, value):
        NumOfTry = 0
        success = False
        while success == False and NumOfTry < MaxNumOfTry:
            try:
                self.write_register(RegNum, value)
                success = True
            except IOError:
                NumOfTry = NumOfTry + 1
                print(str(NumOfTry)+" IOERROR, prover igjen")
                pass
            
if __name__ == '__main__':
   Ventilasjon_8a = SystemAirUnit('/dev/ttyUSB0', 1, "Fjellmoveien 8a",'VENT8A')
   # print(Ventilasjon_8a.get_fan_lvl())
   print Ventilasjon_8a.set_fan_lvl(2)
   print Ventilasjon_8a.Check_DI3()
   pass

