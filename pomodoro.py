from datetime import datetime, timedelta
import time
from windows_toasts import (
    Toast,
    WindowsToaster,
    ToastDuration,
    ToastAudio,
    AudioSource,
)
import tkinter as tk

# Change to False for real values
test = False

# Sound
play_alarm = True

_pattern_format_time = "%I:%M:%S %p"

# Default times
_max_section_pomo_time = 20 if not test else 1
_max_short_break_time = 5 if not test else 1
_max_long_break_time = 15 if not test else 2

# Current sections
pomo_count = 0
break_count = 0
long_break_count = 0


def send_notification(message: str, is_long: bool = True, title: str = "Pomodoro"):

    toaster = WindowsToaster(title)
    new_toast = Toast([message])
    new_toast.duration = ToastDuration.Long if is_long else ToastDuration.Default

    if play_alarm:
        new_toast.audio = ToastAudio(sound=AudioSource.Alarm)

    toaster.show_toast(new_toast)


def insert_frame(master_, height_):
    """
    Inserta espacio en la ventana
    """
    frame_1 = tk.Frame(master=master_, width=6, height=height_, bg="#212121")
    frame_1.pack()


def get_time():
    """
    Generador contador de tiempo
    """
    while True:
        tm = datetime.now()
        time.sleep(1)
        yield tm.strftime(_pattern_format_time)


def get_finish_time(min: int):
    """
    Obtiene el tiempo en que debe finalizar el pomodoro o la pausa
    ...

    Parameters
    ---
    min : int -> Minutos a sumar al tiempo actual
    """
    tm = datetime.now()
    tm_delta = timedelta(minutes=min)
    tm_finish = tm_delta + tm
    return datetime.strftime(tm_finish, "%I:%M:%S %p")


def UpdateWindowDecor(func):
    """
    Decorador para actualizar el label en la UI
    """

    def wrapper(label: tk.Label, time: str = None):
        func(label, time) if time else func(label)
        window.update()

    return wrapper


def finalizar_pomo_tkinder():
    """
    Finaliza el programa
    """
    window.destroy()


@UpdateWindowDecor
def update_pomo_count(label: tk.Label):
    global pomo_count
    pomo_count += 1
    label["text"] = f"Pomodoros: \n{pomo_count}"


@UpdateWindowDecor
def update_break_count(label: tk.Label):
    global break_count
    break_count += 1
    label["text"] = f"Descansos cortos: \n{break_count}"


@UpdateWindowDecor
def update_long_break_count(label: tk.Label):
    global long_break_count
    long_break_count += 1
    label["text"] = f"Descansos largos: \n{long_break_count}"


@UpdateWindowDecor
def update_label_finish(label: tk.Label, time: str):
    label["text"] = f"Finaliza: {time}"


@UpdateWindowDecor
def update_label_time_count(label: tk.Label, time: str):
    label["text"] = time


def start_break():
    next_break = _max_short_break_time if pomo_count % 4 != 0 else _max_long_break_time

    time_format = get_finish_time(next_break)
    update_label_finish(label_finish, time_format)

    button_end.pack(after=button_start_break)
    button_start_break.pack_forget()

    for x in get_time():
        # try:
        update_label_time_count(label_count_clock, x)
        if x == time_format:
            button_start.pack(after=button_end)
            button_end.pack_forget()

            if next_break == _max_short_break_time:
                update_break_count(label_count_break)
            else:
                update_long_break_count(label_count_long_break)

            send_notification("¡Descanso terminado!")
            break
        # except:
        #     break


def start_pomo():
    global label_finish

    button_end.pack(after=button_start)
    button_start.pack_forget()

    time_format = get_finish_time(_max_section_pomo_time)
    update_label_finish(label_finish, time_format)

    for x in get_time():
        try:
            update_label_time_count(label_count_clock, x)
            if x == time_format:
                button_start_break.pack(after=button_end)
                button_end.pack_forget()
                update_pomo_count(label_count_pomos)
                send_notification("¡Pomodoro terminado!")
                break
        except Exception as err:
            print(f"Error -> {err}")
            break


# UI

_styles = {"color_font": "ivory2", "color_background": "#212121"}
_width_buttons = {"width": 30, "relief": "flat"}
_text_start_clock = "00:00"
_font_poppins = lambda size=12, bold=True: ("Poppins", f"{size}", "bold" if bold else "normal")
_label_style = {"fg": _styles["color_font"], "bg": _styles["color_background"]}

# Tkinter config
window = tk.Tk()
window.title("Pomodoro! by Leonardo Henao")
window.configure(bg=_styles["color_background"])

# Title
label_head = tk.Label(
    window,
    text="Bienvenido, \nNos alegra saber que deseas ser mas productivo.",
    padx=6,
    pady=4,
    font=_font_poppins(),
    **_label_style,
)
label_head.pack()

# Count
label_count_clock = tk.Label(window, text=_text_start_clock, font=("Arial", "20", "roman"), **_label_style)
label_count_clock.pack()

# Finish
label_finish = tk.Label(
    window, text=_text_start_clock, font=("Arial", "15", "roman"), fg="red", bg=_styles["color_background"]
)
label_finish.pack()

# Space
insert_frame(window, 50)

# Button start
button_start = tk.Button(
    window,
    text="Iniciar pomodoro",
    command=start_pomo,
    bg="#2ECC71",
    fg="black",
    font=("poppins", "12", "bold"),
    **_width_buttons,
)
button_start.pack()

# Button end
button_end = tk.Button(
    window,
    text="Finalizar",
    command=finalizar_pomo_tkinder,
    bg="red",
    fg="white",
    font=("poppins", "12", "bold"),
    **_width_buttons,
)

# Button start break
button_start_break = tk.Button(
    window,
    text="Iniciar pausa",
    command=start_break,
    bg="#2E86C1",
    fg="white",
    font=("poppins", "12", "bold"),
    **_width_buttons,
)

# Space
insert_frame(window, 50)

# label count pomo
label_count_pomos = tk.Label(window, text="Pomodoros: \n0", **_label_style, font=_font_poppins(bold=False))
label_count_pomos.pack(fill="both")

# label count break
label_count_break = tk.Label(
    window, text="Descansos cortos: \n0", bg="#3498DB", fg="white", font=_font_poppins(bold=False), width=21
)
label_count_break.pack(side="left")

# label count long break
label_count_long_break = tk.Label(
    window, text="Descansos largos: \n0", font=_font_poppins(bold=False), bg="#2980B9", fg="white", width=21
)
label_count_long_break.pack()

window.mainloop()
