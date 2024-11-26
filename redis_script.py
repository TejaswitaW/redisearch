import redis

# Connect to Redis server (adjust host and port as needed)
client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# File paths
input_file_path = '/data/import_movies.redis'
temp_file_path = '/data/import_movies_temp.redis'

# Open the original file and create a temporary file for output
with open(input_file_path, 'r') as infile, open(temp_file_path, 'w') as outfile:
    for line in infile:
        command = line.strip()
        try:
            # Attempt to execute the command in Redis
            client.execute_command(command)
            # If successful, write the command to the new file
            outfile.write(command + '\n')
        except redis.exceptions.ResponseError as e:
            # If there's an error, log it or modify it
            print(f"Syntax error in line: {command}\nError: {e}")
            # Option 1: Remove the invalid line completely
            # Do nothing here; line won't be written to outfile
            
            # Option 2: Flag the invalid line with a comment
            # outfile.write(f"# Syntax error: {command} - {e}\n")

# Replace the original file with the modified temp file
import os
os.replace(temp_file_path, input_file_path)

print("File rewrite completed. Only valid commands are saved in the original file.")
