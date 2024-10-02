import psutil
import pandas as pd
import time
import seaborn as sns
from pynput import keyboard
import matplotlib.pyplot as plt

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
        print("\033[H\033[J", end="") #Cleaning screen...
        list_connections()
        df = pd.DataFrame(data={'pid': pids_array, 'name': names_array, 'ip': raddr_ip_array, 'port': raddr_port_array})
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)

        # --- Plotting the statistics ---
        # plt.figure(figsize=(10, 6))  # Adjust figure size as needed
        # sns.countplot(y='name', data=df, order=df['name'].value_counts().index)
        # plt.title('Number of Unique IPs Used by Each Process')
        # plt.xlabel('Number of Unique IPs')
        # plt.ylabel('Process Name')
        # plt.tight_layout() 
        # plt.show()

        df_sorted_by_name = df.groupby('name')
        # Print all IPs used by each process
        df_sorted_by_name.apply(lambda x: print(f"Process: {x.name}, IPs: {x['ip'].tolist()}"), include_groups=False)
        time.sleep(1)
