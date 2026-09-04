import socket # TCP + DNS
import sys # tty
import time # duration
from concurrent.futures import ThreadPoolExecutor, as_completed

# PC assumes truecolor terminal, no Termux fallback needed
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def banner(): # PC wide logo, keep your art
    print(MAGENTA + BOLD + r"""
   ___  __  _______  ___  ____  ___  ____  ___  ______  ____________   _  ___  _________ 
  / _ \/ / / / _ ) \/ ( )/ __/ / _ \/ __ \/ _ \/_  __/ / __/ ___/ _ | / |/ / |/ / __/ _ \
 / , _/ /_/ / _  |\  /|/_\ \  / ___/ /_/ / , _/ / /   _\ \/ /__/ __ |/    /    / _// , _/
/_/|_|\____/____/ /_/  /___/ /_/   \____/_/|_| /_/   /___/\___/_/ |_/_/|_/_/|_/___/_/|_| 
                                                                                         
""" + RESET)
    print(DIM + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + RESET)
    print("")
def clean_target(raw):
    s = raw.strip()
    if "://" in s:
        s = s.split("://", 1)[1]
    s = s.split("/")[0]
    s = s.split(":")[0]
    return s.strip().lower()

normal_ports = [21,22,23,80,443,8080]
medium_ports = [21,22,23,80,443,8080,25,53,67,68,69,88,110,111,123,135,137,139,143,161,389,445,465,514,587,631,636,993,995,1080,1433,1521,1723,2049,2082,2083,3306,3389,5432,5900,6379,8000,8443,8888,9000,27017,5000,3000,1194,1900]
high_ports = [21,22,23,80,443,8080,25,53,67,68,69,88,110,111,123,135,137,139,143,161,389,445,465,514,587,631,636,993,995,1080,1433,1521,1723,2049,2082,2083,3306,3389,5432,5900,6379,8000,8443,8888,9000,27017,5000,3000,1194,1900,5353,2375,5901,8081,10000,11211,81,82,83,8008,8010,8028,8088,8090,8100,8181,8280,8880,9001,9002,9080,9090,9091,9100,8001,8002,8011,8091,8099,8123,1434,3050,50000,27018,27019,6380,9042,9160,7474,7687,8529,9200,9300,15672,5672,61616,2181,9092,6378,5984,2222,2000,2001,5800,5902,5903,5985,5986,3388,3390,2200,512,513,543,544,8291,8728,10011,1311,4786,500,4500,1701,1812,1813,162,199,427,546,547,51820,3128,8118,3260,3268,3269,464,749,750,520,7547,2323,6667,1883,8883,5683,554,8554,1935,5357,515,9101,5060,5061,3478,5349,1720,2427,6881,6969,25565,27015,27016,9987,25575,3074,3724,7777,19132,9418,2376,6443,10250,2379,2380,4505,4506,5666,5601,4040,4000,4001,4567,5001,5050,7000,7001,7443,4568,4444,42,43,102,113,119,179,873,1025,1026,1027]
top1000_ports = high_ports + [p for p in range(1, 1025) if p not in set(high_ports)][:800]

speeds = {
    "1": ("Normal", 1.0, 50),
    "2": ("Fast", 0.5, 150),
    "3": ("Super", 0.3, 300),
}

def scan_port(host, port, timeout=1.0):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return port, True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return port, False

def print_scan_menu():
    print(BOLD + MAGENTA + "╭─ SELECT SCAN ──────────────────────╮" + RESET)
    print("│  1) Normal   [6 ports]             │")
    print("│  2) Medium   [50 ports]            │")
    print("│  3) High     [200 ports]           │")
    print(f"│  4) Top      [1000 ports] {YELLOW}(!){RESET}      │")
    print(f"│  5) All      [65535 ports] {YELLOW}(!){RESET}     │")
    print(BOLD + MAGENTA + "╰────────────────────────────────────╯" + RESET)
    print(DIM + "!: scanning all ports may take 10-20 min" + RESET)

def print_speed_menu():
    print(BOLD + MAGENTA + "╭─ SELECT SPEED ─────────────────────╮" + RESET)
    print("│  1) Normal  [safe]                 │")
    print("│  2) Fast    [fast]                 │")
    print("│  3) Super   [aggressive]           │")
    print(BOLD + MAGENTA + "╰────────────────────────────────────╯" + RESET)
    print(DIM + "!: higher speeds may rate-limit your ip" + RESET)

def scan(host, ports, workers=50, timeout=1.0):
    host = clean_target(host)
    try:
        target = socket.gethostbyname(host)
    except socket.gaierror:
        print(RED + "Host undefined" + RESET)
        return
    print(f"{DIM}Target:{RESET} {BOLD}{CYAN}{target}{RESET} {DIM}[{len(ports)} ports | {workers} thr | {timeout}s]{RESET}")

    open_ports = []
    total = len(ports)
    done = 0
    start = time.time()

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(scan_port, target, p, timeout) for p in ports]
        for f in as_completed(futures):
            port, is_open = f.result()
            if is_open:
                open_ports.append(port)
            done += 1
            filled = done * 20 // total  # PC: 20 block bar
            percent = done * 100 // total
            bar = "█" * filled + "░" * (20 - filled)
            print(f"\r{YELLOW}[{bar}]{RESET} {percent:>3}%", end="", flush=True)

    elapsed = time.time() - start
    print()
    print(DIM + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + RESET)
    if open_ports:
        print(BOLD + f"{'PORT':<11} {'SERVICE':<12} STATE" + RESET)
        for p in sorted(open_ports):
            try:
                name = socket.getservbyport(p, "tcp")
            except OSError:
                name = "unknown"
            print(f"{GREEN}{str(p)+'/tcp':<11} {name:<12} open [+]{RESET}")
        print(DIM + f"{len(open_ports)} open in {elapsed:.1f}s" + RESET)
    else:
        print(RED + "─ No open ports found ─" + RESET)
    print(DIM + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + RESET)

def main():
    banner()
    while True:
        target_input = input(f"{BOLD}{CYAN}Target IP/domain:{RESET} ").strip()
        if not target_input:
            continue
        if target_input.lower() in ("q", "quit", "exit", "0"):
            break
        print_scan_menu()
        c = input(f"{BOLD}Choice:{RESET} ").strip()
        if c in ("0", "q", "quit", "exit"):
            print("Bye.")
            break
        if c not in ("1", "2", "3", "4", "5"):
            print(RED + "Err: type 0-5" + RESET)
            continue
        print_speed_menu()
        s = input(f"{BOLD}Speed:{RESET} ").strip()
        if s not in speeds:
            print(RED + "Err: type 1-3" + RESET)
            continue
        _, timeout, workers = speeds[s]
        if c == "1":
            scan(target_input, normal_ports, workers, timeout)
        elif c == "2":
            scan(target_input, medium_ports, workers, timeout)
        elif c == "3":
            scan(target_input, high_ports, workers, timeout)
        elif c == "4":
            scan(target_input, top1000_ports, workers, timeout)
        elif c == "5":
            scan(target_input, range(1, 65536), workers, timeout)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")