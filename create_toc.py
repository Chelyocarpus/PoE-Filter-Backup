import string
import re
import secrets

# Function to generate a random string of 5 uppercase characters (letters and digits)
def generate_random_string(length=5):
    return ''.join(secrets.SystemRandom().choices(string.ascii_uppercase + string.digits, k=length))

# Function to remove the existing random string from the header
def remove_existing_random_string(header):
    return re.sub(r'\s*\[\w{5}\]$', '', header)

# Open the file in read mode
with open('Book of Wisdom.filter', 'r') as file:
    # Read all the lines in the file
    lines = file.readlines()

# Initialize a dictionary to store the headers and their associated random strings
header_dict = {}

# Loop through each line in the file
for i in range(len(lines)):
    # Check if the line starts with the search string
    if lines[i].startswith('#======================================================================'):
        # Extract the header name from the line below it
        header_name = lines[i-1].strip()
        # Remove existing random string if present
        header_name_clean = remove_existing_random_string(header_name)
        # Generate a new random string and store it with the header
        if header_name_clean:
            header_dict[header_name_clean] = f"{header_name_clean} [{generate_random_string()}]"

# Write the modified headers to the output file
with open('create_toc_output.txt', 'w') as output_file:
    for original_header, modified_header in header_dict.items():
        output_file.write(modified_header + '\n')

# Update the input file with the modified headers
with open('Book of Wisdom.filter', 'w') as file:
    for i in range(len(lines)):
        if lines[i].startswith('#======================================================================'):
            header_name = lines[i-1].strip()
            header_name_clean = remove_existing_random_string(header_name)
            if header_name_clean in header_dict:
                # Replace the original header with the modified header
                lines[i-1] = header_dict[header_name_clean] + '\n'
    # Write the updated lines back to the file
    file.writelines(lines)
