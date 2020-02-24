# Import DroneKit-Python
from dronekit import connect, VehicleMode, time
import RPi.GPIO as GPIO
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, 0)


port = '/dev/ttyUSB0'
# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (port))
# vehicle = connect('/dev/ttyAMA0', baud=57600,  wait_ready=True)
vehicle = connect(port, baud=921600, wait_ready=True)

# Get some vehicle attributes (state)
print "Get some vehicle attribute values:"
print " GPS: %s" % vehicle.gps_0
#print " Battery: %s" % vehicle.battery
#print " Last Heartbeat: %s" % vehicle.last_heartbeat
print " Is Armable?: %s" % vehicle.is_armable
#print " System status: %s" % vehicle.system_status.state
print " Mode: %s" % vehicle.mode.name    # settable
#print " Attitude: %s" % vehicle.attitude
print " Altitude: %s" % vehicle.location.global_relative_frame.alt
print " Home: %s" % vehicle.home_location

vehicle.armed = True
while not vehicle.armed:
	time.sleep(1)


vehicle.mode = VehicleMode("AUTO")

while not vehicle.mode.name == "AUTO":
	print 'Waiting for AUTO mode.'
	time.sleep(1)


#altitude averaging code <--- need this in the new 
homeAlt = 0
x=0
while x < 10:
	homeAlt += vehicle.location.global_relative_frame.alt
	x+=1
	print "homeAlt iteration %s is %s " % (x, homeAlt)
	time.sleep(1)


avgHomeAlt = (homeAlt / 10)
trueHomeAlt = 0

print avgHomeAlt

burstAlt = 1
releaseAlt = burstAlt - .5

condi = 1
height = vehicle.location.global_relative_frame.alt - avgHomeAlt


while condi == 1:
	if height > burstAlt:
		print 'Burn Started.'
		GPIO.output(11, 1)
		while height > releaseAlt:
			height = vehicle.location.global_relative_frame.alt - avgHomeAlt
			print 'Home Alt: %s Current Alt: %s' % (trueHomeAlt, height)
			time.sleep(1)
		GPIO.output(11, 0)
		GPIO.cleanup()
		print 'Burn finished. Exiting'
		condi = 2
	else:
		height = vehicle.location.global_relative_frame.alt - avgHomeAlt
		print 'Home Alt: %s Current Alt: %s' % (trueHomeAlt, height)
		time.sleep(1)

vehicle.mode = VehicleMode("MANUAL")

# Close vehicle object before exiting script
vehicle.close()

print("Completed")
