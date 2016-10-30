from flask import Flask, render_template, redirect, url_for
from DeviceClasses.SystemAir_Class import SystemAirUnit

Ventilation_Unit = SystemAirUnit('/dev/ttyUSB0', 1, "NAME OF YOUR HOUSE",'UNITNICK')
IP_ADDR_RASPBERRY = "192.168.1.158"
app = Flask(__name__)

@app.route('/')
def PanelPage():

    #Collect current data:
    SupplyAir = Ventilation_Unit.get_supply_temp()
    ExtractAir = Ventilation_Unit.get_extr_temp()
    HeatIndex = Ventilation_Unit.get_temp_lvl()
    FanSpeed = Ventilation_Unit.get_fan_lvl()
    HouseName = 'Your Address'
    UnitName = 'Unit Name i.e Home HVAC'
    
    #Prepare data for Webpage/Panel:
    FanIconSrc = str('/static/V'+str(FanSpeed)+'.png')
    HeatIconSrc = str('/static/T'+str(HeatIndex)+'.png')
    PanelSrc = '/static/Panel.png'
    templateData = {'HouseName' : HouseName,
                    'UnitName' : UnitName,
                    'Fan' : str(FanSpeed),
                    'Heat' : str(HeatIndex),
                    'PanelSrc' : PanelSrc,
                    'FanIconSrc' : FanIconSrc,
                    'HeatIconSrc' : HeatIconSrc,
                    'SupplyAir' : SupplyAir,
                    'ExtractAir': ExtractAir}

    return render_template("index.html",**templateData)

@app.route("/Sminus")  
def DecreaseSpeed():
    CurrSpeedLevel = Ventilation_Unit.get_fan_lvl()
    NewSpeedLevel = max(CurrSpeedLevel-1,1)
    Ventilation_Unit.set_fan_lvl(NewSpeedLevel)

    return redirect(url_for('PanelPage'))
    
@app.route('/Splus')
def IncreaseSpeed():
    CurrSpeedLevel = Ventilation_Unit.get_fan_lvl()
    NewSpeedLevel = min(CurrSpeedLevel+1,3)
    Ventilation_Unit.set_fan_lvl(NewSpeedLevel)

    return redirect(url_for('PanelPage'))
    
@app.route("/Hplus")  
def IncreaseTemp():
    CurrTempLevel = Ventilation_Unit.get_temp_lvl()
    NewTempLevel = min(CurrTempLevel+1,5)
    Ventilation_Unit.set_temp_lvl(NewTempLevel)
    
    return redirect(url_for('PanelPage'))

@app.route("/Hminus")  
def DecreaseTemp():
    CurrTempLevel = Ventilation_Unit.get_temp_lvl()
    NewTempLevel = max(CurrTempLevel-1,1)
    Ventilation_Unit.set_temp_lvl(NewTempLevel)
    
    return redirect(url_for('PanelPage'))

if __name__ == "__main__": 
    app.run(debug=False, host="192.168.1.158", port=8040)
