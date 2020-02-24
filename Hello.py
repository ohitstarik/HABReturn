# Import DroneKit-Python
from dronekit import connect, VehicleMode, time
port = '/dev/ttyACM0'
# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (port))
# vehicle = connect('/dev/ttyAMA0', baud=57600,  wait_ready=True)
vehicle = connect(port, baud=921600, wait_ready=True)


# Get some vehicle attributes (state)
print "Get some vehicle attribute values:"
print " GPS: %s" % vehicle.gps_0
print " Battery: %s" % vehicle.battery
print " Last Heartbeat: %s" % vehicle.last_heartbeat
print " Is Armable?: %s" % vehicle.is_armable
print " System status: %s" % vehicle.system_status.state
print " Mode: %s" % vehicle.mode.name    # settable


# Close vehicle object before exiting script
vehicle.close()

print("Completed")