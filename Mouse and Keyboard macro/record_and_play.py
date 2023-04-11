import keyboard as k  # used only to stop the player if user presses esc during play
import tkinter as tk
from tkinter import scrolledtext
from pynput import mouse, keyboard
from pynput.keyboard import Key as p_k
import json, time, pyautogui


class MouseKeyboardRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Input Recorder")
        self.setup_ui()
        self.special_keys = {"Key.shift": p_k.shift, "Key.tab": p_k.tab, "Key.caps_lock": p_k.caps_lock,
                             "Key.ctrl": p_k.ctrl, "Key.ctrl_l": p_k.ctrl_l, "Key.alt": p_k.alt, "Key.cmd": p_k.cmd,
                             "Key.cmd_r": p_k.cmd_r, "Key.alt_r": p_k.alt_r, "Key.alt_l": p_k.alt_l,
                             "Key.ctrl_r": p_k.ctrl_r, "Key.shift_r": p_k.shift_r, "Key.enter": p_k.enter,
                             "Key.backspace": p_k.backspace,"Key.right": p_k.right, "Key.down": p_k.down,
                             "Key.left": p_k.left, "Key.up": p_k.up, "Key.page_up": p_k.page_up,
                             "Key.page_down": p_k.page_down, "Key.home": p_k.home, "Key.end": p_k.end,
                             "Key.delete": p_k.delete, "Key.space": p_k.space, 'Key.alt_gr': p_k.alt_gr,
                             'Key.menu': p_k.menu, "Key.esc": p_k.esc
                             }
        self.root.mainloop()

    def setup_ui(self):
        self.root.configure(padx=50, pady=50)

        self.record_button = tk.Button(self.root, text="Record", command=self.record)
        self.record_button.grid(row=0, column=0, padx=25)

        self.play_button = tk.Button(self.root, text="Play", command=self.play, state="disabled")
        self.play_button.grid(row=0, column=1, padx=25)

        self.loops = tk.Entry(self.root, state='disabled')
        self.loops.grid(row=0, column=3, padx=25)

        self.loops_label = tk.Label(self.root, text="How many times do you want this program to repeat?")
        self.loops_label.grid(row=0, column=2)

        self.log = scrolledtext.ScrolledText(self.root, width=50, height=10)
        self.log.grid(row=1, column=0, columnspan=2, pady=50)

    def record(self):
        self.log.insert(tk.END, "Recording...\n")
        self.log.see(tk.END)

        self.record_button.config(state="disabled")
        self.play_button.config(state="disabled")

        self.data = []
        self.start_time = time.time()
        self.mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

        self.mouse_listener.start()
        self.keyboard_listener.start()

    def play(self):
        self.log.insert(tk.END, "Playing...\n")
        self.log.see(tk.END)

        with open("data.txt", "r") as f:
            data = json.load(f)

        looper = int(self.loops.get())
        for i in range(looper):
            prev_time = data[0]["time"]
            for action in data:
                event = action["event"]
                args = action["args"]

                curr_time = action["time"]
                time_diff = curr_time - prev_time
                time.sleep(time_diff)

                if event == "move":
                    mouse.Controller().position = args
                elif event == "click":
                    button = args[2]
                    pressed = args[3]
                    x, y = args[0], args[1]

                    # using pyautogui to click because pynput doesn't work as well. it clicks/drags instead of click
                    if pressed:
                        if button == "Button.right":
                            pyautogui.rightClick(x, y)
                        else:
                            pyautogui.leftClick(x, y)
                elif event == "scroll":
                    mouse.Controller().scroll(*args)
                elif event == "press" or event == "release":
                    if args == 'Key.esc':
                        continue
                    if args not in self.special_keys:
                        keyboard.Controller().press(args)
                        keyboard.Controller().release(args)
                    else:
                        x = self.special_keys[args]
                        keyboard.Controller().press(x)
                        keyboard.Controller().release(x)

                prev_time = curr_time

                # If escape key is pressed, stop playing
                if k.is_pressed('esc'):
                    self.log.insert(tk.END, "Playback stopped\n")
                    self.log.see(tk.END)
                    return

            self.log.insert(tk.END, "Playback complete\n")
            self.log.see(tk.END)

    def on_move(self, x, y):
        if self.data and self.data[-1]["event"] == "move":
            if (time.time() - self.start_time) - self.data[-1]["time"] < .02:
                return

        timestamp = time.time() - self.start_time
        self.data.append({"event": "move", "args": (x, y), "time": timestamp})
        from_pos = self.data[-2]["args"] if len(self.data) > 1 else ""
        self.log.insert(tk.END, f"Moved {from_pos} to {x, y}\n")
        self.log.see(tk.END)

    def on_click(self, x, y, button, pressed):
        timestamp = time.time() - self.start_time
        self.data.append({"event": "click", "args": (x, y, str(button), pressed), "time": timestamp})
        self.log.insert(tk.END, f"{'Pressed' if pressed else 'Released'} {button} at {x, y}\n")
        self.log.see(tk.END)

    def on_scroll(self, x, y, dx, dy):
        timestamp = time.time() - self.start_time
        self.data.append({"event": "scroll", "args": (dx, dy), "time": timestamp})
        self.log.insert(tk.END, f"Scrolled by {dx, dy}\n")
        self.log.see(tk.END)

    def on_press(self, key):
        timestamp = time.time() - self.start_time
        try:
            self.data.append({"event": "press", "args": key.char, "time": timestamp})
            self.log.insert(tk.END, f"Key pressed: {key.char}\n")
        except AttributeError:
            self.data.append({"event": "press", "args": str(key), "time": timestamp})
            self.log.insert(tk.END, f"Key pressed: {key}\n")

        self.log.see(tk.END)
        if key == keyboard.Key.esc:
            self.stop_recording()

    def on_release(self, key):
        timestamp = time.time() - self.start_time
        try:
            self.data.append({"event": "release", "args": key.char, "time": timestamp})
            self.log.insert(tk.END, f"Key released: {key}\n")
        except AttributeError:
            self.data.append({"event": "release", "args": str(key), "time": timestamp})
            self.log.insert(tk.END, f"Key released: {str(key)}\n")
        self.log.see(tk.END)

    def stop_recording(self):
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        self.record_button.config(state="normal")
        self.play_button.config(state="normal")
        self.loops.config(state="normal")
        self.loops.delete(0)
        self.loops.insert(0, "0")

        with open("data.txt", "w") as f:
            json.dump(self.data, f)

        self.log.insert(tk.END, "Recording stopped.\n")
        self.log.see(tk.END)


if __name__ == "__main__":
    app = MouseKeyboardRecorder()
