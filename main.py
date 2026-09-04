#!/usr/bin/env python3

import os
from modules import ruby_port_scanner

def clear():
    os.system("clear")

def banner():
    print("""\033[96m\033[1m
  ▄▄▄        ▄████ ▓█████▄▄▄█████▓ ██░ ██  ▄▄▄           ▓█████ ▒██   ██▒▓█████    
▒████▄     ██▒ ▀█▒▓█   ▀▓  ██▒ ▓▒▓██░ ██▒▒████▄         ▓█   ▀ ▒▒ █ █ ▒░▓█   ▀    
▒██  ▀█▄  ▒██░▄▄▄░▒███  ▒ ▓██░ ▒░▒██▀▀██░▒██  ▀█▄       ▒███   ░░  █   ░▒███      
░██▄▄▄▄██ ░▓█  ██▓▒▓█  ▄░ ▓██▓ ░ ░▓█ ░██ ░██▄▄▄▄██      ▒▓█  ▄  ░ █ █ ▒ ▒▓█  ▄    
 ▓█   ▓██▒░▒▓███▀▒░▒████▒ ▒██▒ ░ ░▓█▒░██▓ ▓█   ▓██▒ ██▓ ░▒████▒▒██▒ ▒██▒░▒████▒   
 ▒▒   ▓▒█░ ░▒   ▒ ░░ ▒░ ░ ▒ ░░    ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒▓▒ ░░ ▒░ ░▒▒ ░ ░▓ ░░░ ▒░ ░   
  ▒   ▒▒ ░  ░   ░  ░ ░  ░   ░     ▒ ░▒░ ░  ▒   ▒▒ ░ ░▒   ░ ░  ░░░   ░▒ ░ ░ ░  ░   
  ░   ▒   ░ ░   ░    ░    ░       ░  ░░ ░  ░   ▒    ░      ░    ░    ░     ░      
      ░  ░      ░    ░  ░         ░  ░  ░      ░  ░  ░     ░  ░ ░    ░     ░  ░   
                                                     ░                            
 v.alpha0.1                                                       \033[0m""")

def menu():
    clear()
    banner()
    while True:
        print("")
        print("\033[2m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
        print("")
        print("  1) 𝙋𝙤𝙧𝙩 𝙨𝙘𝙖𝙣𝙣𝙚𝙧")
        print("  0) 𝙀𝙭𝙞𝙩")
        print("")
        print("\033[2m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")
        print("")
        choice = input("Choice: ").strip()
        if choice == "1":
            clear()
            ruby_port_scanner.main()
            input("\nPress Enter to return...")
            clear()
            banner()
        elif choice in ("0", "q", "quit", "exit"):
            print("Bye.")
            break
        else:
            print("Ｅｒｒ： ｔｙｐｅ ０－１")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nStopped.")