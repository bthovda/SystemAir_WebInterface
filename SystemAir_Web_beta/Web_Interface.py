from flask import Flask, render_template, redirect, url_for
from ThingSpeakLogger import doit

from DeviceClasses.SystemAir import SystemAirUnit
from DeviceClasses.Regnskvett import Vaerdata
from DeviceClasses.MelCloud_Class import Varmepumpe
from DeviceClasses.KlimaDataHus_Class import KlimaDataHus
Ventilasjon_8a = SystemAirUnit('/dev/ttyUSB0', 1, "Fjellmoveien 8a",'VENT8A')

VarmePumpe_Stue = Varmepumpe('bthovda@gmail.com','Torvastad7',47887,10126,'VP_STUE')
VarmePumpe_LoftStue = Varmepumpe('bthovda@gmail.com','Torvastad7',47868,10126,'VP_LOFT')

BadUetg = KlimaDataHus(53761, "Bad U.etg")
Vaskerom = KlimaDataHus(48897, "Vaskerom")
Bad2etg = KlimaDataHus(51201, "Bad 2.etg")

app = Flask(__name__)

@app.route("/")
def StartSide():
    Lokalt_Vaer = Vaerdata("http://www.regnskvett.com/clientraw.txt", "Randaberg")
    VarmePumpe_Stue.RefreshLocalData()
    VarmePumpe_LoftStue.RefreshLocalData()
    #BadUetg.RefreshLocalData()
    #Vaskerom.RefreshLocalData()
    #Bad2etg.RefreshLocalData()
    
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
    
    #Grafisk:
    VifteIcon = 'V'+str(ViftHast)+".png"
    VarmeIcon = 'T'+str(VarmeIndex)+".png"
    templateData = {'Viftehastighet' : "Faktisk Viftehastighet: "+str(ViftHast),
                    'Varme' : "Varme: "+str(VarmeIndex),
                    'VifteIcon' : str("/static/"+VifteIcon), 
                    'VarmeIcon' : str("/static/"+VarmeIcon), 
                    'SupplyAir' : SupplyAir,
                    'ExtractAir': ExtractAir,
                    'TempOut' : TempOut,
                    'VindMS' : VindMS,
                    'VindRettn' : VindRettn,
                    'LuftFukt' : LuftFukt,
                    'Baro' : Baro,
                    'LastWeatherUpdate' : LastWeatherUpdate,
                    'ActLoftStueTemp' : ActLoftStueTemp,
                    'SetLoftStueTemp' : SetLoftStueTemp,
                    'ActStueTemp' : ActStueTemp,
                    'SetStueTemp' : SetStueTemp,
                    'ModeStue' : ModeStue,
                    'ModeLoftStue' : ModeLoftStue,
                    'BadUetgTemp' : BadUetgTemp,
                    'BadUetgFukt' : BadUetgFukt,
                    'VaskeromTemp' : VaskeromTemp,
                    'VaskeromFukt' : VaskeromFukt,
                    'Bad2etgTemp' : Bad2etgTemp,
                    'Bad2etgFukt' : Bad2etgFukt}
    #print templateData
    print LastWeatherUpdate
    return render_template("index.html",**templateData)

@app.route("/Splus")  
def IncreaseSpeed():
    CurrSpeedLevel = Ventilasjon_8a.get_fan_lvl()
    NewSpeedLevel = CurrSpeedLevel+1
    NewSpeedLevel = min(NewSpeedLevel,3)
    Ventilasjon_8a.set_fan_lvl(NewSpeedLevel)
    #doit() #oppdaterer Thingspeak (ressurskrevende)
    return redirect(url_for('StartSide'))

@app.route("/Sminus")  
def DecreaseSpeed():
    CurrSpeedLevel = Ventilasjon_8a.get_fan_lvl()
    NewSpeedLevel = CurrSpeedLevel-1
    NewSpeedLevel = max(NewSpeedLevel,1)
    Ventilasjon_8a.set_fan_lvl(NewSpeedLevel)
    #doit() #oppdaterer Thingspeak (ressurskrevende)
    return redirect(url_for('StartSide'))

@app.route("/Hplus")  
def IncreaseTemp():
    CurrTempLevel = Ventilasjon_8a.get_temp_lvl()
    NewTempLevel = CurrTempLevel+1
    NewTempLevel = min(NewTempLevel,5)
    Ventilasjon_8a.set_temp_lvl(NewTempLevel)
    return redirect(url_for('StartSide'))

@app.route("/Hminus")  
def DecreaseTemp():
    CurrTempLevel = Ventilasjon_8a.get_temp_lvl()
    NewTempLevel = CurrTempLevel-1
    NewTempLevel = max(NewTempLevel,1)
    Ventilasjon_8a.set_temp_lvl(NewTempLevel)
    return redirect(url_for('StartSide'))

@app.route('/T1')
def Testing():
    return render_template("Test1.html")
if __name__ == "__main__": 
    #app.run(host='0.0.0.0')
    app.run(debug=False, host="192.168.1.158", port=8060)
