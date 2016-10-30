import httplib, urllib
from time import localtime, strftime
import time

from DeviceClasses.SystemAir import SystemAirUnit
from DeviceClasses.Regnskvett import Vaerdata
from DeviceClasses.MelCloud_Class import Varmepumpe
from DeviceClasses.KlimaDataHus_Class import KlimaDataHus

def doit():

    Ventilasjon_8a = SystemAirUnit('/dev/ttyUSB0', 1, "Fjellmoveien 8a",'VENT8A')

    VarmePumpe_Stue = Varmepumpe('bthovda@gmail.com','Torvastad7',47887,10126,'VP_STUE')
    VarmePumpe_LoftStue = Varmepumpe('bthovda@gmail.com','Torvastad7',47868,10126,'VP_LOFT')

    BadUetg = KlimaDataHus(53761, "Bad U.etg")
    Vaskerom = KlimaDataHus(48897, "Vaskerom")
    Bad2etg = KlimaDataHus(51201, "Bad 2.etg")


    Lokalt_Vaer = Vaerdata("http://www.regnskvett.com/clientraw.txt", "Randaberg")
    VarmePumpe_Stue.RefreshLocalData()
    VarmePumpe_LoftStue.RefreshLocalData()
    
    #KlimaDataUte:
    TempOut = Lokalt_Vaer.Temperatur()
    Baro = Lokalt_Vaer.LuftTrykk()
    VindMS = Lokalt_Vaer.VindStyrke()
    VindRettn = Lokalt_Vaer.VindRetning()
    LastWeatherUpdate = Lokalt_Vaer.LastUpdate()
    LuftFukt = Lokalt_Vaer.LuftFuktighet()
    #KlimaDataHus:
    BadUetgTemp = BadUetg.Temperatur()
    BadUetgFukt = BadUetg.Fuktighet()
    VaskeromTemp = Vaskerom.Temperatur()
    VaskeromFukt = Vaskerom.Fuktighet()
    Bad2etgTemp = Bad2etg.Temperatur()
    Bad2etgFukt = Bad2etg.Fuktighet()
    #Ventilasjon:
    SupplyAir = Ventilasjon_8a.get_supply_temp()
    ExtractAir = Ventilasjon_8a.get_extr_temp()
    VarmeIndex = Ventilasjon_8a.get_temp_lvl()
    ViftHast = Ventilasjon_8a.get_fan_lvl()
    #Varmepumpe:
    ActLoftStueTemp = VarmePumpe_LoftStue.RoomTemperature()
    SetLoftStueTemp = VarmePumpe_LoftStue.TargetTemperature()
    ActStueTemp = VarmePumpe_Stue.RoomTemperature()
    SetStueTemp = VarmePumpe_Stue.TargetTemperature()
    ModeStue = VarmePumpe_Stue.OperationModeTEXT()
    ModeLoftStue = VarmePumpe_LoftStue.OperationModeTEXT()

    
    paramsFUKT = urllib.urlencode({'field1': VaskeromFukt, 
                               'field2': Bad2etgFukt,
                               'field3': BadUetgFukt, 
                               'field4': 0,
                               'field5': LuftFukt, 
                               'field6': ViftHast,
                               'key':'GOCOJRI3GVWSWRDW'})

    paramsTEMP = urllib.urlencode({'field1': ActStueTemp, 
                                    'field2': ActLoftStueTemp,
                                    'field3': BadUetgTemp, 
                                    'field4': VaskeromTemp,
                                    'field5': Bad2etgTemp, 
                                    'field6': SetLoftStueTemp,
                                    'field7': SetStueTemp,
                                    'field8': TempOut,
                                    'key':'8GNC36S2WO2RFKM4'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
	
    try:
	    conn.request("POST", "/update", paramsFUKT, headers)
	    response = conn.getresponse()
	    print strftime("%a, %d %b %Y %H:%M:%S", localtime())
	    print response.status, response.reason
	    data = response.read()
	    conn.close()
    except:
	    print "connection failed"

    try:
	    conn.request("POST", "/update", paramsTEMP, headers)
	    response = conn.getresponse()
	    print strftime("%a, %d %b %Y %H:%M:%S", localtime())
	    print response.status, response.reason
	    data = response.read()
	    conn.close()
    except:
	    print "connection failed"


#sleep for 60 seconds (api limit of 15 secs)
if __name__ == "__main__":
	   while True:
		    doit()
		    time.sleep(60) 
