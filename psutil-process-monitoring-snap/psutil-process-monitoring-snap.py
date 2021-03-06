import psutil
import pandas as pd
import time
import os
from datetime import datetime

def get_size(bytes, suffix=''):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(bytes) < 1024.0:
            return "%3.1f%s%s" % (bytes, unit, suffix)
        bytes /= 1024.0
    return "%.1f%s%s" % (bytes, 'Yi', suffix)

def get_processes_info():
    # the list the contain all process dictionaries
    up=0
    processes = []
    for process in psutil.process_iter():
      if(process.pid!=os.getpid()):
           pid = process.pid
           if pid == 0:
                # System Idle Process for Windows NT, useless to see anyways
               continue
           name = process.name()
           p = psutil.Process(pid)
           cpu_usage = p.cpu_percent()
           mem_usage=p.memory_percent()
           status = process.status()
           cwd=p.cwd()
           # get the time the process was spawned
           try:
               create_time = datetime.fromtimestamp(process.create_time())
           except OSError:
                # system processes, using boot time instead
               create_time = datetime.fromtimestamp(psutil.boot_time())
           except OSError:
                # system processes, using boot time instead
               create_time = datetime.fromtimestamp(psutil.boot_time())

           uptime=time.time() - process.create_time()
           #uptime=time.strftime('%H:%M:%S', time.gmtime(uptime))
           if (uptime<60):
               uptime=round((uptime/60),2)
           try:
               username = process.username()
           except psutil.AccessDenied:
               username = "N/A"
           try:
               exe = process.exe()
           except psutil.AccessDenied:
               exe = "Access to full path denied"
           processes.append({
                 'pid': pid, 'name': name,'username': username,'cwd':cwd,'exe':exe,
                 'status': status,'cpu_usage':cpu_usage,'memory_usage':mem_usage,'found_ratio':uptime
           })
    return(processes)
if __name__ == "__main__":
    while(True):
        processes=get_processes_info()
        df = pd.DataFrame(processes)
        total_memory_percent=df['memory_usage'].sum()
        total_cpu_percent=df['cpu_usage'].sum()
        max_cpu = df['cpu_usage'].max()
        df['memory_usage']=df['memory_usage'].apply(get_size)
        max_mem=df['memory_usage'].max()
        df = df[['pid', 'name','username','exe','status','cwd','found_ratio','cpu_usage','memory_usage']]
        df = df[df['found_ratio']<1]
        #df.sort_values(by=['found_ratio'], inplace=True)
        #df=df.iloc[:30]
        os.system("clear")
        print("\n Max CPU(%):",max_cpu," || Max Memory(%):",max_mem," || Total Processes:",len(processes)," || Total CPU(%) Usage:",total_cpu_percent," || Total Memory(%): {:.1f}".format(tot$
        if df.empty == True:
             print("\n No process started in the last 60 seconds")
        else:
             print("\n")
             print(df.to_string(index=False))
        time.sleep(1)
