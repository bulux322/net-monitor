import subprocess
import time
import datetime
import platform
import re

INTERVAL = 1
WINDOW_SIZE = 20
RTO_LATENCY_THRESHOLD = 200

target = "8.8.8.8"
running = False

history = []
latency_history = []

def set_target(t):
    global target
    target = t or "8.8.8.8"

def stop_monitor():
    global running
    running = False

def ping():
    system = platform.system().lower()
    cmd = ["ping", "-n", "1", target] if system == "windows" else ["ping", "-c", "1", target]

    start = time.time()
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )
    process_latency = round((time.time() - start) * 1000, 2)

    icmp_latency = None
    if result.returncode == 0:
        if system == "windows":
            match = re.search(r"time[=<]\s*(\d+)", result.stdout)
        else:
            match = re.search(r"time=(\d+\.?\d*)", result.stdout)

        if match:
            icmp_latency = float(match.group(1))

    return result.returncode == 0, icmp_latency, process_latency

def smart_status(latency, packet_loss, jitter, ok):
    if not ok:
        return "DOWN"

    if packet_loss < 1 and jitter < 10 and latency < 80:
        return "STABLE"

    if packet_loss < 5 and jitter < 30 and latency < 200:
        return "LAG"

    return "BAD"

def start_monitor(socketio):
    global running
    if running:
        return

    running = True
    print(f"Monitoring started → {target}")

    while running:
        ok, icmp_latency, process_latency = ping()
        ts = datetime.datetime.now().strftime("%H:%M:%S")

        # packet loss window
        history.append(1 if ok else 0)
        if len(history) > WINDOW_SIZE:
            history.pop(0)

        packet_loss = round((1 - sum(history) / len(history)) * 100, 1)

        # latency history (ICMP only)
        if ok and icmp_latency is not None:
            latency_history.append(icmp_latency)
            if len(latency_history) > WINDOW_SIZE:
                latency_history.pop(0)

        # jitter
        jitter = (
            abs(latency_history[-1] - latency_history[-2])
            if len(latency_history) >= 2 else 0
        )

        # RTO
        rto = sum(1 for l in latency_history if l > RTO_LATENCY_THRESHOLD)
        if not ok:
            rto += 1

        # SMART STATUS (PAKAI ICMP)
        status = smart_status(
            icmp_latency if icmp_latency is not None else 999,
            packet_loss,
            jitter,
            ok
        )

        socketio.emit("ping_data", {
            "time": ts,
            "icmp_latency": icmp_latency,
            "process_latency": process_latency,
            "packet_loss": packet_loss,
            "jitter": round(jitter, 2),
            "rto": rto,
            "target": target,
            "status": status
        })

        socketio.sleep(INTERVAL)