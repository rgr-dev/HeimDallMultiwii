# HeimdallMUltiwii Package

### MUltiwii communication package


This is a Multiwii communication package (for Python 3.6) for send/receive data from/to FCBs (Flight Controller Boards) with **Miltiwii v2.3** Firmware (Old I know...)

The main approach of this package is abstract all complex stuff and worry only for ask him only what you need.

As i said, the firmware Miltiwii is Old i know, but this project is a TOC before a more ambitious project.

A couple of messages was changed for my purposes, these message (And changes) are:

+ MSP_RAW_IMU
    * The estructure of this message changes, 
    * If you need this message just like that, add a change in your MultiWii Firmware(**). **Or** simply uncomment line 7 and comment line 8 in constants.py file and calls the method **get_original_rawimu()** in comm.py file. The original Multiwii message will return.
+ MSP_ATTITUDE
    * Have a change that parse the **angx** to clockWise degrees (I need parse to Radians in clockwise too for use in a Widget [Transform.rotate](https://docs.flutter.io/flutter/widgets/Transform/Transform.rotate.html)).
    * Yo can use the original message without parsed data. Just call the method get_original_attitude() in comm.py file. 

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
###### Calibrate ACC and MAG
```
droneFCB.ACC_calibration()
droneFCB.MAG_calibration()
```

###### Arm/Disarm and Send RCSignals over serial protocol
```
#  Arm 
droneFCB.drone_ARM()

#  Disarm
droneFCB.drone_DISARM()

#  Send RC signal example: [ROLL, PITCH, YAW, THROTTLE]
droneFCB.send_rc_signal([1500, 1500, 1500, 1000])
```
When the drone is fliying you can read IMU metrics using:
```
#  Only if you have MiltiWii Firmware modified (See (**) section at the README.md)
droneFCB.get_rawimu()
```


For Use Serial ports without problems include your user in dialout group:
```
bash
$ usermod -a -G dialout MY_USER_NAME
```
then LogOff or Reboot.

----

####(**) Changes in MiltiWii 2.3 Firmware ()Protocol.cpp file):

add the methods:

```c++
void  s_structwithouthead(uint8_t *cb,uint8_t siz) {
    while(siz--) serialize8(*cb++);
}

void s_struct_w_custom(uint8_t *cb,uint8_t siz) {
    while(siz--) *cb++ = read8();
}
```
Replace the next case switch contents:
```c++
   case MSP_SET_RAW_RC:
     s_struct_w((uint8_t*)&rcSerial,16);
     rcSerialCount = 50; // 1s transition 
     break;
```
and
```c++
   case MSP_RAW_IMU:
     #if defined(DYNBALANCE)
       for(uint8_t axis=0;axis<3;axis++) {imu.gyroData[axis]=imu.gyroADC[axis];imu.accSmooth[axis]= imu.accADC[axis];} // Send the unfiltered Gyro & Acc values to gui.
     #endif 
     s_struct((uint8_t*)&imu,18);
     break;
```
For
```c++
   case MSP_SET_RAW_RC:
     s_struct_w_custom((uint8_t*)&rcSerial,16);
     headSerialReply(28);
     s_structwithouthead((uint8_t*)&imu,18);
     serialize32(GPS_coord[LAT]);
     serialize32(GPS_coord[LON]);
     serialize16(GPS_altitude);
     rcSerialCount = 50; // 1s transition 
     break;
```
and
```c++
   case MSP_RAW_IMU:
     #if defined(DYNBALANCE)
       for(uint8_t axis=0;axis<3;axis++) {imu.gyroData[axis]=imu.gyroADC[axis];imu.accSmooth[axis]= imu.accADC[axis];} // Send the unfiltered Gyro & Acc values to gui.
     #endif
     headSerialReply(28);
     s_structwithouthead((uint8_t*)&imu,18);
     serialize32(GPS_coord[LAT]);
     serialize32(GPS_coord[LON]);
     serialize16(GPS_altitude);
     break;
```

You can use the unit test files for guide. Look inside **test/** directory

The package is in active development and you can find it in the Pypi test site. Comming soon in real Pypi

####Pending:
+ Multiwii MSP
    * intermittent problem reads get_rawimu() when are flying. 
+ Misc
    * Make it ThreadSafe


HeimdallMultiwii package test index [HeimdallMultiwii](https://test.pypi.org/project/HeimdallMultiwii/). 

Please Use it and leave a comment.