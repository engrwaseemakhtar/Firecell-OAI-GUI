import tkinter as tk
import paramiko
import time
import csv
import re
import threading

# Global variable to store the subprocess
stop_thread = False

def ssh_command(host, port, username, password, csv_filename):
    global stop_thread
    try:
        # Create SSH client
        client = paramiko.SSHClient()

        # Automatically add untrusted hosts (make sure this is okay in your situation)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the host
        client.connect(hostname=host, port=port, username=username, password=password)

        # Start an interactive shell session
        channel = client.invoke_shell()

        # Read and discard the initial informational text
        while True:
            output = channel.recv(65535).decode('utf-8').strip()
            if 'Device:     RUTX50' in output or \
               '-----------------------------------' in output or \
               'gpsctl -t -i -x -u' in output or \
               ' gsmctl -q' in output or \
               'RSSI: ' in output or \
               'RSRP: ' in output or \
               'SINR: ' in output or \
               'RSRQ: ' in output or \
               'Kernel:  ' in output or \
               'Firmware:   ' in output:
                break

        # Start saving data to CSV
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['TIME_STAMP', 'LATITUDE', 'LONGITUDE', 'ACCURACY', 'TX', 'RX', 'RSSI', 'RSRP', 'SINR', 'RSRQ'])

            while not stop_thread:
                # Send the commands
                channel.send('gpsctl -t -i -x -u; gsmctl -e eth0 -r eth0 -q\n')  # all data
                time.sleep(0.04)  # Wait for the command to execute
                output_all = channel.recv(65535).decode('utf-8').strip()

                # Parse GPS data
                parsed_data_all = parse_output_gpsctl_t(output_all)

                # Write to CSV
                writer.writerow([
                    parsed_data_all.get('TIME_STAMP', ''),
                    parsed_data_all.get('LATITUDE', ''),
                    parsed_data_all.get('LONGITUDE', ''),
                    parsed_data_all.get('ACCURACY', ''),
                    parsed_data_all.get('TX', ''),
                    parsed_data_all.get('RX', ''),
                    parsed_data_all.get('RSSI', ''),
                    parsed_data_all.get('RSRP', ''),
                    parsed_data_all.get('SINR', ''),
                    parsed_data_all.get('RSRQ', '')
                ])

                # Flush the buffer to write to the file immediately
                csvfile.flush()

    except Exception as e:
        print(f"Error: {e}")

def parse_output_gpsctl_t(output_all):
    parsed_data = {}
    lines = output_all.split('\n')[:10]
    if len(lines) >= 6:
        parsed_data["TIME_STAMP"] = lines[1].strip()
        parsed_data["LATITUDE"] = lines[2].strip()
        parsed_data["LONGITUDE"] = lines[3].strip()
        parsed_data["ACCURACY"] = lines[4].strip()
        parsed_data["TX"] = lines[5].strip()
        parsed_data["RX"] = lines[6].strip()

    for line in output_all.split('\n'):
        if line.startswith("RSSI:") or line.startswith("RSRP:") or line.startswith("SINR:") or line.startswith("RSRQ:"):
            key, value = line.strip().split(": ", 1)
            parsed_data[key.strip()] = value.strip()
    print(parsed_data)

    return parsed_data

def start_ssh_command():
    global stop_thread
    stop_thread = False
    #host = host_entry.get()
    #port = int(port_entry.get())
    #username = username_entry.get()
    #password = password_entry.get()
    csv_filename = csv_filename_entry.get()
    
    thread = threading.Thread(target=ssh_command, args=(host, port, username, password, csv_filename))
    thread.start()

def stop_ssh_command():
    global stop_thread
    stop_thread = True

def main():
    global host, port, username, password, csv_filename_entry

    root = tk.Tk()
    root.title("SSH Command Runner")
    '''
    # Frame for Host input
    host_frame = tk.Frame(root)
    host_frame.pack(pady=5)
    tk.Label(host_frame, text="Host:").pack(side=tk.LEFT)
    host_entry = tk.Entry(host_frame)
    host_entry.pack(side=tk.LEFT)

    # Frame for Port input
    port_frame = tk.Frame(root)
    port_frame.pack(pady=5)
    tk.Label(port_frame, text="Port:").pack(side=tk.LEFT)
    port_entry = tk.Entry(port_frame)
    port_entry.pack(side=tk.LEFT)

    # Frame for Username input
    username_frame = tk.Frame(root)
    username_frame.pack(pady=5)
    tk.Label(username_frame, text="Username:").pack(side=tk.LEFT)
    username_entry = tk.Entry(username_frame)
    username_entry.pack(side=tk.LEFT)

    # Frame for Password input
    password_frame = tk.Frame(root)
    password_frame.pack(pady=5)
    tk.Label(password_frame, text="Password:").pack(side=tk.LEFT)
    password_entry = tk.Entry(password_frame, show="*")
    password_entry.pack(side=tk.LEFT)
    '''
    host = '192.168.1.1'
    port = 22
    username = 'root'  # Replace with your SSH username
    password = 'Firecell123456'
    
    # Frame for CSV Filename input
    csv_filename_frame = tk.Frame(root)
    csv_filename_frame.pack(pady=5)
    tk.Label(csv_filename_frame, text="CSV Filename:").pack(side=tk.LEFT)
    csv_filename_entry = tk.Entry(csv_filename_frame)
    csv_filename_entry.pack(side=tk.LEFT)

    # Frame for start and stop buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    start_button = tk.Button(button_frame, text="Start", command=start_ssh_command)
    start_button.pack(side=tk.LEFT, padx=10)
    stop_button = tk.Button(button_frame, text="Stop", command=stop_ssh_command)
    stop_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()

if __name__ == "__main__":
    main()

