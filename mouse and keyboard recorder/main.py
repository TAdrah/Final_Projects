import keyword as k  # used only to stop the player if user presses esc during play
import tkinter as tk
from tkinter import scrolledtext
from pynput import mouse, keyboard
from pynput.keyboard import Key as PK
import json, time, pyautogui


def record():
    log.insert(tk.END, "Recording...\n")
    log.see(tk.END)

    record_button.config(state="disabled")
    play_button.config(state="disabled")

    mouse_listener.start()
    keyboard_listener.start()


def play():
    log.insert(tk.END, "Playing...\n")
    log.see(tk.END)

    with open("data.txt", "r") as f:
        data_file = json.load(f)

    looper = int(loops.get())
    for i in range(looper):
        prev_time = data_file[0]["time"]
        for action in data_file:
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
                if args not in special_keys:
                    keyboard.Controller().press(args)
                    keyboard.Controller().release(args)
                else:
                    x = special_keys[args]
                    keyboard.Controller().press(x)
                    keyboard.Controller().release(x)

            prev_time = curr_time

            # If escape key is pressed, stop playing
            if k.is_pressed('esc'):
                log.insert(tk.END, "Playback stopped\n")
                log.see(tk.END)
                return

        log.insert(tk.END, "Playback complete\n")
        log.see(tk.END)


def on_move(x, y):
    if data and data[-1]["event"] == "move":
        if (time.time() - start_time) - data[-1]["time"] < .02:
            return

    timestamp = time.time() - start_time
    data.append({"event": "move", "args": (x, y), "time": timestamp})
    from_pos = data[-2]["args"] if len(data) > 1 else ""
    log.insert(tk.END, f"Moved {from_pos} to {x, y}\n")
    log.see(tk.END)


def on_click(x, y, button, pressed):
    timestamp = time.time() - start_time
    data.append({"event": "click", "args": (x, y, str(button), pressed), "time": timestamp})
    log.insert(tk.END, f"{'Pressed' if pressed else 'Released'} {button} at {x, y}\n")
    log.see(tk.END)


def on_scroll(x, y, dx, dy):
    timestamp = time.time() - start_time
    data.append({"event": "scroll", "args": (dx, dy), "time": timestamp})
    log.insert(tk.END, f"Scrolled by {dx, dy}\n")
    log.see(tk.END)


def on_press(key):
    timestamp = time.time() - start_time
    try:
        data.append({"event": "press", "args": key.char, "time": timestamp})
        log.insert(tk.END, f"Key pressed: {key.char}\n")
    except AttributeError:
        data.append({"event": "press", "args": str(key), "time": timestamp})
        log.insert(tk.END, f"Key pressed: {key}\n")

    log.see(tk.END)
    if key == keyboard.Key.esc:
        stop_recording()


def on_release(key):
    timestamp = time.time() - start_time
    try:
        data.append({"event": "release", "args": key.char, "time": timestamp})
        log.insert(tk.END, f"Key released: {key}\n")
    except AttributeError:
        data.append({"event": "release", "args": str(key), "time": timestamp})
        log.insert(tk.END, f"Key released: {str(key)}\n")
    log.see(tk.END)


def stop_recording():
    mouse_listener.stop()
    keyboard_listener.stop()
    record_button.config(state="normal")
    play_button.config(state="normal")
    loops.config(state="normal")
    loops.delete(0)
    loops.insert(0, "1")

    with open("data.txt", "w") as f:
        json.dump(data, f)

    log.insert(tk.END, "Recording stopped.\n")
    log.see(tk.END)


root = tk.Tk()
root.title("Input Recorder")
special_keys = {"Key.shift": PK.shift, "Key.tab": PK.tab, "Key.caps_lock": PK.caps_lock, "Key.ctrl": PK.ctrl,
                "Key.ctrl_l": PK.ctrl_l, "Key.alt": PK.alt, "Key.cmd": PK.cmd, "Key.cmd_r": PK.cmd_r,
                "Key.alt_r": PK.alt_r, "Key.alt_l": PK.alt_l, "Key.ctrl_r": PK.ctrl_r, "Key.shift_r": PK.shift_r,
                "Key.enter": PK.enter,"Key.backspace": PK.backspace, "Key.right": PK.right, "Key.down": PK.down,
                "Key.left": PK.left, "Key.up": PK.up, "Key.page_up": PK.page_up, "Key.page_down": PK.page_down,
                "Key.home": PK.home, "Key.end": PK.end, "Key.delete": PK.delete, "Key.space": PK.space,
                'Key.alt_gr': PK.alt_gr, 'Key.menu': PK.menu, "Key.esc": PK.esc
                }
data = []
start_time = time.time()
mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

# ------------- set up UI ----------------- #
root.configure(padx=50, pady=50)

record_button = tk.Button(root, text="Record", command=record)
record_button.grid(row=0, column=0, padx=25)

play_button = tk.Button(root, text="Play", command=play, state="disabled")
play_button.grid(row=0, column=1, padx=25)

loops = tk.Entry(root, state='disabled')
loops.grid(row=0, column=3, padx=25)

loops_label = tk.Label(root, text="How many times do you want this program to repeat?")
loops_label.grid(row=0, column=2)

log = scrolledtext.ScrolledText(root, width=50, height=10)
log.grid(row=1, column=0, columnspan=2, pady=50)

root.mainloop()

