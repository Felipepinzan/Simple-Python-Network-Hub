import socket
import platform
import psutil
import requests
from ping3 import ping
import speedtest
import time
from datetime import datetime


def get_local_info():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    system_info = platform.platform()
    return hostname, local_ip, system_info

def get_public_info():
    try:
        data = requests.get("http://ip-api.com/json", timeout=5).json()
        return {
            "ip": data.get("query"),
            "isp": data.get("isp"),
            "city": data.get("city"),
            "country": data.get("country"),
            "timezone": data.get("timezone"),
        }
    except:
        return None

def check_ping(host="8.8.8.8"):
    try:
        latency = ping(host, timeout=2)
        if latency is not None:
            return round(latency * 1000, 2)  # ms
        return None
    except:
        return None

def speed_test():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = round(st.download() / 1_000_000, 2)  # Mbps
        upload = round(st.upload() / 1_000_000, 2)      # Mbps
        ping_val = st.results.ping
        return download, upload, ping_val
    except:
        return None, None, None

def get_network_usage():
    counters = psutil.net_io_counters()
    sent = round(counters.bytes_sent / 1_000_000, 2)  # MB
    recv = round(counters.bytes_recv / 1_000_000, 2)  # MB
    return sent, recv

# display

def main():
    for _ in range(5):
        print('')
    print("Network Information Hub")
    print("────────────────────────────")
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Local info
    hostname, local_ip, system_info = get_local_info()
    print(f"💻 Hostname: {hostname}")
    print(f"🏠 Local IP: {local_ip}")
    print(f"🖥️ System: {system_info}")
    print()

    # Public info
    public_info = get_public_info()
    if public_info:
        print(f"🌐 Public IP: {public_info['ip']}")
        print(f"🏢 ISP: {public_info['isp']}")
        print(f"📍 Location: {public_info['city']}, {public_info['country']}")
        print(f"🕒 Timezone: {public_info['timezone']}")
    else:
        print("⚠️ Could not fetch public IP/ISP info")
    print()

    # Ping test
    latency = check_ping()
    if latency is not None:
        print(f"📶 Ping to 8.8.8.8: {latency} ms")
    else:
        print("⚠️ Ping failed")
    print()

    # Speed test
    print("⏳ Running speed test (may take ~30s)...")
    download, upload, speed_ping = speed_test()
    if download is not None:
        print(f"⬇️ Download: {download} Mbps")
        print(f"⬆️ Upload: {upload} Mbps")
        print(f"📶 Speedtest Ping: {speed_ping} ms")
    else:
        print("⚠️ Speed test failed")
    print()

    # Network usage
    sent, recv = get_network_usage()
    print(f"📤 Data Sent: {sent} MB")
    print(f"📥 Data Received: {recv} MB")

if __name__ == "__main__":
    main()
