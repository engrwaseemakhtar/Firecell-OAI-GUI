import tkinter as tk
import subprocess
import os
import signal

class ScriptRunner:
    def __init__(self, root):
        self.root = root
        self.process = None

        self.root.title("Script Runner")

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        self.start_button = tk.Button(self.button_frame, text="Start Script", command=self.start_script)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(self.button_frame, text="Stop Script", command=self.stop_script, state=tk.DISABLED)
        self.stop_button.pack(side=tk.RIGHT, padx=10)

    def start_script(self):
        script_path = "/home/waseem/Documents/Teltonika States/gpsgsmstates.py"
        try:
            # Start the process
            self.process = subprocess.Popen(["python3", script_path], preexec_fn=os.setsid)
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
        except Exception as e:
            print(f"Error: {e}")

    def stop_script(self):
        if self.process:
            try:
                # Send SIGINT to the process group to simulate Ctrl+C
                os.killpg(os.getpgid(self.process.pid), signal.SIGINT)
                self.process.wait(timeout=5)  # Wait for the process to terminate

                # Ensure the process is stopped
                if self.process.poll() is None:
                    self.process.terminate()
                    self.process.wait(timeout=5)

                if self.process.poll() is None:
                    self.process.kill()
                    self.process.wait(timeout=5)

                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
            except Exception as e:
                print(f"Error stopping the script: {e}")

def main():
    root = tk.Tk()
    app = ScriptRunner(root)
    root.mainloop()

if __name__ == "__main__":
    main()

