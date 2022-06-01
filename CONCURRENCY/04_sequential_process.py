import sys
from time import perf_counter
from typing import NamedTuple
from multiprocessing import Process, SimpleQueue, cpu_count
from multiprocessing import queues 

from primes import is_prime, NUMBERS

class PrimeResult(NamedTuple):
    n: int
    prime: bool
    elapsed: float

JobQueue = queues.SimpleQueue[int] #1 
ResultQueue = queues.SimpleQueue[PrimeResult] #2 

def check(n:int) -> PrimeResult:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n,res,perf_counter() - t0)

def worker(jobs: JobQueue, results:ResultQueue) -> None: #3
    while n := jobs.get(): #4 walrus operator assining value from right to the left.
        results.put(check(n)) #5
    results.put(PrimeResult(0,False,0.0)) #6

def start_jobs(
    procs: int, jobs: JobQueue, results: ResultQueue #7
) -> None:
    for n in NUMBERS:
        jobs.put(n)     #8
    for _ in range(procs):
        proc = Process(target=worker, args=(jobs,results)) #9
        proc.start() #10
        jobs.put(0) #11

"""
#1 For type alias that main function will use. 

#2 For type alias. The values in the queue will be tuples made of the number to be tested and Result tuple

#3 This gets a queue with the numbers to be checked, and another to put results.

#4 In this code, I use number 0 as a poison pill: a signal for the worker to finish. If n is not 0, proceed with the loop.

#5 Invoke the primality check and enqueue PrimeResult

#6 Send back a PrimeResult(0, False, 0.0) to let the main loop know that this worker is done.

#7 procs is the number of processes that will compute the prime checks in parallel.

#8 Enqueue the numbers to be checked in jobs.

#9 Fork a child process for each worker. Each child will run the loop inside its own instance of the worker function,
    until it fetches a 0 from the jobs queue.

#10 start ewach child process

#11 Enqueue one 0 for each process, to terminate them. 
"""

def main() -> None:
    if len(sys.argv) <2: #1 
        procs = cpu_count()
    else:
        procs = int(sys.argv[1])
    print(f"Checking {len(NUMBERS)} numbers with {procs} processes:")
    t0 = perf_counter()
    jobs: JobQueue = SimpleQueue() #2  
    results: ResultQueue = SimpleQueue()
    start_jobs(procs, jobs, results) #3 
    checked = report(procs, results) #4
    elapsed = perf_counter() - t0
    print(f"{checked} checks in {elapsed:.2f}s") 

def report(procs:int, results: ResultQueue) -> int: 
    checked = 0
    procs_done = 0
    while procs_done < procs: #5
        n, prime, elapsed = results.get() #6
        if n == 0: #7
            procs_done += 1
        else:
            checked += 1 #8
            label = 'P' if prime else ' '
            print(f"{n:16}  {label} {elapsed:9.6f}s")
    return checked

"""
#1 If no command-line argument is given, set the number of processes to the number of CPU cores

#2 jobs and results are the queues. We must call this multiprocssing.SimpleQueue to build a queue.
Keep in mind that we can't use this in type hints. For type hints, we use multiprocessing.queues.SimpleQueue. 

#3 start proc processes to consume jobs and post results 

#4 Retrieve the result and dsiplay them. 

#5 loop until all processes are done.

#6 get one PrimeResult. Calling .get() on a queue block until there is an item in the queue. 
   it's also possible to make this nonblocking, or set a timeout. For that, see the SimpleQueue.get documentation. 

#7 if n is zero, then one process exited; increment the procs_done count. 

#8 otherwise, increment the checked count(to keep track of the numbers checked) and display the results. 
"""

if __name__ == "__main__":
    main()