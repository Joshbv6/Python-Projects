import pywhatkit
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
  # returns our WiFi IPv4
  return IP

if __name__ == '__main__':
    
    ip = get_ip()

    print("\r\nServer running at: http://%s:8000\r\n" %ip) 

    pywhatkit.start_server()
