"""
    WHEA Robotics 3881 vision program for FRC 2019
    Basic vision code for using two usb cameras
"""

from cscore import CameraServer

def main():
    cs = CameraServer.getInstance()
    cs.enableLogging()

    #Note that the cameras will be displayed as "USB Camera 0" or 1 in the dashboard
    usb1 = cs.startAutomaticCapture(dev=0) 
    usb2 = cs.startAutomaticCapture(dev=1)

    cs.waitForever()
