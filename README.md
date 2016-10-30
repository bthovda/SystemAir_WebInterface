# SystemAir_WebInterface
Created by Bjoern Tore Hovda

Web interface for SystemAir residental HVAC units

The modbus driver is based on this repository: https://github.com/wimpy87/sambus. (Thank you Atle!!)

Important: will be accessible for everyone on the Wifi.

My Setup/requriments
Raspberry Pi 
 - Wifi dongle or ethernet cable
 - 'USB to modbus converter' connected to my Systemair residental unit.


Installation:

1. Install flask
   sudo apt-get install python3-flask
   
2. Customize SystemAir_Web.py with unit name and IP adress of your raspberry Pi.

3. Run SystemAir_Web.py

4. Web interface will now be accessible via web browser (http://YOUR_RASPBERRY_IP:8040/)


For Autostart on each reboot use systemd or supervisor.

systemd tutorial:
http://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/
(instead of myscript.py use SystemAir_Web.py)
