# Bruin Formula Racing Dashboard
Written by Guo (Jason) Liu 2022-2023<br>
Email liug22@hotmail.com for suggestions
 
### How to set up on Raspberry Pi
1. Connect Raspberry Pi and a screen with resolution around 1280x720 pixels to power supply.
2. Configure the Raspberry Pi according to [this manual](https://www.waveshare.com/w/upload/2/29/RS485-CAN-HAT-user-manuakl-en.pdf), test the can0 channel with can-utils
3. Package resource files (if you made any changes to them) with command: pyrcc5 resources.qrc -o resources.py
4. Upload non-resource files (excluding gui/resources, gui/main.ui and resources.qrc) to Raspberry Pi
5. Configure the resolution of Raspberry Pi to be 1280x720
6. Cd to main.py's directory, and run command: python main.py. The dashboard should display.
7. You may have to update constant scalers in globalfonts.py since fonts in Raspberry Pi's OS look different.
8. To hide the menu bar, enter in the terminal: `sudo nano /home/[name of your pi]/config/lxsession/LXDE-pi/autostart` and comment out by adding a '#' the line: `@lxpanel --profile LXDE`
9. To launch on boot, enter in the terminal
```
mkdir /home/[name of your pi]/.config/autostart
nano /home/pi/.config/autostart/mumble.desktop
```
