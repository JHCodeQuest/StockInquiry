#simulate processing delay

import time


def simulate_thinking(seconds, message="Processing..."):
    print(message)
    for i in range(seconds):
        time.sleep(1)
        print(f"{i + 1}s...")