import time
import serial
import csv
import matplotlib.pyplot as plt
from pylablib.devices import Thorlabs

# --- Configuration ---
# Easier to change settings here than digging through the code
ARDUINO_PORT = 'COM5'
MOTOR_PORT = 'COM3'
MOTOR_ADDRESS = 3  # The address of your Elliptec motor
BAUD_RATE = 9600
INITIAL_DELAY = 2  # Seconds to wait for Arduino to initialize
STEP_SIZE_DEGREES = 10
MAX_ANGLE = 180
SAMPLES_PER_POINT = 4 # How many readings to average from the photodiode
OUTPUT_FILENAME = 'rotation_data.csv'

def get_photodiode_reading(ser, num_samples):
    """
    Reads a specified number of lines from the Arduino, averages them, and returns the result.
    
    Args:
        ser (serial.Serial): The active and open serial connection to the Arduino.
        num_samples (int): The number of readings to take and average.
    
    Returns:
        float: The average of the readings, or 0.0 if readings fail.
    """
    total = 0
    readings_count = 0
    
    # Flush any old data out of the buffer before starting
    ser.reset_input_buffer()
    
    while readings_count < num_samples:
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                total += float(line)
                readings_count += 1
            except (UnicodeDecodeError, ValueError):
                # Ignore lines that can't be parsed and try again
                print(f"Warning: Could not parse line: {line}. Skipping.")
                
    return total / num_samples if num_samples > 0 else 0.0

def run_experiment():
    """
    Main function to run the rotation and measurement experiment.
    """
    collected_data = []
    
    print("--- Starting Experiment ---")
    print(f"Connecting to motor on {MOTOR_PORT} and Arduino on {ARDUINO_PORT}...")

    # The 'with' statements handle connecting and, crucially, disconnecting
    # automatically, even if an error occurs.
    # By nesting them, we ensure both are open before the loop starts.
    try:
        with Thorlabs.ElliptecMotor(MOTOR_PORT) as stage, \
             serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1) as ser:

            # --- One-Time Setup ---
            print("Devices connected. Performing initial setup.")
            stage.set_default_addr(MOTOR_ADDRESS)
            time.sleep(INITIAL_DELAY) # Give Arduino time to boot up properly once
            
            # --- Main Loop ---
            for angle in range(0, MAX_ANGLE + 1, STEP_SIZE_DEGREES):
                print(f"--- Angle: {angle}° ---")

                # 1. Take a measurement
                print("Measuring light intensity...")
                intensity = get_photodiode_reading(ser, SAMPLES_PER_POINT)
                print(f"Average Intensity: {intensity:.4f}")
                collected_data.append([angle, intensity])

                # 2. Move the motor for the next reading (if not the last step)
                if angle < MAX_ANGLE:
                    print(f"Moving motor by {STEP_SIZE_DEGREES}°...")
                    stage.move_by(STEP_SIZE_DEGREES)
                    # Optional: Add a small delay if the reading is unstable immediately after moving
                    time.sleep(0.1) 

    except serial.SerialException as e:
        print(f"FATAL ERROR: Could not connect to Arduino on {ARDUINO_PORT}. {e}")
        return None # Exit if we can't connect
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # The 'with' block will still ensure devices are closed properly
        return None

    print("\n--- Experiment Finished ---")
    return collected_data

def save_and_plot_data(data, filename):
    """Saves the data to a CSV and generates a scatter plot."""
    if not data:
        print("No data collected, cannot save or plot.")
        return

    # --- Save to CSV ---
    print(f"Saving data to {filename}...")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Angle (degrees)', 'Intensity (arbitrary units)']) # Write header
        writer.writerows(data)
    print("Save complete.")

    # --- Plot the data ---
    print("Generating plot...")
    # Unzip the data into separate lists for plotting
    angles = [row[0] for row in data]
    intensities = [row[1] for row in data]

    plt.figure(figsize=(10, 6)) # Create a nice-sized figure
    plt.scatter(angles, intensities, label='Measured Data')
    plt.title('Light Intensity vs. Rotation Angle')
    plt.xlabel('Angle (degrees)')
    plt.ylabel('Average Photodiode Reading')
    plt.grid(True)
    plt.xticks(range(0, MAX_ANGLE + 1, STEP_SIZE_DEGREES * 2)) # Set clear x-axis ticks
    plt.legend()
    
    # Display the plot. The script will pause here until you close the plot window.
    plt.show()


# --- Main execution block ---
if __name__ == "__main__":
    experimental_data = run_experiment()
    save_and_plot_data(experimental_data, OUTPUT_FILENAME)
    print("Done.")