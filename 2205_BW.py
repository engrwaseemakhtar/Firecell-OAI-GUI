import tkinter as tk
import subprocess
import signal
import os

# Global variable to store the subprocess
process = None

def execute_command_verbose(receiver_ip, port):
    global process
    process = subprocess.Popen(["./scream-master/bin/scream_bw_test_tx", "-verbose", receiver_ip, port])

def execute_command_log(receiver_ip, port):
    global process
    process = subprocess.Popen(["./scream-master/bin/scream_bw_test_tx", "-log", "MWA_Demo.csv", "-itemlist", receiver_ip, port])

def execute_command_key(receiver_ip, port):
    global process
    process = subprocess.Popen(["./scream-master/bin/scream_bw_test_tx", "-key", "2", "10", receiver_ip, port])

def execute_command_minrate(receiver_ip, port):
    global process
    process = subprocess.Popen(["./scream-master/bin/scream_bw_test_tx", "-minrate", "2000", receiver_ip, port])

def execute_command_maxrate(receiver_ip, port):
    global process
    process = subprocess.Popen(["./scream-master/bin/scream_bw_test_tx", "-maxrate", "20000", receiver_ip, port])

def execute_command_delaytarget(receiver_ip, port):
    global process
    process = subprocess.Popen(["./scream-master/bin/scream_bw_test_tx", "-delaytarget", "0.05", receiver_ip, port])

# Mapping command options to corresponding functions
commands = {
    "-verbose": execute_command_verbose,
    "-log": execute_command_log,
    "-key": execute_command_key,
    "-minrate": execute_command_minrate,
    "-maxrate": execute_command_maxrate,
    "-delaytarget": execute_command_delaytarget
}

def start_script():
    receiver_ip = ip_entry.get()
    port = port_entry.get()
    command_option = command_var.get()

    if command_option not in commands:
        print("Invalid command option")
        return

    # Execute the corresponding function based on the command option
    commands[command_option](receiver_ip, port)

def stop_script():
    global process
    if process:
        process.terminate()
        process = None
        print("Script stopped")

def terminate_script():
    global process
    if process:
        process.send_signal(signal.SIGINT)
        #process = None
        os._exit(0)
        print("Script terminated")

def main():
    global ip_entry, port_entry, command_var

    root = tk.Tk()
    root.title("Script Runner")

    # Frame for IP address input
    ip_frame = tk.Frame(root)
    ip_frame.pack(pady=10)
    tk.Label(ip_frame, text="Receiver IP Address:").pack(side=tk.LEFT)
    ip_entry = tk.Entry(ip_frame)
    ip_entry.pack(side=tk.LEFT)

    # Frame for Port number input
    port_frame = tk.Frame(root)
    port_frame.pack(pady=10)
    tk.Label(port_frame, text="Port Number:").pack(side=tk.LEFT)
    port_entry = tk.Entry(port_frame)
    port_entry.pack(side=tk.LEFT)

    # Frame for Command option input
    command_frame = tk.Frame(root)
    command_frame.pack(pady=10)
    tk.Label(command_frame, text="Command Option:").pack(side=tk.LEFT)
    command_var = tk.StringVar()
    command_menu = tk.OptionMenu(command_frame, command_var, *commands.keys())
    command_menu.pack(side=tk.LEFT)

    # Frame for start button
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    start_button = tk.Button(button_frame, text="Start Script", command=start_script)
    start_button.pack(side=tk.LEFT, padx=10)

    # Frame for stop button
    stop_button = tk.Button(button_frame, text="Stop Script", command=stop_script)
    stop_button.pack(side=tk.LEFT, padx=10)

    # Frame for terminate button
    terminate_button = tk.Button(button_frame, text="Terminate", command=terminate_script)
    terminate_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()

if __name__ == "__main__":
    main()

