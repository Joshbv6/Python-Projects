# import module
import os
import signal
import subprocess
import time
import win32com.shell.shell as shell
from tqdm import tqdm

tries = 0

def handler(signum, frame):

    print("\r\nAle!!\r\nSure! We're not connecting anywhere!")

    exit(1)

signal.signal(signal.SIGINT, handler) 

def get_wifi_list():
    return subprocess.check_output(f'cmd /c "netsh wlan show network mode=Bssid"', shell=True)

def get_signal(ssid, wifi_available):
    wifi_available = wifi_available.split('\n')
    for i in range(len(wifi_available)):
        if ssid in wifi_available[i]:
            for line in wifi_available[i:]:
                print(line)
                if 'Signal' in line or 'Señal' in line or 'Se¤al' in line:
                    signal_strength = line.split(':')[1].strip()
                    return int(signal_strength.strip(' \t\n\r%'))
    return None

def restart_adapter():
    command = 'netsh interface set interface name="Wi-Fi" admin=disabled'

    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+command)
    #subprocess.call('C:\Windows\System32\powershell.exe Restart-NetAdapter -Name "Wi-Fi"', shell=True)

    time.sleep(1.5)

    command_enable = 'netsh interface set interface name="Wi-Fi" admin=enabled'

    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+command_enable)

    for i in tqdm (range (100),desc="Restarting Network Adapter…", ascii=False, ncols=75):
        time.sleep(0.08)

    print("\r\nNetwork Adapter restarted succesfully.\r\n")

def connect(network, strenght):
    subprocess.check_output('cmd /c "netsh wlan disconnect && netsh wlan connect "' + network, shell=True)
    print("\r\nKnown wifi network...\r\n")
    print(f"\r\nConnecting to: {network} with a {strenght}% of intensity\r\n")
    os.system(f'''cmd /c "netsh wlan connect name="''' + network)
    time.sleep(2)
    exit(1)

def Wifi_Connection(tries = False):

    tries = tries + 1

    print("\r\nWifi Connection nº %i \r\n" %tries)

    print("\r\nRestarting Network Adapter\r\n")

    restart_adapter()

    wifi_signal = {}

    wifi_available = get_wifi_list()

    wifi_know = ["list of known SSID"]


    while not wifi_available:

        wifi_available = get_wifi_list()

    print(wifi_available)

    for wifi in wifi_know:
        if(wifi in wifi_available):
            wifi_signal[wifi] = get_signal(wifi, wifi_available)
            continue

        if(wifi not in wifi_available):
            continue

    if len(wifi_signal) == 0:
        if tries < 3:
            print('\r\nNo available and known network found, trying again.\r\n')
            time.sleep(2)
            Wifi_Connection(tries)

        else:
            print("\r\Process could not find available and known network found.\r\n\r\nPlease be sure to got a known network near.")
            exit(1)
    else:
        network = max(wifi_signal, key=wifi_signal.get)
        strenght = wifi_signal[network]
    
    connect(network, strenght)



if __name__ == "__main__":

    Wifi_Connection(0) 
