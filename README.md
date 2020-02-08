# MIDI-LED
Using a Raspberry Pi to control LED lights with MIDI output<br />

# Running on your RPI
## Installing program requirements
git clone https://github.com/jzarzycki/MIDI-LED.git<br />
cd MIDI-LED<br />
pip3 install -r requirements.txt<br />

sudo apt-get install -y nodejs npm

cd website<br />
npm install<br />

## Start program at boot automatically
<i>In bash enter:</i><br />
sudo crontab -e<br />
<i>And add at the end of the file:</i>
```
@reboot cd /home/pi/MIDI-LED/website && node app.js
@reboot python3 /home/pi/MIDI-LED/midi-led.py
```
<i>The program should now start automatically and be available at port 13579 on the ip address of your RaspberryPI (It needs to be connected to a WiFi, or work in access point mode. I plan to add instructions on how to do this in the future.)</i>

# Current Status
<a href="http://www.youtube.com/watch?feature=player_embedded&v=ZgxArVfICzk
" target="_blank"><img src="http://img.youtube.com/vi/ZgxArVfICzk/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>
