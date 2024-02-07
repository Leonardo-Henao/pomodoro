from datetime import datetime, timedelta
import time
from windows_toasts import Toast, WindowsToaster, ToastDuration
import tkinter as tk

# Change to False for real values
test = True

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
    toaster.show_toast(new_toast)


def insert_frame(master_, height_, row_, column_=1):
    """
    Inserta espacio en la ventana
    """
    frame_1 = tk.Frame(master=master_, width=6, height=height_, bg="#212121")
    frame_1.grid(column=column_, row=row_, columnspan=6)


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
    def wrapper(label: tk.Label, time: str = None):
        func(label, time) if time else func(label)
        window.update()

    return wrapper


def finalizar_pomo_tkinder():
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

    button_end.grid(**_button_center)
    button_start_break.grid_remove()

    for x in get_time():
        try:
            update_label_time_count(label_count_clock, x)
            if x == time_format:
                button_end.grid_remove()
                button_start.grid(**_button_center)

                if next_break == _max_short_break_time:
                    update_break_count(label_count_break)
                else:
                    update_long_break_count(label_count_long_break)

                send_notification("¡Descanso terminado!")
                break
        except:
            break


def start_pomo():
    global label_finish

    button_start.grid_remove()
    button_end.grid(**_button_center)

    time_format = get_finish_time(_max_section_pomo_time)
    update_label_finish(label_finish, time_format)

    for x in get_time():
        try:
            update_label_time_count(label_count_clock, x)
            if x == time_format:
                button_end.grid_remove()
                button_start_break.grid(**_button_center)
                update_pomo_count(label_count_pomos)
                send_notification("¡Pomodoro terminado!")
                break
        except Exception as err:
            print(f"Error -> {err}")
            break


# GUI

_styles = {"color_font": "ivory2", "color_background": "#212121"}
_button_center = {"column": 3, "row": 5}
_width_buttons = {"width": 30}
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
    padx=4,
    pady=2,
    font=_font_poppins(),
    **_label_style,
)
label_head.grid(column=1, row=1, columnspan=6)

# Count
label_count_clock = tk.Label(window, text=_text_start_clock, font=("Arial", "20", "roman"), **_label_style)
label_count_clock.grid(column=1, row=2, columnspan=6, pady=2)

# Finish
label_finish = tk.Label(
    window, text=_text_start_clock, font=("Arial", "15", "roman"), fg="red", bg=_styles["color_background"]
)
label_finish.grid(column=1, row=3, columnspan=6)

# Space
insert_frame(window, 50, 4)

# Button
button_start = tk.Button(
    window,
    text="Iniciar pomodoro",
    command=start_pomo,
    bg="cyan",
    fg="black",
    font=("poppins", "12", "bold"),
    **_width_buttons,
)
button_start.grid(**_button_center)

button_end = tk.Button(
    window,
    text="Finalizar",
    command=finalizar_pomo_tkinder,
    bg="red",
    fg="white",
    font=("poppins", "12", "bold"),
    **_width_buttons,
)


button_start_break = tk.Button(
    window,
    text="Iniciar pausa",
    command=start_break,
    bg="gray",
    fg="black",
    font=("poppins", "12", "bold"),
    **_width_buttons,
)

# Space
insert_frame(window, 50, 7)

# label count pomo
label_count_pomos = tk.Label(window, text="Pomodoros: \n0", **_label_style, font=_font_poppins(bold=False))
label_count_pomos.grid(column=2, row=8)

# label count break
label_count_break = tk.Label(window, text="Descansos cortos: \n0", **_label_style, font=_font_poppins(bold=False))
label_count_break.grid(column=3, row=8)

# label count long break
label_count_long_break = tk.Label(window, text="Descansos largos: \n0", **_label_style, font=_font_poppins(bold=False))
label_count_long_break.grid(column=5, row=8)

window.mainloop()
