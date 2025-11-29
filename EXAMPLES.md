# LX-Z Usage Examples & Tips

## 📚 Complete Usage Guide

### Installation Examples

#### Ubuntu/Debian Example
```bash
# Full installation with all features
git clone https://github.com/sarat1kyan/LX-Z.git
cd LX-Z
chmod +x install.sh
./install.sh

# Verify installation
./lxz.py --version 2>/dev/null || ./lxz.py
```

#### RHEL/CentOS/Fedora Example
```bash
# Clone and install
git clone https://github.com/sarat1kyan/LX-Z.git
cd LX-Z
chmod +x install.sh
sudo ./install.sh

# Create system-wide alias
echo "alias lxz='sudo /path/to/LX-Z/lxz.py'" >> ~/.bashrc
source ~/.bashrc
```

#### Arch Linux Example
```bash
# Clone and install
git clone https://github.com/sarat1kyan/LX-Z.git
cd LX-Z
chmod +x install.sh
./install.sh

# Optional AUR packaging (future feature)
# makepkg -si
```

---

## 🎮 Interactive Mode Examples

### Example 1: Quick CPU Check
```bash
$ ./lxz.py
# Press 1 (CPU Information)
# View detailed CPU specs
# Press Enter to return
# Press 0 to exit
```

### Example 2: Complete System Audit
```bash
$ sudo ./lxz.py
# Press 7 (Complete System Overview)
# View all system information at once
# Press 8 to export
# Select 3 (Both formats)
```

### Example 3: Temperature Monitoring
```bash
$ sudo ./lxz.py
# Press 6 (Sensors & Hardware Monitor)
# Check temperatures and fan speeds
# Exit and rerun to see changes
```

---

## 🔧 Command-Line Integration

### Scripting Examples

#### Extract CPU Model
```python
#!/usr/bin/env python3
from utils.cpu import CPUInfo

cpu = CPUInfo()
info = cpu.get_all_info()
print(f"CPU: {info['model']}")
print(f"Cores: {info['cores']}")
print(f"Threads: {info['threads']}")
```

#### Check Available RAM
```python
#!/usr/bin/env python3
from utils.memory import MemoryInfo

mem = MemoryInfo()
info = mem.get_all_info()
print(f"Total RAM: {info['total']}")
print(f"Available: {info['available']}")
print(f"Usage: {info['percent']}")
```

#### List All Storage Devices
```python
#!/usr/bin/env python3
from utils.storage import StorageInfo

storage = StorageInfo()
info = storage.get_all_info()

print("Storage Devices:")
for device in info['devices']:
    print(f"  {device['name']}: {device['size']} ({device['type']})")
```

#### Export System Report
```python
#!/usr/bin/env python3
from utils.cpu import CPUInfo
from utils.memory import MemoryInfo
from utils.storage import StorageInfo
from utils.gpu import GPUInfo
from utils.sensors import SensorInfo
from utils.exporter import ExportReport

# Gather all data
data = {
    'cpu': CPUInfo().get_all_info(),
    'memory': MemoryInfo().get_all_info(),
    'storage': StorageInfo().get_all_info(),
    'gpu': GPUInfo().get_all_info(),
    'sensors': SensorInfo().get_all_info(),
}

# Export
exporter = ExportReport()
json_file = exporter.export_json(data, 'my_system_report.json')
txt_file = exporter.export_txt(data, 'my_system_report.txt')

print(f"Reports saved:")
print(f"  JSON: {json_file}")
print(f"  TXT: {txt_file}")
```

---

## 🔄 Automation Examples

### Cron Job for Daily Reports
```bash
# Add to crontab (crontab -e)
0 2 * * * /path/to/LX-Z/lxz.py --export-json /var/log/system_reports/daily_$(date +\%Y\%m\%d).json

# Note: Requires non-interactive export feature (future enhancement)
```

### Temperature Monitoring Script
```bash
#!/bin/bash
# monitor_temps.sh - Log temperatures every minute

while true; do
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    temps=$(python3 -c "
from utils.sensors import SensorInfo
import json
sensor = SensorInfo()
info = sensor.get_all_info()
print(json.dumps(info.get('temperatures', {})))
")
    echo "[$timestamp] $temps" >> temp_log.txt
    sleep 60
done
```

### System Inventory Database
```python
#!/usr/bin/env python3
# inventory.py - Build hardware inventory database

import json
import socket
from datetime import datetime
from utils.cpu import CPUInfo
from utils.memory import MemoryInfo
from utils.storage import StorageInfo

def get_system_inventory():
    return {
        'hostname': socket.gethostname(),
        'timestamp': datetime.now().isoformat(),
        'cpu': CPUInfo().get_summary(),
        'memory': MemoryInfo().get_summary(),
        'storage': StorageInfo().get_summary(),
    }

if __name__ == '__main__':
    inventory = get_system_inventory()
    
    # Save to JSON
    with open(f'inventory_{socket.gethostname()}.json', 'w') as f:
        json.dump(inventory, f, indent=2)
    
    print(f"Inventory saved for {inventory['hostname']}")
```

---

## 📊 Report Examples

### JSON Report Structure
```json
{
  "generated_at": "2024-11-29T10:30:00",
  "generator": "LX-Z v1.0",
  "system_info": {
    "cpu": {
      "model": "Intel Core i7-9750H CPU @ 2.60GHz",
      "architecture": "x86_64",
      "cores": 6,
      "threads": 12,
      "current_freq": "2600.00 MHz",
      "l3_cache": "12 MiB"
    },
    "memory": {
      "total": "16.00 GB",
      "available": "8.50 GB",
      "used": "7.50 GB",
      "percent": "46.9%"
    },
    "storage": {
      "devices": [
        {
          "name": "nvme0n1",
          "size": "512.00 GB",
          "type": "SSD"
        }
      ]
    }
  }
}
```

