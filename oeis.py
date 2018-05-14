import json
import re
import threading
import time
from datetime import datetime
from requests import get
from requests.exceptions import RequestException
from contextlib import closing


def simple_get(url):
    '''Makes an HTTP GET request, returning the content as bytes.'''
    with closing(get(url, stream=True)) as resp:
        return resp.content

def get_xrefs(An):
    '''Scrape the crossrefs for an A-number.
       This ignores "in context" and adjacent sequences.'''
    s = simple_get('https://oeis.org/search?q=' + An + '&fmt=json')
    s = s.replace(b'\n', b'') #get rid of pesky formatting
    s = s.replace(b'\t', b'')
    try:
        f = json.loads(s)
    except: #we went too fast
        return None
    if 'xref' in f['results'][0].keys(): #are there xrefs?
        xrefs_raw = f['results'][0]['xref'] #navigate the json
        xrefs = []
        for entry in xrefs_raw:
            xrefs = xrefs + re.findall('A[0-9]{6}', entry) #pull out the A-numbers using regex
        return xrefs
    return []

def int_to_An(i):
    '''Converts an integer to an A-number (ex: 1 -> A000001).'''
    n = str(i)
    if len(n) < 6:
        n = '0'*(6-len(n)) + n #leading zeros
    An = 'A' + n
    return An

D = {} #will contain a dictionary format of the network
PAUSE = True #used for thread control
DONE = False #used for thread control

def format_network(filename='output.csv'):
    '''Saves the network as a csv to the specified filename.'''
    global D
    f = open(filename, 'w')
    keys = set(D.keys()) #D changes during loop, so we snapshot it
    for An in keys:
        s = An
        for cf in D[An]:
            s = s + ',' + cf
        f.write(s+'\n')
    f.close()

def pauser():
    '''Essentially a controller for the fetching threads.'''
    global D, PAUSE, DONE, IP1, IP2, IP3, IP4
    N = 1000
    while not DONE:
        if get_xrefs('A000001') is None:
            if not PAUSE:
                print(str(datetime.now()), 'Pausing at', len(D.keys()))
                format_network()
            PAUSE = True
        else:
            if PAUSE:
                print(str(datetime.now()), 'Resuming at', len(D.keys()))
            PAUSE = False
        if PAUSE:
            time.sleep(1)
        if len(D.keys()) > N:
            print(str(datetime.now()), N)
            format_network()
            N += 1000

def single_An(i):
    '''A single fetching thread.'''
    global D, PAUSE
    An = int_to_An(i)
    while PAUSE:
        pass
    r = get_xrefs(An)
    while r is None: #a bit janky, but guarantees we get the entry eventually
        time.sleep(10)
        r = get_xrefs(An)
    D[An] = r

def create_xrefs_dict(maxn=304236):
    '''Scrape the crossrefs for all A-numbers up to maxn
       and put them in the global D dictionary.'''
    global D, PAUSE, DONE
    i = 1
    p = threading.Thread(target=pauser) #a thread to pause when we go too fast
    p.start()
    while i <= maxn:
        while PAUSE:
            pass
        t = threading.Thread(target=single_An, args=(i,)) #multithreading for speed
        while threading.active_count() > 5: #speed limit (pauser + 4 fetching)
            pass
        t.start()
        i += 1
    while len(D.keys()) < maxn: #wait for all the fetching to finish
        pass
    DONE = True #stops the pauser thread
    print('Scraping done')
    format_network()
    print('Output done')
