import time
import sys
import keyboard
import threading

# printing out some instructions before user is done
sys.stdout.write("press x and enter to leave (Yes, it would be nicer if you didn't\n\
have to press enter, but that would requires some black magic)\n\n")
sys.stdout.flush()


exit_flag = False

# callbacks for different hotkeys 

# def on_space():
#     sys.stdout.write("\nspace pressed")
#     sys.stdout.flush()
#     exit_flag = True
# keyboard.add_hotkey('space', on_space)


def keyboard_listener():
    while True:
        event = keyboard.read_event()
        if (event.event_type == keyboard.KEY_DOWN and event.name == "x"):
            sys.stdout.write("\nx pressed")
            sys.stdout.flush()
            exit_flag = True
            sys.exit(0)


# naturally must be nonblocking
def run_animation():
    animation = "|/-\\"
    start_time = time.time()
    while True:
        for i in range(4):
            time.sleep(0.1)
            sys.stdout.write("\r" + animation[i % len(animation)])
            sys.stdout.flush()
            if (exit_flag == True):
                sys.exit(0)


# main function
if __name__ == "__main__":
    # printing title of game 
    sys.stdout.write("\
______       _   _   _           _     _\n\
| ___ \     | | | | | |         | |   (_)\n\
| |_/ / __ _| |_| |_| | ___  ___| |__  _ _ __  \n\
| ___ \/ _` | __| __| |/ _ \/ __| '_ \| | '_ \ \n\
| |_/ / (_| | |_| |_| |  __/\__ \ | | | | |_) |\n\
\____/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/\n\
                                        | |\n\
                                        |_|\n\n")

    # start animation thread
    run_animation_thread = threading.Thread(target=run_animation)
    run_animation_thread.daemon = True
    run_animation_thread.start()
    
    # start keyboard listener thread
    keyboard_listener_thread = threading.Thread(target=keyboard_listener)
    keyboard_listener_thread.start()

    # wait for keyboard_listener_thread to finish (when x for exit is pressed)
    keyboard_listener_thread.join()

    sys.stdout.write("\nExiting!")
    sys.exit(0)

