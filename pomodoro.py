import time
import vlc
from colorama import just_fix_windows_console, init, Fore
from colorama.ansi import clear_screen
from windows_toasts import Toast, WindowsToaster, ToastDuration

just_fix_windows_console()
init(autoreset=True, convert=True)

# Change to False for real values
test = False

# Default times
_max_section_time = 20 * 60 if not test else 10
_max_break_time = 5 * 60 if not test else 4
_max_sections_to_long_break = 4
_max_long_break_time = 15 * 60 if not test else 7

# Current sections
section_number = 1

# Messages
message_finish_pomodoro = "¿Desear finalizar Pomodoro? [S] o [N]: "
message_error = "Opción invalida 👾"


def print_seconds(arg):
    minutes = int(arg / 60)
    minutes = str(minutes) if minutes > 9 else str(f"0{minutes}")
    seconds = arg % 60
    seconds = str(seconds) if seconds > 9 else str(f"0{seconds}")

    print_formatted = f"{minutes}:{str(seconds)}"
    print(Fore.CYAN + print_formatted, end='\r')


def print_message_app(message):
    print(Fore.YELLOW + message)


def print_error(message):
    print(Fore.RED + message)


def send_notification(
    message: str, is_long: bool = True, title: str = "Pomodoro leonardohenao.com"
):
    toaster = WindowsToaster(title)
    new_toast = Toast([message])
    new_toast.duration = ToastDuration.Long if is_long else ToastDuration.Default
    toaster.show_toast(new_toast)


def start_player(path_sound):
    player_st = vlc.MediaPlayer(path_sound)
    player_st.play()


def show_message_finish_pomodoro():
    while True:
        options_close = input(message_finish_pomodoro)
        if options_close.lower() == 's':
            exit()
        else:
            break


def control_pomodoro():
    while True:
        options = input("¿Deseas continuar con el Pomodoro? [S] o [N]: ")
        if options.lower() == 's':
            start_pomodoro()
            break
        elif options.lower() == 'n':
            show_message_finish_pomodoro()
        else:
            print_error(message_error)
            continue


def start_break(long: bool = False):
    count = 0
    time_to_break = _max_break_time if not long else _max_long_break_time
    start_player("/media/break_time.mp3")
    while True:
        time.sleep(1)
        count += 1
        print_seconds(time_to_break - count)
        if count == time_to_break:
            send_notification("¡Tiempo de descanso finalizado!")
            control_pomodoro()
            break


def control_breaks():
    global _max_sections_to_long_break, section_number

    message_start_break = "¿Deseas iniciar ya el tiempo de descanso? [S] o [N]: "

    if section_number == _max_sections_to_long_break:
        print("Descanso largo muy merecido 🐻")
        while True:
            options = input(message_start_break)
            if options.lower() == 's':
                section_number = 1
                start_break(long=True)
                break
            elif options.lower() == 'n':
                show_message_finish_pomodoro()
            else:
                print_error(message_error)
                continue
    elif section_number < _max_sections_to_long_break:
        print(f"Descanso de {int(_max_break_time / 60)}.")
        while True:
            options = input(message_start_break)
            if options.lower() == 's':
                start_break()
                break
            elif options.lower() == 'n':
                show_message_finish_pomodoro()
            else:
                print_error(message_error)
                continue


def start_pomodoro():
    global section_number
    count = 0
    start_player("/media/pomodoro_start.mp3")
    try:
        while True:
            time.sleep(1)
            count += 1
            if count == _max_section_time:
                send_notification("¡Tiempo finalizado!")
                start_player("/media/alert_pomodoro.mp3")
                section_number += 1
                control_breaks()
                break
            else:
                print_seconds(_max_section_time - count)
    except KeyboardInterrupt:
        print_message_app("Saliendo de Pomodoro, hasta la proxima. 🧙 ")
        exit()


print(clear_screen())
print_message_app("Bienvenido, iniciando el Pomodoro!")
start_pomodoro()
