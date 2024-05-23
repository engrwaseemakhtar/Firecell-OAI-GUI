import tkinter as tk
from tkinter import ttk
import subprocess
import os
import signal

class FiveGSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("5G Simulation GUI-Waseem")
        self.processes = {}  # Dictionary to store running processes

        # Calculate screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set the size of the window to fit all frames within the screen
        window_width = int(screen_width / 3)
        window_height = int(screen_height)
        self.root.geometry(f"{window_width}x{window_height}+{screen_width//4}+{screen_height//4}")

        ##---------------------------------------------------------------------------------------------##
        ##--------------------Create a frame for gNB test controls-----------------------------------##
        ##---------------------------------------------------------------------------------------------##
        self.gnb_ue_frame = ttk.LabelFrame(self.root, text="gNB and UE Control")
        self.gnb_ue_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        ttk.Label(self.gnb_ue_frame, text="Band:").grid(row=0, column=0, padx=5, pady=5)
        self.band_var = tk.StringVar()
        self.band_entry = ttk.Entry(self.gnb_ue_frame, textvariable=self.band_var)
        self.band_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.gnb_ue_frame, text="Frequency:").grid(row=1, column=0, padx=5, pady=5)
        self.freq_var = tk.StringVar()
        self.freq_entry = ttk.Entry(self.gnb_ue_frame, textvariable=self.freq_var)
        self.freq_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.gnb_ue_frame, text="PRBs:").grid(row=2, column=0, padx=10, pady=10)
        self.prbs_var = tk.StringVar()
        self.prbs_entry = ttk.Entry(self.gnb_ue_frame, textvariable=self.prbs_var)
        self.prbs_entry.grid(row=2, column=1, padx=5, pady=5)

        self.start_gnb_ue_btn = ttk.Button(self.gnb_ue_frame, text="Start gNB & UE", command=self.start_gnb_ue, style="Green.TButton")
        self.start_gnb_ue_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)
        self.stop_gnb_ue_btn = ttk.Button(self.gnb_ue_frame, text="Stop gNB & UE", command=self.stop_gnb_ue, style="Red.TButton", state=tk.DISABLED)
        self.stop_gnb_ue_btn.grid(row=3, column=2, columnspan=2, padx=20, pady=20)

        ##---------------------------------------------------------------------------------------------##
        ##--------------------Create a frame for TWAMP test controls-----------------------------------##
        ##---------------------------------------------------------------------------------------------##
        self.twamp_control_frame = ttk.LabelFrame(self.root, text="TWAMP Test Controls")
        self.twamp_control_frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.NSEW)
        
        self.start_twamp_btn = ttk.Button(self.twamp_control_frame, text="Start TWAMP Test", command=self.start_twamp_test, style="Green.TButton")
        self.start_twamp_btn.grid(row=2, column=0, padx=20, pady=20)
        '''
        ttk.Label(self.twamp_control_frame, text="Receiver's IP:").grid(row=1, column=0, padx=5, pady=5)
        self.twamp_ip_var = tk.StringVar()
        self.twamp_ip_entry = ttk.Entry(self.twamp_control_frame, textvariable=self.twamp_ip_var)
        self.twamp_ip_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.twamp_control_frame, text="Port #:").grid(row=1, column=2, padx=5, pady=5)
        self.twamp_port_var = tk.StringVar()
        self.twamp_port_entry = ttk.Entry(self.twamp_control_frame, textvariable=self.twamp_port_var)
        self.twamp_port_entry.grid(row=1, column=3, padx=10, pady=10)
        '''
        self.stop_twamp_btn = ttk.Button(self.twamp_control_frame, text="Stop TWAMP Test", command=self.stop_twamp_test, style="Red.TButton", state=tk.DISABLED)
        self.stop_twamp_btn.grid(row=2, column=3, padx=20, pady=20)

        ##---------------------------------------------------------------------------------------------##
        ##--------------------Create a frame for BW test controls-----------------------------------##
        ##---------------------------------------------------------------------------------------------##
        self.bw_control_frame = ttk.LabelFrame(self.root, text="BW Test Controls")
        self.bw_control_frame.grid(row=2, column=0, padx=10, pady=10, sticky=tk.NSEW)

        self.start_bw_btn = ttk.Button(self.bw_control_frame, text="Start BW Test", command=self.start_bw_test, style="Green.TButton")
        self.start_bw_btn.grid(row=2, column=0, padx=20, pady=20)
        '''
        ttk.Label(self.bw_control_frame, text="Receiver's IP:").grid(row=0, column=0, padx=5, pady=5)
        self.bw_ip_var = tk.StringVar()
        self.bw_ip_entry = ttk.Entry(self.bw_control_frame, textvariable=self.bw_ip_var)
        self.bw_ip_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.bw_control_frame, text="Port #:").grid(row=0, column=2, padx=5, pady=5)
        self.bw_port_var = tk.StringVar()
        self.bw_port_entry = ttk.Entry(self.bw_control_frame, textvariable=self.bw_port_var)
        self.bw_port_entry.grid(row=0, column=3, padx=10, pady=10)
        
        ttk.Label(self.bw_control_frame, text="Select test:").grid(row=1, column=0, padx=10, pady=10)
        self.bw_testtype_var = tk.StringVar()
        self.bw_testtype_entry = ttk.Entry(self.bw_control_frame, textvariable=self.bw_testtype_var)
        self.bw_testtype_entry.grid(row=1, column=1, padx=10, pady=10) 
        '''       

        self.stop_bw_btn = ttk.Button(self.bw_control_frame, text="Stop BW Test", command=self.stop_bw_test, style="Red.TButton", state=tk.DISABLED)
        self.stop_bw_btn.grid(row=2, column=3, padx=20, pady=20)

        ##---------------------------------------------------------------------------------------------##
        ##--------------------Create a frame for Teltonika test controls-----------------------------------##
        ##---------------------------------------------------------------------------------------------##
        self.teltonika_control_frame = ttk.LabelFrame(self.root, text="Teltonika State Controls")
        self.teltonika_control_frame.grid(row=3, column=0, padx=10, pady=10, sticky=tk.NSEW)

        self.start_teltonika_btn = ttk.Button(self.teltonika_control_frame, text="Start Getting States for Teltonika Router", command=self.start_teltonika, style="Green.TButton")
        self.start_teltonika_btn.grid(row=0, column=0, padx=20, pady=20)
        self.stop_teltonika_btn = ttk.Button(self.teltonika_control_frame, text="Stop Getting States for Teltonika Router", command=self.stop_teltonika, style="Red.TButton", state=tk.DISABLED)
        self.stop_teltonika_btn.grid(row=0, column=3, padx=20, pady=20)

    def start_gnb_ue(self):
        # Example command for starting gNB and UE
        band = self.band_var.get()
        freq = self.freq_var.get()
        prbs = self.prbs_var.get()
        print(f"Starting gNB and UE with Band: {band}, Frequency: {freq}, PRBs: {prbs}")
        # Add subprocess or appropriate code to start gNB and UE

    def stop_gnb_ue(self):
        # Example command for stopping gNB and UE
        print("Stopping gNB and UE")

    def start_twamp_test(self):
        print("Starting TWAMP test...")
        script_path = "/home/waseem/Documents/Teltonika States/twamp.py"
        self._start_script("twamp_test", script_path)

    def stop_twamp_test(self):
        print("Stopping TWAMP test")
        self._stop_script("twamp_test")

    def start_bw_test(self):
        print("Starting BW test...")
        script_path = "/home/waseem/Documents/Teltonika States/2205_BW.py" #MWA_BWTest.py
        self._start_script("bw_test", script_path)

    def stop_bw_test(self):
        print("Stopping BW test")
        self._stop_script("bw_test")

    def start_teltonika(self):
        print("Starting Getting States for Teltonika Router...")
        script_path = "/home/waseem/Documents/Teltonika States/gpsgsmstates.py"
        self._start_script("teltonika", script_path)

    def stop_teltonika(self):
        print("Stopping Getting States for Teltonika Router")
        self._stop_script("teltonika")

    def _start_script(self, key, script_path):
        try:
            process = subprocess.Popen(["python3", script_path], preexec_fn=os.setsid)
            self.processes[key] = process
            self._update_buttons(key, start=False)
        except Exception as e:
            print(f"Error starting {key} script: {e}")

    def _stop_script(self, key):
        process = self.processes.get(key)
        if process:
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGINT)
                process.wait(timeout=5)
                if process.poll() is None:
                    process.terminate()
                    process.wait(timeout=5)
                if process.poll() is None:
                    process.kill()
                    process.wait(timeout=5)
                self._update_buttons(key, start=True)
            except Exception as e:
                print(f"Error stopping {key} script: {e}")

    def _update_buttons(self, key, start):
        if key == "twamp_test":
            self.start_twamp_btn.config(state=tk.NORMAL if start else tk.DISABLED)
            self.stop_twamp_btn.config(state=tk.DISABLED if start else tk.NORMAL)
        elif key == "bw_test":
            self.start_bw_btn.config(state=tk.NORMAL if start else tk.DISABLED)
            self.stop_bw_btn.config(state=tk.DISABLED if start else tk.NORMAL)
        elif key == "teltonika":
            self.start_teltonika_btn.config(state=tk.NORMAL if start else tk.DISABLED)
            self.stop_teltonika_btn.config(state=tk.DISABLED if start else tk.NORMAL)

def main():
    root = tk.Tk()
    app = FiveGSimulatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

