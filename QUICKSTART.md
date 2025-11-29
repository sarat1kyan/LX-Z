# LX-Z Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
./install.sh
```

### Step 2: Run LX-Z
```bash
./lxz.py
```

### Step 3: For Full Features
```bash
sudo ./lxz.py
```

---

## 📋 Main Menu Options

| Option | Function | Description |
|--------|----------|-------------|
| **1** | CPU Info | Detailed processor information |
| **2** | Memory Info | RAM modules and usage |
| **3** | Storage | Disks and partitions |
| **4** | GPU Info | Graphics card details |
| **5** | Motherboard | BIOS and mainboard info |
| **6** | Sensors | Temperatures and fans |
| **7** | Overview | Complete system summary |
| **8** | Export | Save report to file |
| **0** | Exit | Close the application |

---

## 💡 Pro Tips

### 1. Run with sudo for Best Results
```bash
sudo ./lxz.py
```
This enables:
- DMI memory module information
- SMART disk health data
- Accurate motherboard/BIOS details
- Full sensor readings

### 2. Export System Report
- Select option **8**
- Choose JSON for automation
- Choose TXT for documentation
- Reports saved to `~/lxz_report_*.json/txt`

### 3. Sensor Detection
If temperatures don't show:
```bash
sudo sensors-detect  # Say YES to all
sudo service kmod start
```

### 4. Quick System Check
```bash
# Just CPU info
./lxz.py
# Select option 1, then 0 to exit

# Export and view
./lxz.py
# Select 8 > 2 (TXT) > cat ~/lxz_report_*.txt
```

---

## 🔍 What Information You'll Get

### CPU Section
- ✅ Model and architecture
- ✅ Core/thread count
- ✅ Clock speeds (current/min/max)
- ✅ Cache sizes (L1/L2/L3)
- ✅ CPU features/flags

### Memory Section
- ✅ Total/available/used RAM
- ✅ Swap information
- ✅ Memory module details (with sudo)
- ✅ Speed and manufacturer

### Storage Section
- ✅ All disks (SSD/HDD detection)
- ✅ Partition layout
- ✅ Filesystem types
- ✅ Disk usage
- ✅ SMART health (with sudo)

### GPU Section
- ✅ Graphics card model
- ✅ Driver version
- ✅ VRAM size (NVIDIA)
- ✅ OpenGL/Vulkan support

### Sensors Section
- ✅ CPU temperature
- ✅ GPU temperature
- ✅ Motherboard temp
- ✅ Fan speeds
- ✅ Battery info (laptops)

---

## ⚡ One-Line Commands

```bash
# Install and run
./install.sh && ./lxz.py

# Run with elevated privileges
sudo ./lxz.py

# Export report immediately (requires menu navigation)
# Or use scripting:
python3 -c "from utils.cpu import CPUInfo; print(CPUInfo().get_all_info())"

# Check if all dependencies are installed
lspci --version && dmidecode --version && sensors --version
```

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| `Permission denied` | Run with `sudo ./lxz.py` |
| `rich not found` | `pip3 install rich --break-system-packages` |
| No temperatures | `sudo sensors-detect && sudo service kmod start` |
| Missing GPU info | Install GPU drivers and `lspci` |
| No DMI data | Run with `sudo` |

---

## 📊 Sample Output

```
╦  ═╗ ╦   ╔═╗
║   ╔╝   ╔═╝
╩═╝ ╩    ╚═╝

Linux Hardware Analyzer v1.0

╭─────────────── CPU Information ───────────────╮
│ Processor    │ Intel Core i7-9750H @ 2.60GHz │
│ Architecture │ x86_64                         │
│ Cores        │ 6 cores, 12 threads            │
│ L3 Cache     │ 12 MiB                         │
╰────────────────────────────────────────────────╯
```

---

## 🎯 Common Use Cases

### 1. System Documentation
```bash
sudo ./lxz.py
# Select 8 > 2 (TXT export)
# Share ~/lxz_report_*.txt with support
```

### 2. Pre-Purchase Verification
```bash
# Check hardware before buying used system
sudo ./lxz.py
# Verify CPU, RAM, storage specs
```

### 3. Troubleshooting Overheating
```bash
# Monitor temperatures
sudo ./lxz.py
# Select option 6 (Sensors)
```

### 4. Hardware Inventory
```bash
# Export JSON for database
sudo ./lxz.py
# Select 8 > 1 (JSON)
# Parse ~/lxz_report_*.json
```

---

## 📱 Need Help?

- Check the full [README.md](README.md)
- Open an [issue](https://github.com/sarat1kyan/LX-Z/issues)
- Read [troubleshooting](README.md#-troubleshooting)

---

**Ready to explore your hardware? Run `./lxz.py` now!** 🚀
