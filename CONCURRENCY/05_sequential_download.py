import time
from pathlib import Path
from typing import Callable
import httpx

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'https://www.fluentpython.com/data/flags'
DEST_DIR = Path("downloaded") #Local directory where the images are saved. 

def save_flag(img:bytes, filename:str) -> None:  #Save image bites to filename in the DEST_DIR
    (DEST_DIR / filename).write_bytes(img)

def get_flag(cc:str) -> bytes:
    url = f"{BASE_URL}/{cc}/{cc}.gif".lower()
    resp = httpx.get(url, timeout=6.1,     # set timeout to avoid blocking for several minutes for no good reason. 
                    follow_redirects=True) # By default, HTTPX does not follow redirects.
    resp.raise_for_status()                # There is no error handling but this method raises an exception if HTTP status is not in the 2XX range
    return resp.content

def download_many(cc_list:list[str]) -> int: #This is a key function to compare with the concurrent implementations 
    for cc in sorted(cc_list):
        image = get_flag(cc)
        save_flag(image, f'{cc}.gif')
        print(cc, end=" ", flush=True)  #Display one country code at a time. flush=True argument is needed 
                                        #because by default Python output is line buffered meaning that 
                                        #Python only displays printed characters after a line break
    return len(cc_list)

def main(downloader:Callable[[list[str]],int]) -> None: #13
    DEST_DIR.mkdir(exist_ok=True)       # Create DEST_DIR if needed; don't raise an error if the directory exists.
    t0 = time.perf_counter()            
    count = downloader(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f"\n{count} downloads in {elapsed:.2f}s")

if __name__ == "__main__":
    main(download_many)