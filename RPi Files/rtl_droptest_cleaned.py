#!/usr/bin/env python3
from dronekit import connect, mavutil, VehicleMode, time
import RPi.GPIO as GPIO
import sys
GPIO.setmode(GPIO.BOARD)

# Init GPIO to cut cord
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE   = 921600
BURN_PIN = 13

ALT_SAMPLE_INTERVAL = 10  # sampling reference altitude (seconds)
FALL_THRESH  = -5 # threshold to force RTL if falling (meters)

# Define values
burnAlt = 75
confirmationAlt = burnAlt - 2
condi = 1

GPIO.setwarnings(False)
GPIO.setup(BURN_PIN, GPIO.OUT)
GPIO.output(BURN_PIN, GPIO.LOW)

# Connect to Vehicle
print("Connecting to vehicle on: %s" % (SERIAL_PORT))
vehicle = connect(SERIAL_PORT, wait_ready=False, baud=BAUD_RATE)
time.sleep(10)

# Download the vehicle waypoints (commands). Wait until download is complete. Necessary for home point check
cmds = vehicle.commands
cmds.download()
cmds.wait_ready()
time.sleep(10)
vehicle.home_location = vehicle.location.global_frame
home = vehicle.home_location #i aint typin all that up lmao
print "HOME: ", home
print "CURRENT LOCATION: ", vehicle.location.global_frame
print "FLIGHT MODE: ", vehicle.mode.name

# Initial Vehicle state. Using this to decide if vehicle is healthy for flight
vehicle.armed = True
vehicle.mode = VehicleMode("MANUAL")

# Check if above worked
while not vehicle.armed and vehicle.mode.name == "MANUAL":
	print("Waiting until Vehicle is armed and in MANUAL mode")
	time.sleep(1)
print("ARM STATUS: ", vehicle.armed, vehicle.is_armable)

# Disarm vehicle for logging reasons
vehicle.armed = False

reference_altitude = vehicle. location.global_frame.alt

print("Get some vehicle attribute values:")
print(" GPS: %s" % vehicle.gps_0)
print(" System status: %s" % vehicle.system_status.state)
print(" Mode: %s" % vehicle.mode.name)   

count = 0
while condi == 1:
        if vehicle.location.global_relative_frame.alt > burnAlt or (vehicle.location.global_frame.alt - reference_altitude) < FALL_THRESH:

        	# Denoting that the cut was due to
            if(vehicle.location.global_frame.alt - reference_altitude) < FALL_THRESH:
               print("\n\nERROR: UNINTENDED DESCENT. PACK IT UP BOYS.\n")
               confirmationAlt = vehicle.location.global_relative_frame.alt - 1
            vehicle.mode = VehicleMode("AUTO")
            GPIO.output(BURN_PIN, GPIO.HIGH)

            while not vehicle.mode.name == "AUTO":
            	print('Waiting for AUTO mode.')
            	time.sleep(1)
            print('Vehicle in %s mode' % vehicle.mode.name)
            print('##### BURN STARTED #####')
            GPIO.output(BURN_PIN, GPIO.HIGH)
            while vehicle.location.global_relative_frame.alt > confirmationAlt:
                print('Burning, Current Alt: %s Released Confirmation Alt: %s' % (vehicle.location.global_relative_frame.alt, confirmationAlt))
                time.sleep(1)
            GPIO.output(BURN_PIN, GPIO.LOW)
            GPIO.cleanup()
            print('Burn finished. Vehicle in %s mode. Exiting' % vehicle.mode.name)
            condi = 2
        else:
                print('Current Alt: %s Burn Alt: %s' % (vehicle.location.global_relative_frame.alt, burnAlt))
                time.sleep(1)
                if count > ALT_SAMPLE_INTERVAL:
                    count = 0
                    reference_altitude = vehicle.location.global_frame.alt
                count += 1
