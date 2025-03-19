import csv

def process_data_to_csv(input_file, output_file):
    # Initialize variables
    tile_no = 1
    current_tile_data = {'Tile No': tile_no, 'Receiver 1': '', 'Receiver 2': '', 'Receiver 3': '', 'Human Status': '2'}

    # Open the output CSV file for writing
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Tile No', 'Receiver 1', 'Receiver 2', 'Receiver 3', 'Human Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Read the input file
        with open(input_file, 'r') as file:
            for line in file:
                line = line.strip()  # Remove leading/trailing whitespace
                if line.startswith("Receiver"):
                    receiver, value, timestamp = line.split(',')
                    if receiver == "Receiver_1":
                        current_tile_data['Receiver 1'] = value
                    elif receiver == "Receiver_2":
                        current_tile_data['Receiver 2'] = value
                    elif receiver == "Receiver_3":
                        current_tile_data['Receiver 3'] = value

                    # Check if all three receiver values are collected
                    if current_tile_data['Receiver 1'] and current_tile_data['Receiver 2'] and current_tile_data['Receiver 3']:
                        # Write the row to CSV with Tile No and Human Status
                        writer.writerow(current_tile_data)
                        print(f"Written to CSV: {current_tile_data}")  # Debugging
                        # Reset the receiver values for the next set of data
                        current_tile_data['Receiver 1'] = ''
                        current_tile_data['Receiver 2'] = ''
                        current_tile_data['Receiver 3'] = ''

                elif line.startswith("Move to next tile"):
                    tile_no += 1
                    current_tile_data['Tile No'] = tile_no  # Update tile number for the next set of values

    print(f"CSV file '{output_file}' has been created successfully.")

# Input and output file paths
input_file = 'SaveMovingData1.txt'  # Replace with your input file path
output_file = 'SaveMovingData1Output.txt'     # Replace with your desired output file path

# Process the data
process_data_to_csv(input_file, output_file)