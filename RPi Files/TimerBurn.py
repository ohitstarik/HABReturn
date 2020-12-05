# Import DroneKit-Python
from dronekit import connect, VehicleMode, time
import RPi.GPIO as GPIO
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, 0)


port = '/dev/ttyUSB0'
# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (port))
# vehicle = connect('/dev/ttyAMA0', baud=57600,  wait_ready=True)
vehicle = connect(port, baud=921600, wait_ready=False)

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

print " ### BEGINNING BURN IN 5 SECONDS ###"

print " ### 5 ###"

time.sleep(1)

print " ### 4 ###"

time.sleep(1)

print " ### 3 ###"

time.sleep(1)

print " ### 2 ###"

time.sleep(1)

print " ### 1 ###"

time.sleep(1)

print " ### BEGINNING BURN ###"

GPIO.output(27, 1)
time.sleep(3)
GPIO.output(27, 0)
GPIO.cleanup()
print "Burn finished. Exiting"

# Close vehicle object before exiting script
vehicle.close()

print("Completed")
