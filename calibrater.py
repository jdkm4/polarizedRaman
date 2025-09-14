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
    while checks < 10:
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
                total += int(cleaned_line)
                checks += 1
                
            except (UnicodeDecodeError, ValueError):
                # Handle cases where the line is not valid UTF-8 or not a number
                # This can happen during startup or if the Arduino sends garbage data
                print(f"Could not parse line: {line}")
    if ser.is_open:
        ser.close()
        print("Serial port closed.")
    print("Total: " + str(total))
    return total

working = True

print("Finding minimum:")
minimum = photoCheck()

while working:
    print("Testing 90 deg")
    with Thorlabs.ElliptecMotor("COM3") as stage:
        stage.set_default_addr(1)
        moveBack = 0
        if stage.get_position() < 360:
            stage.move_by(90)
            moveBack = -90
        else:
            stage.move_by(-90)
            moveBack = 90
    
    if photoCheck() < 1.05*minimum:
        print("Done!!!")
        working = False
        
    else:
        print("Moving ELL")
        with Thorlabs.ElliptecMotor("COM3") as stage:
            stage.set_default_addr(1)
            stage.move_by(moveBack)
        with Thorlabs.ElliptecMotor("COM3") as stage:
            stage.set_default_addr(2)
            stage.move_by(2)
        with Thorlabs.KinesisPiezoMotor("97251742") as stage:
            print("Checking light")
            currentLight = photoCheck()
            
            if currentLight < minimum:
                minimum = currentLight

            while currentLight > minimum*1.05:
                print("Nudging PDR")
                stage.set_default_channel(3)
                stage.move_by(10)
                print("Checking light")
                currentLight = photoCheck()
                if currentLight < minimum:
                    minimum = currentLight
            print("Looks good")