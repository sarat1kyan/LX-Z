# LX-Z - Linux Hardware Analyzer

<div align="center">

```
╦  ═╗ ╦   ╔═╗
║   ╔╝   ╔═╝
╩═╝ ╩    ╚═╝
```

**A professional CPU-Z alternative for Linux systems**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Linux](https://img.shields.io/badge/platform-Linux-green.svg)](https://www.linux.org/)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Supported Distributions](#-supported-distributions)
- [Installation](#-installation)
- [Usage](#-usage)
- [System Requirements](#-system-requirements)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**LX-Z** is a comprehensive, professional-grade hardware information tool for Linux systems, designed to be the definitive alternative to CPU-Z on Windows. It provides detailed information about your system's hardware components with a beautiful, interactive command-line interface.

### Why LX-Z?

- ✨ **Beautiful CLI Interface** - Modern, colorful, and intuitive interface powered by Rich
- 🔍 **Comprehensive Hardware Detection** - CPU, RAM, Storage, GPU, Sensors, and more
- 🚀 **Multi-Distribution Support** - Works on Ubuntu, Debian, RHEL, CentOS, Fedora, and Arch
- 📊 **Export Capabilities** - Generate JSON and TXT reports for documentation
- ⚡ **Fast & Lightweight** - Minimal dependencies, maximum performance
- 🛡️ **No Root Required** - Basic functionality works without sudo (enhanced features need root)

---

## 🚀 Features

### CPU Information
- **Basic Details**: Model, architecture, vendor, family, stepping
- **Core Configuration**: Physical cores, logical processors, sockets
- **Frequency**: Current, minimum, and maximum clock speeds
- **Cache**: L1 (data/instruction), L2, and L3 cache sizes
- **Capabilities**: Complete CPU flags and feature set (SSE, AVX, virtualization, etc.)

### Memory (RAM) Information
- **Overview**: Total, available, used, and free RAM
- **Swap**: Complete swap space information and usage
- **Memory Modules**: Detailed information from DMI (requires root)
  - Size, type, speed, manufacturer
  - Physical slot location
  - Part numbers and serial numbers

### Storage Information
- **Block Devices**: All storage devices (HDD/SSD detection)
- **Device Details**: Model, size, type, read-only status
- **Partitions**: Complete filesystem information
  - Mount points, filesystem types
  - Size, usage, and availability
- **SMART**: Health status monitoring (if available)

### GPU Information
- **Graphics Cards**: All installed GPUs
- **Details**: Vendor, model, driver information
- **VRAM**: Memory size (NVIDIA GPUs)
- **API Support**: OpenGL and Vulkan versions

### Motherboard & BIOS
- **Motherboard**: Manufacturer, model, version, serial number
- **BIOS/UEFI**: Vendor, version, release date

### Sensors & Hardware Monitoring
- **Temperature**: CPU, GPU, and motherboard temperatures
- **Fan Speeds**: All system fan RPM readings
- **Battery**: Comprehensive laptop battery information
  - Capacity, status, energy levels
  - Manufacturer and model

### Export & Reporting
- **JSON Export**: Machine-readable format for automation
- **TXT Export**: Human-readable detailed reports
- **Timestamped**: Auto-generated filenames with timestamps

---

## 📸 Screenshots

### Main Menu
```
╦  ═╗ ╦   ╔═╗
║   ╔╝   ╔═╝
╩═╝ ╩    ╚═╝

Linux Hardware Analyzer v1.0
A professional CPU-Z alternative for Linux

╭───────────────────────────────────────────╮
│              Main Menu                     │
├───────┬───────────────────────────────────┤
│  [1]  │ 🔹 CPU Information                 │
│  [2]  │ 🔹 Memory (RAM) Information        │
│  [3]  │ 🔹 Storage Devices                 │
│  [4]  │ 🔹 GPU Information                 │
│  [5]  │ 🔹 Motherboard & BIOS              │
│  [6]  │ 🔹 Sensors & Hardware Monitor      │
│  [7]  │ 🔹 Complete System Overview        │
│  [8]  │ 🔹 Export Report (JSON/TXT)        │
│  [0]  │ 🔹 Exit                            │
╰───────┴───────────────────────────────────╯
```

---

## 🐧 Supported Distributions

LX-Z has been tested and works on the following Linux distributions:

| Distribution | Version | Package Manager | Status |
|-------------|---------|-----------------|--------|
| Ubuntu | 18.04+ | APT | ✅ Tested |
| Debian | 9+ | APT | ✅ Tested |
| Linux Mint | 19+ | APT | ✅ Compatible |
| RHEL | 7+ | YUM/DNF | ✅ Tested |
| CentOS | 7+ | YUM/DNF | ✅ Tested |
| Rocky Linux | 8+ | DNF | ✅ Compatible |
| Fedora | 30+ | DNF | ✅ Tested |
| Arch Linux | Rolling | Pacman | ✅ Tested |
| Manjaro | Rolling | Pacman | ✅ Compatible |

### Compatibility Notes
- **Kernel**: Linux kernel 4.x and 5.x+ supported
- **VM Support**: Works in both virtual machines and bare-metal
- **ARM**: Basic support (some features may be limited)

---

## 📦 Installation

### Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/sarat1kyan/LX-Z.git
cd LX-Z

# Run the installation script
chmod +x install.sh
./install.sh

# Run LX-Z
./lxz.py
```

### Manual Installation

#### 1. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y lshw hwinfo dmidecode smartmontools \
    lm-sensors pciutils usbutils util-linux mesa-utils
```

**RHEL/CentOS/Fedora:**
```bash
sudo dnf install -y lshw hwinfo dmidecode smartmontools \
    lm_sensors pciutils usbutils util-linux mesa-demos
```

**Arch Linux:**
```bash
sudo pacman -S lshw hwinfo dmidecode smartmontools \
    lm_sensors pciutils usbutils util-linux mesa-demos
```

#### 2. Install Python Dependencies

```bash
pip3 install rich --break-system-packages
# Or
pip3 install -r requirements.txt --break-system-packages
```

#### 3. Make Executable

```bash
chmod +x lxz.py
```

#### 4. Optional: Create System-wide Link

```bash
sudo ln -s $(pwd)/lxz.py /usr/local/bin/lxz
```

---

## 🎮 Usage

### Basic Usage

```bash
# Run from installation directory
./lxz.py

# Or if you created a symlink
lxz
```

### Advanced Usage (Recommended)

For full functionality, including DMI information, SMART data, and detailed sensors:

```bash
sudo ./lxz.py
```

### Navigation

- Use **number keys** to select menu options
- Press **Enter** to confirm selections
- Press **Ctrl+C** to exit at any time

### Export Reports

1. Select option **8** from the main menu
2. Choose export format:
   - **JSON** - For automation and scripting
   - **TXT** - For human-readable reports
   - **Both** - Export in both formats

Reports are saved to your home directory with timestamps:
- `~/lxz_report_YYYYMMDD_HHMMSS.json`
- `~/lxz_report_YYYYMMDD_HHMMSS.txt`

---

## 💻 System Requirements

### Minimum Requirements
- **OS**: Linux kernel 4.x or later
- **Python**: Python 3.6 or later
- **Memory**: 50 MB RAM
- **Disk**: 10 MB free space

### Recommended Requirements
- **OS**: Linux kernel 5.x or later
- **Python**: Python 3.8 or later
- **Root Access**: For full feature set
- **Sensors**: lm-sensors configured for temperature monitoring

---

## 🔧 Troubleshooting

### Common Issues

#### 1. "Permission Denied" Errors

**Problem**: Some hardware information is not accessible without root.

**Solution**:
```bash
sudo ./lxz.py
```

#### 2. "rich module not found"

**Problem**: Rich library not installed.

**Solution**:
```bash
pip3 install rich --break-system-packages
```

#### 3. No Temperature Sensors Detected

**Problem**: lm-sensors not configured.

**Solution**:
```bash
sudo sensors-detect  # Answer YES to all prompts
sudo service kmod start  # Or reboot
```

#### 4. Missing GPU Information

**Problem**: GPU drivers not installed or lspci not available.

**Solution**:
```bash
# Install pciutils
sudo apt-get install pciutils  # Debian/Ubuntu
sudo dnf install pciutils      # Fedora/RHEL
sudo pacman -S pciutils        # Arch

# Install appropriate GPU drivers
# NVIDIA: nvidia-driver
# AMD: mesa-vulkan-drivers
```

#### 5. SMART Data Not Available

**Problem**: smartmontools not installed or insufficient permissions.

**Solution**:
```bash
# Install smartmontools
sudo apt-get install smartmontools  # Debian/Ubuntu
sudo dnf install smartmontools      # Fedora/RHEL

# Run with sudo
sudo ./lxz.py
```

### Diagnostic Mode

For debugging, you can check individual components:

```python
# Test CPU detection
python3 -c "from utils.cpu import CPUInfo; print(CPUInfo().get_all_info())"

# Test memory detection
python3 -c "from utils.memory import MemoryInfo; print(MemoryInfo().get_all_info())"
```

---

## 🎨 Features Comparison

| Feature | LX-Z | CPU-Z (Windows) | lscpu | neofetch |
|---------|------|-----------------|-------|----------|
| CPU Details | ✅ Full | ✅ Full | ✅ Basic | ✅ Basic |
| Memory Modules | ✅ DMI | ✅ DMI | ❌ | ❌ |
| Storage Info | ✅ Full | ✅ Full | ❌ | ✅ Basic |
| GPU Details | ✅ Full | ✅ Full | ❌ | ✅ Basic |
| Sensors | ✅ Full | ✅ Full | ❌ | ❌ |
| BIOS Info | ✅ Full | ✅ Full | ❌ | ❌ |
| Export Reports | ✅ JSON/TXT | ✅ TXT/HTML | ❌ | ❌ |
| Interactive UI | ✅ Rich | ✅ GUI | ❌ | ❌ |
| Cross-Platform | 🐧 Linux | 🪟 Windows | 🐧 Linux | 🐧 Multi |

---

## 📚 Project Structure

```
LX-Z/
├── lxz.py                 # Main application entry point
├── install.sh             # Automated installation script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── LICENSE               # MIT License
├── utils/                # Core utility modules
│   ├── __init__.py       # Package initializer
│   ├── cpu.py           # CPU information gathering
│   ├── memory.py        # Memory and motherboard info
│   ├── storage.py       # Storage devices and partitions
│   ├── gpu.py           # GPU and graphics info
│   ├── sensors.py       # Temperature and sensors
│   └── exporter.py      # Report export functionality
└── docs/                # Documentation (if needed)
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add docstrings to all functions and classes
- Test on multiple distributions before submitting
- Update README.md if adding new features

---

## 🐛 Bug Reports

Found a bug? Please open an issue with:

- Your Linux distribution and version
- Python version (`python3 --version`)
- Steps to reproduce
- Expected vs actual behavior
- Any error messages

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by CPU-Z for Windows
- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Thanks to the Linux community for excellent hardware detection tools

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/sarat1kyan/LX-Z/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sarat1kyan/LX-Z/discussions)

---

## 🗺️ Roadmap

- [ ] Real-time CPU frequency monitoring
- [ ] Network adapter information
- [ ] Overclocking detection
- [ ] Benchmark integration
- [ ] Web-based GUI interface
- [ ] Docker container support
- [ ] Raspberry Pi optimization
- [ ] Hardware comparison database

---

<div align="center">

**Made with ❤️ for the Linux community**

**⭐ Star this repo if you found it helpful!**
[![BuyMeACoffee](https://raw.githubusercontent.com/pachadotdev/buymeacoffee-badges/main/bmc-donate-yellow.svg)](https://www.buymeacoffee.com/saratikyan)
[![Report Bug](https://img.shields.io/badge/Report-Bug-red.svg)](https://github.com/sarat1kyan/LX-Z/issues)

</div>
