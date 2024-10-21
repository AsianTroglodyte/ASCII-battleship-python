import time
import sys
animation = "|/-\\"
start_time = time.time()

sys.stdout.write("press x and enter to leave (Yes, it would be nicer if you didn't\n  \
have to press enter, but that would requires some black magic)\n\n")

sys.stdout.flush()

while True:
    for i in range(4):
        time.sleep(0.2)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()
    if time.time() - start_time > 10:
        break

sys.stdout.write("\rDone!")

