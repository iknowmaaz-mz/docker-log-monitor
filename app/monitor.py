import psutil
import time
import os
from datetime import datetime
LOG_FILE = "/app/logs/metrics.log"
CPU_THRESHOLD = float(os.getenv("CPU_THRESHOLD", 80))
MEM_THRESHOLD = float(os.getenv("MEM_THRESHOLD", 80))
DISK_THRESHOLD = float(os.getenv("DISK_THRESHOLD", 80))
INTERVAL = int(os.getenv("INTERVAL", 10))
os.makedirs("/app/logs", exist_ok=True)
def get_metrics():
cpu = psutil.cpu_percent(interval=1)
mem = psutil.virtual_memory().percent
disk = psutil.disk_usage("/").percent
return cpu, mem, disk
def check_alerts(cpu, mem, disk):
alerts = []
if cpu > CPU_THRESHOLD:
alerts.append("CPU usage critical: " + str(cpu) + "%")
if mem > MEM_THRESHOLD:
alerts.append("Memory usage critical: " + str(mem) + "%")
if disk > DISK_THRESHOLD:
alerts.append("Disk usage critical: " + str(disk) + "%")
return alerts
def log_metrics():
while True:
cpu, mem, disk = get_metrics()
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_entry = "[" + timestamp + "] CPU: " + str(cpu) + "% | MEM: " + str(mem) + "% | DISK: " + str(disk) + "%"
alerts = check_alerts(cpu, mem, disk)
if alerts:
log_entry += " | ALERTS: " + "; ".join(alerts)
with open(LOG_FILE, "a") as f:
f.write(log_entry + "\n")
print(log_entry)
time.sleep(INTERVAL)
if __name__ == "__main__":
log_metrics()