### Text Report Example
```
================================================================================
LX-Z - Linux Hardware Analyzer Report
================================================================================
Generated: 2024-11-29 10:30:00
================================================================================

CPU INFORMATION
================================================================================
Model: Intel Core i7-9750H CPU @ 2.60GHz
Architecture: x86_64
Cores: 6
Threads: 12
Current Frequency: 2600.00 MHz
L3 Cache: 12 MiB

MEMORY INFORMATION
================================================================================
Total RAM: 16.00 GB
Available RAM: 8.50 GB
Used RAM: 7.50 GB
Usage: 46.9%
```

---

## 🚀 Performance Tips

### 1. Faster Startup
```bash
# Skip unnecessary checks by running specific modules
python3 -c "from utils.cpu import CPUInfo; print(CPUInfo().get_summary())"
```

### 2. Minimal Dependencies Mode
```bash
# If you only need basic info, you can disable rich formatting
export TERM=dumb
./lxz.py
```

### 3. Batch Processing
```bash
# Process multiple systems
for host in server1 server2 server3; do
    ssh $host "cd /opt/LX-Z && sudo ./lxz.py" > ${host}_report.txt
done
```

---

## 🐛 Debugging Examples

### Enable Verbose Output
```python
# Add to lxz.py for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components
```bash
# Test CPU detection
python3 -c "from utils.cpu import CPUInfo; import json; print(json.dumps(CPUInfo().get_all_info(), indent=2))"

# Test memory detection
python3 -c "from utils.memory import MemoryInfo; import json; print(json.dumps(MemoryInfo().get_all_info(), indent=2))"

# Test storage detection
python3 -c "from utils.storage import StorageInfo; import json; print(json.dumps(StorageInfo().get_all_info(), indent=2))"

# Test GPU detection
python3 -c "from utils.gpu import GPUInfo; import json; print(json.dumps(GPUInfo().get_all_info(), indent=2))"

# Test sensor detection
python3 -c "from utils.sensors import SensorInfo; import json; print(json.dumps(SensorInfo().get_all_info(), indent=2))"
```

---

## 🎯 Real-World Use Cases

### Use Case 1: IT Asset Management
```bash
# Run on all servers and collect reports
#!/bin/bash
for server in $(cat servers.txt); do
    echo "Collecting from $server..."
    ssh root@$server "cd /opt/LX-Z && ./lxz.py" > reports/${server}.json
done

# Parse and import to database
python3 import_to_db.py reports/*.json
```

### Use Case 2: Pre-Purchase Hardware Verification
```bash
# Verify seller's claims about used system
sudo ./lxz.py
# Press 7 for overview
# Press 8 to export
# Compare with advertised specs
```

### Use Case 3: Thermal Troubleshooting
```bash
# Monitor temperatures during stress test
watch -n 1 'python3 -c "from utils.sensors import SensorInfo; s=SensorInfo(); print(s.get_all_info().get(\"temperatures\", {}))"'

# Run stress test in another terminal
stress-ng --cpu 8 --timeout 300s
```

### Use Case 4: Server Documentation
```bash
# Generate documentation for new server
sudo ./lxz.py
# Export as TXT
# Add to server documentation wiki
```

---

## 🔐 Security Considerations

### Running with Minimal Privileges
```bash
# For read-only access without sudo
./lxz.py  # Still provides useful info

# Add user to specific groups for more access
sudo usermod -aG disk,lp $USER  # For storage and sensor access
```

### Sensitive Information
```bash
# Scrub serial numbers from reports
sed -i 's/Serial Number: .*/Serial Number: [REDACTED]/' report.txt

# Or use environment variable
export LXZ_HIDE_SERIAL=1
```

---

## 💻 Integration Examples

### REST API Wrapper
```python
#!/usr/bin/env python3
from flask import Flask, jsonify
from utils.cpu import CPUInfo
from utils.memory import MemoryInfo

app = Flask(__name__)

@app.route('/api/cpu')
def get_cpu():
    return jsonify(CPUInfo().get_all_info())

@app.route('/api/memory')
def get_memory():
    return jsonify(MemoryInfo().get_all_info())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Monitoring Integration (Prometheus)
```python
#!/usr/bin/env python3
from prometheus_client import start_http_server, Gauge
from utils.sensors import SensorInfo
import time

# Create metrics
cpu_temp = Gauge('cpu_temperature_celsius', 'CPU Temperature')
ram_usage = Gauge('memory_usage_percent', 'RAM Usage Percentage')

def collect_metrics():
    sensors = SensorInfo().get_all_info()
    temps = sensors.get('temperatures', {})
    
    # Extract CPU temp (adjust key based on your system)
    for key, value in temps.items():
        if 'CPU' in key or 'Core' in key:
            temp_value = float(value.replace('°C', '').strip())
            cpu_temp.set(temp_value)
            break

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        collect_metrics()
        time.sleep(60)
```

---

## 📈 Advanced Features

### Custom Report Templates
```python
#!/usr/bin/env python3
# custom_report.py

from utils.cpu import CPUInfo
from utils.memory import MemoryInfo
import jinja2

template = """
# System Report: {{ hostname }}

## CPU
- Model: {{ cpu.model }}
- Cores: {{ cpu.cores }}

## Memory
- Total: {{ memory.total }}
- Available: {{ memory.available }}
"""

cpu = CPUInfo().get_all_info()
memory = MemoryInfo().get_all_info()

tmpl = jinja2.Template(template)
report = tmpl.render(
    hostname='my-server',
    cpu=cpu,
    memory=memory
)

print(report)
```

---

**For more examples and advanced usage, check the [README.md](README.md)!**
