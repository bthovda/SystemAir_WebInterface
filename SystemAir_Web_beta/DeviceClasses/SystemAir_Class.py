#!/usr/bin/env python3.4

import time
import minimalmodbus
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL=True
minimalmodbus.BAUDRATE = 9600
minimalmodbus.TIMEOUT = 0.5
minimalmodbus.PARITY = 'N'
MaxNumOfTry = 10


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
        minimalmodbus._checkInt(value, minvalue=1, maxvalue=3, description='fan value')
        self.Tolerant_write_register(100, value)
        return self.Tolerant_read_register(100)
    ## Registers for heater control

    def get_temp_lvl(self):
        """Return the temperatur level."""
        return self.Tolerant_read_register(206)

    ## Kitchen fan (optional)
    def Check_DI3(self):
        """Return the temperatur level."""
        return self.Tolerant_read_register(700)


    def set_temp_lvl(self, value):
        """sett the temperatur level. value = 0-5"""
        minimalmodbus._checkInt(value, minvalue=0, maxvalue=5, description='temp value')
        self.Tolerant_write_register(206, value)

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
                print(str(NumOfTry)+" IOERROR, retry until max attemps")
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
                print(str(NumOfTry)+" IOERROR, retry until max attemps")
                pass

if __name__ == '__main__':
   Ventilation_BOB = SystemAirUnit('/dev/ttyUSB0', 1, "Test address",'Test unit')

   print Ventilation_BOB.get_fan_lvl()

   pass

