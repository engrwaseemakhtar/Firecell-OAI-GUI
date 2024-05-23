import tkinter as tk
from tkinter import ttk
import subprocess
#import os
#import signal
#import time

class FiveGSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("5G Simulation GUI")

        # Calculate screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set the size of the window to fit all frames within the screen
        window_width = int(screen_width / 3)
        window_height = int(screen_height )
        self.root.geometry(f"{window_width}x{window_height}+{screen_width//4}+{screen_height//4}")

        ##---------------------------------------------------------------------------------------------##
        ##--------------------Create a frame for gNB test controls-----------------------------------##
        ##---------------------------------------------------------------------------------------------##
        # Create a frame for gNB and UE control
        self.gnb_ue_frame = ttk.LabelFrame(self.root, text="gNB and UE Control")
        self.gnb_ue_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)  # Use sticky=tk.NSEW for frame resizing

        # Band selection
        ttk.Label(self.gnb_ue_frame, text="Band:").grid(row=0, column=0, padx=5, pady=5)
        self.band_var = tk.StringVar()
        self.band_entry = ttk.Entry(self.gnb_ue_frame, textvariable=self.band_var)
        self.band_entry.grid(row=0, column=1, padx=10, pady=10)

        # Frequency input
        ttk.Label(self.gnb_ue_frame, text="Frequency:").grid(row=1, column=0, padx=5, pady=5)
        self.freq_var = tk.StringVar()
        self.freq_entry = ttk.Entry(self.gnb_ue_frame, textvariable=self.freq_var)
        self.freq_entry.grid(row=1, column=1, padx=10, pady=10)

        # PRBs input
        ttk.Label(self.gnb_ue_frame, text="PRBs:").grid(row=2, column=0, padx=10, pady=10)
        self.prbs_var = tk.StringVar()
        self.prbs_entry = ttk.Entry(self.gnb_ue_frame, textvariable=self.prbs_var)
        self.prbs_entry.grid(row=2, column=1, padx=5, pady=5)

        # Start/Stop gNB and UE buttons
        self.start_gnb_ue_btn = ttk.Button(self.gnb_ue_frame, text="Start gNB & UE", command=self.start_gnb_ue, style="Green.TButton")
        self.start_gnb_ue_btn.grid(row=3, column=0, columnspan=10, padx=20, pady=20)  # Span across 2 columns
        self.stop_gnb_ue_btn = ttk.Button(self.gnb_ue_frame, text="Stop gNB & UE", command=self.stop_gnb_ue, style="Red.TButton")
        self.stop_gnb_ue_btn.grid(row=3, column=3, columnspan=10, padx=20, pady=20)  # Span across 2 columns
        
        ##---------------------------------------------------------------------------------------------##
        ##--------------------Create a frame for TWAMP test controls-----------------------------------##
        ##---------------------------------------------------------------------------------------------##
        self.test_control_frame = ttk.LabelFrame(self.root, text="TWAMP Test Controls")
        self.test_control_frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.NSEW)  # Use sticky=tk.NSEW for frame resizing

        # Start/Stop TWAMP test buttons
        self.start_twamp_btn = ttk.Button(self.test_control_frame, text="Start TWAMP Test", command=self.start_twamp_test, style="Green.TButton")
        self.start_twamp_btn.grid(row=2, column=0,  padx=20, pady=20)

        # IP selection
        ttk.Label(self.test_control_frame, text="Receiver's IP:").grid(row=1, column=0, padx=5, pady=5)
        self.band_var = tk.StringVar()
        self.band_entry = ttk.Entry(self.test_control_frame, textvariable=self.band_var)
        self.band_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # port input
        ttk.Label(self.test_control_frame, text="Port #:").grid(row=1, column=2, padx=5, pady=5)
        self.freq_var = tk.StringVar()
        self.freq_entry = ttk.Entry(self.test_control_frame, textvariable=self.freq_var)
        self.freq_entry.grid(row=1, column=3, padx=10, pady=10)

        self.stop_twamp_btn = ttk.Button(self.test_control_frame, text="Stop TWAMP Test", command=self.stop_twamp_test, style="Red.TButton")
        self.stop_twamp_btn.grid(row=2, column=3, padx=20, pady=20)
        
        ##---------------------------------------------------------------------------------------------##
        ##--------------------Create a frame for BW test controls-----------------------------------##
        ##---------------------------------------------------------------------------------------------##             
        # Create a frame for test controls
        self.test_control_frame = ttk.LabelFrame(self.root, text="BW Test Controls")
        self.test_control_frame.grid(row=2, column=0, padx=10, pady=10, sticky=tk.NSEW)  # Use sticky=tk.NSEW for frame resizing        

        # Start/Stop BW test buttons
        self.start_bw_btn = ttk.Button(self.test_control_frame, text="Start BW Test   ", command=self.start_bw_test, style="Green.TButton")
        self.start_bw_btn.grid(row=1, column=0,  padx=20, pady=20)
        # Band selection
        ttk.Label(self.test_control_frame, text="Receiver's IP:").grid(row=0, column=0, padx=5, pady=5)
        self.band_var = tk.StringVar()
        self.band_entry = ttk.Entry(self.test_control_frame, textvariable=self.band_var)
        self.band_entry.grid(row=0, column=1, padx=10, pady=10)

        # port input
        ttk.Label(self.test_control_frame, text="Port #:").grid(row=0, column=2, padx=5, pady=5)
        self.freq_var = tk.StringVar()
        self.freq_entry = ttk.Entry(self.test_control_frame, textvariable=self.freq_var)
        self.freq_entry.grid(row=0, column=3, padx=10, pady=10)
        
        self.stop_bw_btn = ttk.Button(self.test_control_frame, text="Stop BW Test", command=self.stop_bw_test, style="Red.TButton")
        self.stop_bw_btn.grid(row=1, column=3, padx=20, pady=20)

        ##---------------------------------------------------------------------------------------------##
        ##--------------------Create a frame for Teltonika test controls-----------------------------------##
        ##---------------------------------------------------------------------------------------------##
        self.state_control_frame = ttk.LabelFrame(self.root, text="Teltonika State Controls")
        self.state_control_frame.grid(row=10, column=0, padx=10, pady=10, sticky=tk.NSEW)  # Use sticky=tk.NSEW for frame resizing

        # Start/Stop teltonika button
        self.start_gps_btn = ttk.Button(self.state_control_frame, text="Start Getting States for Teltonika Router", command=self.start_teltonika, style="Green.TButton")
        self.start_gps_btn.grid(row=0, column=0, padx=20, pady=20)
        self.stop_gps_btn = ttk.Button(self.state_control_frame, text="Stop Getting States for Teltonika Router", command=self.stop_teltonika, style="Red.TButton")
        self.stop_gps_btn.grid(row=0, column=3,  padx=20, pady=20)

        # Start/Stop 5G state button
        #self.start_5g_btn = ttk.Button(self.state_control_frame, text="Start 5G", command=self.start_5g, style="Green.TButton")
        #self.start_5g_btn.grid(row=1, column=0,  padx=20, pady=20)
        #self.stop_5g_btn = ttk.Button(self.state_control_frame, text="Stop 5G", command=self.stop_5g, style="Red.TButton")
        #self.stop_5g_btn.grid(row=1, column=3, padx=20, pady=20)

        # Configure grid resizing behavior
        #self.root.grid_rowconfigure(0, weight=1)
        #self.root.grid_rowconfigure(1, weight=1)
        #self.root.grid_rowconfigure(2, weight=1)
        #self.root.grid_columnconfigure(0, weight=1)

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
        self.stop_button = tk.Button(self.button_frame, text="Stop Script", command=self.stop_script, state=tk.DISABLED)
        self.stop_button.pack(side=tk.RIGHT, padx=10)

    def start_twamp_test(self):
        # Example command for starting TWAMP test
        print("Starting TWAMP test.................................")
        script_path = "/home/waseem/Documents/Teltonika States/twamp.py"
        try:
            subprocess.Popen(["python3", script_path])  # Use subprocess to run the script
        except Exception as e:
            print(f"Error: {e}")

    def stop_twamp_test(self):
        # Example command for stopping TWAMP test
        print("Stopping TWAMP test")
        self.stop_button = tk.Button(self.button_frame, text="Stop Script", command=self.stop_script, state=tk.DISABLED)
        self.stop_button.pack(side=tk.RIGHT, padx=10)

    def start_bw_test(self):
        # Example command for starting BW test
        print("Starting BW test..................")
        script_path = "/home/waseem/Documents/Teltonika States/scream-master/MWA_BWTest.py"
        try:
            subprocess.Popen(["python3", script_path])  # Use subprocess to run the script
        except Exception as e:
            print(f"Error: {e}")

    def stop_bw_test(self):
        # Example command for stopping BW test
        print("Stopping BW test")
        self.stop_button = tk.Button(self.button_frame, text="Stop Script", command=self.stop_script, state=tk.DISABLED)
        self.stop_button.pack(side=tk.RIGHT, padx=10)

    def start_teltonika(self):
        # Example command for starting GPS
        print("Starting Getting States for Teltonika Router...............")
        script_path = "/home/waseem/Documents/Teltonika States/gpsgsmstates.py"
        try:
            subprocess.Popen(["python3", script_path])  # Use subprocess to run the script
        except Exception as e:
            print(f"Error: {e}")
        # Add subprocess or appropriate code to start GPS

    def stop_teltonika(self):
        # Example command for stopping GPS
        print("Stop Getting States for Teltonika Router")
        self.stop_button = tk.Button(self.button_frame, text="Stop Script", command=self.stop_script, state=tk.DISABLED)
        self.stop_button.pack(side=tk.RIGHT, padx=10)
        
    def stop_script(self):
        if self.process:
            try:
                # Send SIGINT to the process group
                os.killpg(os.getpgid(self.process.pid), signal.SIGINT)
                self.process.wait(timeout=5)  # Wait for the process to terminate

                # If the process is still running, forcefully terminate it
                if self.process.poll() is None:
                    self.process.terminate()
                    self.process.wait(timeout=5)

                # If the process is still running, forcefully kill it
                if self.process.poll() is None:
                    self.process.kill()
                    self.process.wait(timeout=5)

                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
            except Exception as e:
                print(f"Error stopping the script: {e}")      

   # def start_5g(self):
        # Example command for starting 5G state
    #    print("Starting 5G")
        # Add subprocess or appropriate code to start 5G state

    #def stop_5g(self):
        # Example command for stopping 5G state
     #   print("Stopping 5G")
        # Add subprocess or appropriate code to stop 5G state

def main():
    root = tk.Tk()
    app = FiveGSimulatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

