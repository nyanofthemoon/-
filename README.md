# 0M

Contributing to the Vector community! This framework allows cuztomizing the robot to one's own flavor by creating stackable skills responding to multiple sensory data.

"All life begins with Nu and ends with Nu. This is the truth! This is my belief! ...At least for now."
— "The Mystery of Life," vol. 841, chapter 26

## Installation

### Hardware Dependencies
- [Vector](https://www.anki.com/en-us/vector) robot
- [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b)
  - [Sense HAT](https://www.raspberrypi.org/products/sense-hat) add-on board
  - GPS module for Pi USB port
  - Bluetooth module for Pi USB port

### Software Dependencies
- [Python 3.6.6+](https://www.python.org/downloads)
- [Redis 4.0](https://redis.io/download)
- [Vector SDK](https://developer.anki.com/vector/docs/initial.html#initial)
  - Follow SDK installation process
  - Follow Vector Authentication process
    - Keep provided secrets for configuration in a later step

### Local
- Go to cloned project's root directory
- `cd nu`
- `python setup.py install` or `python -m pip install missing_dependency`
- `git clone git@github.com:anki/vector-python-sdk.git`
- Configure `configs/nu.ini`'s `sdk` section with obtained secrets

### Docker
- Coming soon!

### Raspberry Pi 3
- Clone project into directory `/home/pi`
- `cd /home/pi/0M/nu`
- `python setup.py install` or `python -m pip install missing_dependency`
- `git clone git@github.com:anki/vector-python-sdk.git`
- `cp /home/pi/0M/nu/configs/init.d/0M /etc/init.d`
- Configure `configs/nu.ini`'s `sdk` section with obtained secrets

## Usage 

### Local
- Place Vector on the charger
- Launch Redis using `redis-server`
- `cd` unto 0M project directory
- Launch project in foreground mode
  - normal `python -m nu`
  - verbose `python -m nu -v`
  - very verbose `python -m nu -vv`
- Launch project in background mode
  - silent mode `python -m nu &`
  - silent log mode
    - normal `python -m nu 2>&1 >& /tmp/0M-normal.txt &`
    - verbose `python -m nu -v 2>&1 >& /tmp/0M-verbose.txt &`
    - very verbose `python -m nu -v 2>&1 >& /tmp/0M-very-verbose.txt &`
    
### Docker
- Coming soon!

### Raspberry Pi 3
- Place Vector on the charger
- Launch Redis using `systemctl start redis-server`
- Launch project using `systemctl start 0M`
- Stop using `systemctl stop 0M`

