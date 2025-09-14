from pylablib.devices import Thorlabs
import time
import math
import serial

def photoCheck():
    try:
        ser = serial.Serial('COM5', 9600, timeout=1)
        # A small delay to allow the serial port to initialize
        time.sleep(2) 
        print(f"Connected to Arduino on port {ser.name}")
    except serial.SerialException as e:
        print(f"Error: Could not open port. {e}")
        exit()

    checks = 0
    total = 0
    while checks < 4:
        # Check if there is data waiting in the serial buffer
        if ser.in_waiting > 0:
            # Read one line from the serial port
            line = ser.readline()
            
            # The data comes in as bytes, so we need to decode it to a string
            # We also use .strip() to remove any leading/trailing whitespace or newline characters
            try:
                # Decode from bytes to utf-8 string and remove whitespace
                cleaned_line = line.decode('utf-8').strip()
                
                print(cleaned_line)
                total += float(cleaned_line)
                checks += 1
                
            except (UnicodeDecodeError, ValueError):
                # Handle cases where the line is not valid UTF-8 or not a number
                # This can happen during startup or if the Arduino sends garbage data
                print(f"Could not parse line: {line}")
    print("Total: " + str(total))
    return total

working = True

print("Finding minimum:")
minimum = photoCheck()

a = 30
b = 0

print("Setting up QWPs")
with Thorlabs.ElliptecMotor("COM3") as stage:
    stage.set_default_addr(1)
    stage.move_by(b)
    stage.set_default_addr(2)
    stage.move_by(b)

with Thorlabs.KinesisPiezoMotor("97251668") as stage:
    stage.set_default_channel(3)
    stage.move_by(b*20)
    lastThree = 10000
    lastTwo = 10000
    lastOne = 10000
    while True:
        currentLight = photoCheck()
            
        if currentLight <= minimum:
            minimum = currentLight
        if currentLight <= minimum*1.05 or (currentLight >= lastOne and lastOne >= lastTwo and lastTwo >= lastThree):
            print("QWPs set up")
            break
        else: 
            stage.move_by(min(10,math.ceil(10*(currentLight-minimum))))
        
        lastThree = lastTwo
        lastTwo = lastOne
        lastOne = currentLight
        
        

print("Setting up hwps")
with Thorlabs.ElliptecMotor("COM3") as stage:
    stage.set_default_addr(2)
    stage.move_by(-a)

with Thorlabs.KinesisPiezoMotor("97251668") as stage:
    stage.set_default_channel(2)
    stage.move_by(a*20)
    lastThree = 10000
    lastTwo = 10000
    lastOne = 10000
    while True:
        currentLight = photoCheck()

        if currentLight <= minimum:
            minimum = currentLight
        if currentLight <= minimum*1.05 or (currentLight >= lastOne and lastOne >= lastTwo and lastTwo >= lastThree):
            print("HWPs set up")
            break
        else: 
            stage.move_by(min(10,math.ceil(10*(currentLight-minimum))))
        
        lastThree = lastTwo
        lastTwo = lastOne
        lastOne = currentLight
          


serial.Serial('COM5', 9600, timeout=1).close()