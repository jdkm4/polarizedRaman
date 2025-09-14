from pylablib.devices import Thorlabs
import time
import serial
import csv

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

data = []

angle = 0

while angle<=180:
    print("checking light")
    data.append([angle,photoCheck()])

    print("moving motor")
    with Thorlabs.ElliptecMotor("COM3") as stage:
        stage.set_default_addr(3)
        stage.move_by(10)
        
    angle += 10

with open('rightHandCircularToVertical.csv', 'w', newline='') as f:
    # 1. Create a csv.writer object
    writer = csv.writer(f)

    writer.writerows(data)

print("Done")