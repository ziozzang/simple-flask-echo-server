#!python3
# Very Simple Flask based test server
# Author: Jioh L. Jung <ziozzang@gmail.com>

import flask
import os
import datetime, time
import psutil

import string
import socket
import signal

import threading

#- Define Flask App -----------------------------------------------------------
app = flask.Flask(__name__)

#- Set default object ---------------------------------------------------------
stop_cpu_flag, stop_mem_flag = True, True
mem_holder = ''

thread_pool = []

#- Define Functions -----------------------------------------------------------
def caclulate_pi(cnt=1000000):
    global stop_cpu_flag
    
    # Initialize denominator
    k = 1
    
    # Initialize sum
    s = 0
    
    for i in range(cnt):
        if stop_cpu_flag:
            time.sleep(0.1)
            return s
    
        # even index elements are positive
        if i % 2 == 0:
            s += 4/k
        else:
            # odd index elements are negative
            s -= 4/k
    
        # denominator is odd
        k += 2
    return s


def get_memory_allocator(length):
    global stop_mem_flag
    
    if stop_mem_flag:
        time.sleep(0.1)
        return ''
    
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = '$' * length
    return result_str

# Get Signal and set thread shutdown flag
def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    # Stop all threads
    for i in thread_pool:
        i.shutdown_flag.set()
    for i in thread_pool:
        i.join()
    exit(signum)

#- Define Thread Class --------------------------------------------------------
# CPU Burnin Test
# Issue : CPU burnin test support only single core (cuz of limitation of python)
class BurninTestCPU(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.shutdown_flag = threading.Event()
 
    def run(self):
        while not self.shutdown_flag.is_set():
            caclulate_pi(100000000000000)
            

# Memory Burnin Test
# Issue: Memory burnin test support has issue about OOM killer.
class BurninTestMem(threading.Thread):
    def __init__(self, mem_size, percent=0.9):
        threading.Thread.__init__(self) 
        self.shutdown_flag = threading.Event()
        self.mem_size = mem_size
        self.percent = percent
 
    def run(self):
        global mem_holder
        while not self.shutdown_flag.is_set():
            mem_holder = get_memory_allocator(int(self.mem_size * self.percent))
 
#- Set Flask Routes -----------------------------------------------------------
@app.route('/')
def index():
    # Get System Status
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    
    # Get current time string
    time_string = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Get hostname
    hostname = os.uname()[1]
    
    # Get Headers
    headers_string = ''
    headers = flask.request.headers
    for key, value in headers.items():
        print(key, value)
        headers_string += '> ' + key + ': ' + value + '\n'
    
    # Get Remote IP address
    ip_remote = flask.request.remote_addr
    
    # Get System IP address
    #ip_host = os.popen('hostname -I').read()
    ip_host = socket.gethostbyname(socket.gethostname())
    return f'''
<pre>
Request received at {time_string}

Hostname: {hostname}
Remote IP: {ip_remote}
Host IP: {ip_host}

Headers
{headers_string}

System Status
> CPU Usage: {cpu_usage}%
> RAM Usage: {ram_usage}%

</pre>


'''

@app.route('/burn-cpu')
def burn_cpu():
    global stop_cpu_flag
    stop_cpu_flag = False
    return 'Burn CPU started'


@app.route('/stop-cpu')
def stop_cpu():
    global stop_cpu_flag
    stop_cpu_flag = True
    return 'Burn CPU stopped'

@app.route('/burn-mem')
def burn_mem():
    global stop_mem_flag
    stop_mem_flag = False
    return 'Burn Memory started'

@app.route('/stop-mem')
def stop_mem():
    global stop_mem_flag
    stop_mem_flag = True
    return 'Burn Memory stopped'

@app.route('/exit')
def exit_app():
    print('EXIT called')
    os._exit(0)


@app.route('/env')
def env():
    env_strs = ''
    envs = os.environ
    for key, value in envs.items():
        env_strs += '> ' + key + ': ' + value + '\n'
    return f'''
<pre>
Environment Variables
{env_strs}
</pre>
'''


if __name__ == '__main__':
    #- Set signal handler -----------------------------------------------------
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    
    #- Create Thread ----------------------------------------------------------
    # Thread for Memory Burnin
    mem_size = psutil.virtual_memory().total
    print('memory size: ', mem_size)
    thread_pool.append(BurninTestMem(mem_size))

    # Thread for CPU Burnin
    core_count = os.cpu_count()
    print('core count: ', core_count)
    for i in range(core_count):
        thread_pool.append(BurninTestCPU())
    
    for i in thread_pool:
        i.start()
    
    #- Run app -----------------------------------------------------------------
    app.run(host='0.0.0.0', port=8080)

