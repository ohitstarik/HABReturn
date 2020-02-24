from dronekit import connect
port = '/dev/ttyUSB0'
# Connection shit goddamn please work
print("Connecting to vehicle on %s" % (port))
vehicle = connect(port, baud=921600, wait_ready=True)
print "LETS GOOOOO"
print "the shit connected bro thats whats up aight so lets get some data: "
print "Is the EKF okay: %s" % vehicle.ekf_ok
print "Vehicle's mode: %s" % vehicle.mode.name
print "Vehicle's Arm Status %s" % vehicle.armed 