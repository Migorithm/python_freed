import itertools
import time
from multiprocessing import Process, Event
from multiprocessing import synchronize


def spin(msg:str, done:synchronize.Event ) -> None:        #1
    for char in itertools.cycle(r'\|/-'):      #2
        status=f'\r{char} {msg}'               #3
        print(status, end='',flush=True)
        if done.wait(.1):                      #4
            break                              
    blanks=' ' * len(status)    
    print(f'\r{blanks}\r', end='')             #5

def slow() -> int:
    time.sleep(3)  
    return 42

def supervisor() -> int:
    done = Event() # 7
    spinner = Process(target=spin, 
                args=("thinking!",done)) # 8
    print(f"spinner object: {spinner}")
    spinner.start() # 9
    result = slow()
    done.set() # 10
    spinner.join() # 11
    return result

def main() -> None:
    result = supervisor()
    print(f"Answer: {result}")

if __name__ == '__main__':
    main()

