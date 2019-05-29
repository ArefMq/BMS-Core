# BMS-Core

BMS Controller project
-------------------------------------

## setup
In order to setup the project follow the steps below:

First clone the repository via:
```bash
# It is important to run this part at the home directory
cd ~
git clone https://github.com/ArefMq/BMS-Core.git
```

Next setup network configuration
```bash
cd BMS-Core
sudo cat ./configuration/network_setup >> /etc/networks/interfaces 
```

Then you should install pip and it's requirements
```bash
# install pip
sudo apt-get install -y python3-pip

# then install python requirements
sudo pip3 install -r requirements.txt
```

Setup homebridge:
```bash
sudo apt-get install -y homebridge
cd ~/.homebridge
ln -s /home/pi/BMS-Core/configurations/homebridge/config.json ./config.json
```

Next install crontabs. To do so use:
```bash
cd ~/BMS-Core
# This will update crontab file
crontab crontab_file

# Or alternatively edit crontab usin:
crontab -e
# Then add the content in the 'crontab_file' to the opened editor
```

Then turn-off and turn-on the device and everything should be up and running.
