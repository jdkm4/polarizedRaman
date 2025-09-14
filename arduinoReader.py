import serial
import time

try:
    ser = serial.Serial('COM5', 9600, timeout=1)
    # A small delay to allow the serial port to initialize
    time.sleep(2) 
    print(f"Connected to Arduino on port {ser.name}")
except serial.SerialException as e:
    print(f"Error: Could not open port. {e}")
    exit()


last = [0]*100

try:
    while True:
        # Check if there is data waiting in the serial buffer
        if ser.in_waiting > 0:
            # Read one line from the serial port
            line = ser.readline()
            
            # The data comes in as bytes, so we need to decode it to a string
            # We also use .strip() to remove any leading/trailing whitespace or newline characters
            try:
                # Decode from bytes to utf-8 string and remove whitespace
                cleaned_line = line.decode('utf-8').strip()
                
                last.append(int(cleaned_line))
                last.pop(0)
                print(sum(last)/100)
                
            except (UnicodeDecodeError, ValueError):
                # Handle cases where the line is not valid UTF-8 or not a number
                # This can happen during startup or if the Arduino sends garbage data
                print(f"Could not parse line: {line}")

except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    # IMPORTANT: Always close the serial port when you're done
    if ser.is_open:
        ser.close()
        print("Serial port closed.")