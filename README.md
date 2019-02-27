# HeimdallMUltiwii Package

### MUltiwii communication package


This is a Multiwii communication package (for Python 3.6) for send/receive data from/to FCBs (Flight Controller Boards)

The main approach of this package is abstract all complex stuff and worry only for ask him only what you need.


##### Install (pypi Test Index):

```
pip install -i https://test.pypi.org/simple/ HeimdallMultiwii
```

##### Super Simple Example
```
#!/usr/bin/env python3
from HeimdallMultiwii import

droneFCB = comm.Adapter('/dev/ttyUSB0') #  default baudrate 115200
# OR your custom baudrate                           vvvvv
# droneFCB = comm.Adapter('/dev/ttyUSB0', baud_rate=56000)
droneFCB.connect()
if droneFCB.can_fly():
    print(droneFCB.get_ident())
    print(droneFCB.get_status())
    print(droneFCB.get_rawimu())
    print(droneFCB.get_servo())
    droneFCB.disconnect()

```

For Use Serial ports without problems include your user in dialout group:
```
bash
$ usermod -a -G dialout MY_USER_NAME
```
then LogOff or Reboot.

----

The package is in active development and you can find it in the Pypi test site. Comming soon in real Pypi

####Pending:
+ Multiwii MSP
    * Map all MSP MultiWii FCB responses
    * Send RC commands to FCB
+ Misc
    * Make it ThreadSafe


HeimdallMultiwii package test index [HeimdallMultiwii](https://test.pypi.org/project/HeimdallMultiwii/). 

Please Use it and leave a comment.