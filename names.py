import csv
import time
import os

file_name = "names.csv"

# Check if the chosen file name exists
while os.path.exists(file_name):
    user_choice = input(f"The file {file_name} already exists. Do you want to overwrite it? (y/n): ").lower()

    if user_choice == 'y':
        break

    elif user_choice == 'n':
        file_name = input("Enter a new filename (or press Enter to exit): ").strip()
        if not file_name:
            exit()

    else:
        print("Invalid choice. Please enter 'y' or 'n'.")

# Create or open a CSV file for writing
csv_file = open(file_name, mode='w', newline='')
csv_writer = csv.writer(csv_file)

# Write the header row
csv_writer.writerow(["Name", "Elapsed Time (seconds)"])

# Get the start time when the program is initially run
start_time = time.time()
last_minute_checked = 0
name_count = 0

def save_name(name):
    # Calculate the elapsed time since the program started in minutes and seconds
    elapsed_time = round(time.time() - start_time, 2)
    minutes, seconds = divmod(int(elapsed_time), 60)

    # Write the name and elapsed time to the CSV file
    csv_writer.writerow([name, elapsed_time])

    # Print time elapsed message, if a minute barrier is passed
    global last_minute_checked
    if minutes > last_minute_checked:
        last_minute_checked = minutes
        print(f"{minutes} minute{'s' if minutes > 1 else ''} elapsed")

print("Enter a name (/x to exit)")

try:
    while True:
        user_input = input("name: ")

        if user_input == "/x":
            break

        name_count += 1
        save_name(user_input)

except KeyboardInterrupt:
    print('')

# Close the CSV file
csv_file.close()

print(f"{name_count} names saved to {file_name}")
