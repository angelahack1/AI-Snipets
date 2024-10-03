import socket
import psutil
import pandas as pd
import time
from pynput import keyboard


def on_press(key):
    if key == keyboard.Key.esc:
        return False  # Stop listener

pids_array = []
names_array = []
raddr_ip_array = []
raddr_port_array = []

def get_process_name_by_pid(pid):
    try:
        process = psutil.Process(pid)
        return process.name()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return "N/A"

def list_connections():
    counter = 0
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'ESTABLISHED' and conn.raddr.ip != '127.0.0.1' and conn.raddr.ip != '::1':
            process_name = get_process_name_by_pid(conn.pid) if conn.pid else "N/A"
            pids_array.append(conn.pid)
            names_array.append(process_name)
            raddr_ip_array.append(conn.raddr.ip)
            raddr_port_array.append(conn.raddr.port)
            counter += 1
    print('Number of connections ESTABLISHED: ', counter)

if __name__ == '__main__':
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    while listener.is_alive(): 
        list_connections()
        df = pd.DataFrame(data={'pid': pids_array, 'name': names_array, 'ip': raddr_ip_array, 'port': raddr_port_array})
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        df_sorted_by_name = df.groupby('name')
        # Print all IPs used by each process
        for name, group in df_sorted_by_name:
            if name != 'lsass.exe' and name != 'POWERPNT.EXE' and name != 'OfficeClickToRun.exe' and name != 'OUTLOOK.EXE' and name != 'smartscreen.exe' and name != 'msedgewebview2.exe' and name != 'MpDefenderCoreService.exe' and name != 'BrokerAgent.exe' and name != 'svchost.exe' and name != 'CcmExec.exe' and name != 'System' and name != 'chrome.exe' and name != 'spoolsv.exe' and name != 'splunkd.exe' and name != 'EmaAgent.exe' and name != 'HealthService.exe' and name != 'Parity.exe' and name != 'PicaSvc2.exe' and name != 'cloudcode_cli.exe' and name != 'msedge.exe':
                print(f"\n-------------------------------------------------Process: {name}----------------------------------------------------------")
                ip_list = group['ip'].tolist()
                for ip in ip_list:
                    try:
                        # Perform reverse DNS lookup to get the hostname
                        hostname = socket.gethostbyaddr(ip)[0]
                        print(f"Process: {name}, IP: {ip}, Hostname: {hostname}")
                    except socket.herror:
                        print(f"Process: {name}, IP: {ip}, Hostname: Unknown")
                    # Perform port lookup to get the service name
                    # for port in group['port'].tolist():
                    #    try:
                    #        service_name = socket.getservbyport(port)
                    #        print(f"Process: {name}, IP: {ip}, Port: {port}, Service: {service_name}")
                    #    except socket.error:
                    #        print(f"Process: {name}, IP: {ip}, Port: {port}, Service: Unknown")
        pids_array = []
        names_array = []
        raddr_ip_array = []
        raddr_port_array = []
        time.sleep(1)

