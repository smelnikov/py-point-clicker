# Installation

## Drivers setup

    curl https://www.moxa.ru/files/drivers_utilities_3/driv_linux_mainline_uport1p_v1_4_build_18050314.tgz | tar xvz
    cd mxu11x0/
    make clean
    make install
    apt install setserial
    adduser %USER% dialout

## Python script setup

    git clone https://github.com/smelnikov/py-point-clicker.git
    cd py-point-clicker/
    pip install -r requirements.txt

## Autostart setup

    nano /etc/rc.local
    
    #!/bin/sh -e
    export DISPLAY=":0" BTN_PORT="/dev/ttyUSB0" BTN_RATE="9600" BTN_POS="920,400" BTN_SCRIPT="path/to/script/button.py"
    sleep 60 && setserial $BTN_PORT port 1 && sudo -E -H -u %USER% python $BTN_SCRIPT & 
    exit 0
    
    chmod +x /etc/rc.local

    sudo reboot
