# Import DroneKit-Python and other important joints
from dronekit import connect, VehicleMode, time
import RPi.GPIO as GPIO
import sys

# Init GPIO to cut cord
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, 0)

# Define values
burnAlt = 1
confirmationAlt = burnAlt - 1
condi = 1

# This is the port that the RPi0 will use to connect to the Pixhawk. The RPi connects to an FTDI adapter with usb, and the FTDI connects to the Pixhawk through the serial ports.
port = '/dev/ttyUSB0'

# Connect to Vehicle
print("Connecting to vehicle on: %s" % (port))
vehicle = connect(port, baud=921600, wait_ready=True)

# Download the vehicle waypoints (commands). Wait until download is complete. Necessary for home point check
cmds = vehicle.commands
cmds.download()
cmds.wait_ready()
home = vehicle.home_location #i aint typin all that up lmao

# Initial Vehicle state. Using this to decide if vehicle is healthy for flight
vehicle.armed = True
vehicle.mode = VehicleMode("MANUAL")
#while not vehicle.armed && vehicle.mode.name("MANUAL") == "MANUAL": # BACKBURNER, too lazy to look up syntax for this. Nice to have, good practice, not an absolute need. 
#	print 'Waiting until Vehicle is armed and in MANUAL mode'
#	time.sleep(1)

print "Get some vehicle attribute values:"
print " GPS: %s" % vehicle.gps_0
print " Battery: %s" % vehicle.battery
print " Is Armable?: %s" % vehicle.is_armable
print " System status: %s" % vehicle.system_status.state
print " Mode: %s" % vehicle.mode.name    # settable
print " Altitude: %s" % vehicle.location.global_relative_frame.alt
print " Home: %s" % home

while condi == 1:
	if vehicle.location.global_relative_frame.alt > burnAlt:
		vehicle.mode = VehicleMode("AUTO")
		while not vehicle.mode.name == "AUTO":
			print 'Waiting for AUTO mode.'
			time.sleep(1)
		print 'Vehicle in %s mode' % vehicle.mode.name
		print '##### BURN STARTED #####'
		GPIO.output(11, 1)
		while vehicle.location.global_relative_frame.alt > confirmationAlt:
			print 'Burning, Current Alt: %s Released Confirmation Alt: %s' % (vehicle.location.global_relative_frame.alt, confirmationAlt)
			time.sleep(1)
		GPIO.output(11, 0)
		GPIO.cleanup()
		print 'Burn finished. Vehicle in %s mode. Exiting' % vehicle.mode.name
		condi = 2
	else:
		print 'Current Alt: %s Burn Alt: %s' % (vehicle.location.global_relative_frame.alt, burnAlt)
		time.sleep(1)