import itertools
import time
from threading import Thread, Event
from primes import is_prime
def spin(msg:str, done:Event ) -> None:        #1
    for char in itertools.cycle(r'\|/-'):      #2
        status=f'\r{char} {msg}'               #3
        print(status, end='',flush=True)
        if done.wait(.1):                      #4
            break                              
    blanks=' ' * len(status)    
    print(f'\r{blanks}\r', end='')             #5

def slow() -> int:
    #time.sleep(3)                              #6
    is_prime(5_000_111_000_222_021)
    return 42

def supervisor() -> int:
    done = Event() # 7
    spinner = Thread(target=spin, args=("thinking!",done)) # 8
    print(f"spinner object: {spinner}")
    spinner.start() # 9
    result = slow()
    done.set() # 10
    spinner.join() # 11
    return result

def main() -> None:
    result = supervisor()
    print(f"Answer: {result}")


"""
#1 This function will run in a separate thread. The done argument is an instance of threading.Event, to synchronize threads.

#2 This is an infinite loop.

#3 This is to move the cursor back to the start of the line with the carriage return -> 'r'

#4 Event.wait(timeout=None) method returns True when the event is set by another thread. if the timeout elapses, it returns False. 
The 0.1s timeout sets the 'frame rate' 

#5 clear the status line by overwriting with spaces and moving the cursor back to the beginning.

#6 slow() will be called by the main thread. 

#7 threading.Event instance is the key to coordinate the activities of the main thread. 

#8 To create a new Thread, provide a function as the target keyword argument and positional arguments to the target as a tuple passed via args

#9 Start the spinner thread

#10 Set the Event flag to True; this will terminate the for loop inside the spin function.

#11 Wait until the spinner thread finishes
"""

if __name__ == '__main__':
    main()

