# LX-Z Developer Documentation

## 🏗️ Architecture Overview

LX-Z follows a modular architecture with clear separation of concerns. Each hardware component has its own dedicated module with fallback mechanisms for reliability.

### Design Principles

1. **Modularity** - Each hardware type in separate module
2. **Fallback Mechanisms** - Multiple detection methods
3. **Graceful Degradation** - Works without root access
4. **Cross-Platform** - Support multiple distributions
5. **Clean Code** - PEP 8 compliant, well-documented

---

## 📦 Module Structure

### Main Application (`lxz.py`)

**Purpose**: Main entry point and UI controller

**Key Components**:
- `LXZ` class - Main application controller
- Menu system and user interaction
- Display formatting and rendering
- Module coordination

**Lines of Code**: 658 lines

**Key Methods**:
```python
class LXZ:
    def __init__(self)              # Initialize all modules
    def show_banner(self)           # Display ASCII banner
    def show_menu(self)             # Render main menu
    def show_cpu_info(self)         # Display CPU details
    def show_memory_info(self)      # Display memory details
    def show_storage_info(self)     # Display storage details
    def show_gpu_info(self)         # Display GPU details
    def show_motherboard_info(self) # Display motherboard details
    def show_sensor_info(self)      # Display sensor data
    def show_complete_overview(self)# Display all info
    def export_report(self)         # Export to file
    def run(self)                   # Main loop
```

---

### CPU Module (`utils/cpu.py`)

**Purpose**: Detect and report CPU information

**Lines of Code**: 246 lines

**Data Sources**:
1. Primary: `lscpu` command
2. Fallback: `/proc/cpuinfo`
3. Cache: `/sys/devices/system/cpu/cpu0/cache`
4. Frequency: `/sys/devices/system/cpu/cpu0/cpufreq`

**Key Methods**:
```python
class CPUInfo:
    def _parse_cpuinfo(self)      # Parse /proc/cpuinfo
    def _get_lscpu_info(self)     # Get lscpu output
    def _get_cache_info(self)     # Get cache sizes
    def _get_frequency_info(self) # Get freq data
    def _get_cpu_flags(self)      # Get CPU features
    def _count_cores_threads(self)# Count cores/threads
    def get_all_info(self)        # Return complete data
    def get_summary(self)         # Return brief summary
```

**Detection Logic**:
```python
# Priority order for CPU model:
1. lscpu output (most reliable)
2. /proc/cpuinfo "model name" field
3. Unknown (fallback)

# Cache detection:
1. lscpu cache fields
2. /sys/devices/system/cpu/cpu0/cache/*
3. Unknown (fallback)
```

---

### Memory Module (`utils/memory.py`)

**Purpose**: Detect RAM, motherboard, and BIOS information

**Lines of Code**: 223 lines

**Data Sources**:
1. `/proc/meminfo` - Memory statistics
2. `dmidecode -t memory` - Memory modules (requires root)
3. `dmidecode -t baseboard` - Motherboard info
4. `dmidecode -t bios` - BIOS information

**Key Methods**:
```python
class MemoryInfo:
    def _parse_meminfo(self)       # Parse /proc/meminfo
    def _get_memory_modules(self)  # Get DMI module info
    def get_all_info(self)         # Return complete data
    def get_motherboard_info(self) # Get MB/BIOS data
    def get_summary(self)          # Return brief summary
```

**Root Requirements**:
- `dmidecode` requires root for DMI/SMBIOS access
- Without root: basic memory stats available
- With root: detailed module information

---

### Storage Module (`utils/storage.py`)

**Purpose**: Detect storage devices and partitions

**Lines of Code**: 214 lines

**Data Sources**:
1. Primary: `lsblk` command
2. Fallback: `/sys/block/*`
3. Mounts: `/proc/mounts`
4. SMART: `smartctl` (optional)

**Key Methods**:
```python
class StorageInfo:
    def _get_block_devices(self)   # Get all block devices
    def _get_devices_fallback(self)# Fallback method
    def _get_partitions(self)      # Get partition info
    def _get_smart_info(self)      # Get SMART data
    def get_all_info(self)         # Return complete data
    def get_summary(self)          # Return brief summary
```

**Device Type Detection**:
```python
# SSD vs HDD detection:
1. Check /sys/block/<device>/queue/rotational
2. 0 = SSD (non-rotational)
3. 1 = HDD (rotational)
```

---

### GPU Module (`utils/gpu.py`)

**Purpose**: Detect graphics cards and display information

**Lines of Code**: 242 lines

**Data Sources**:
1. `lspci` - PCI device enumeration
2. `nvidia-smi` - NVIDIA GPU details
3. `glxinfo` - OpenGL support
4. `vulkaninfo` - Vulkan support
5. `modinfo` - Driver version info

**Key Methods**:
```python
class GPUInfo:
    def _get_pci_gpus(self)        # Get GPUs via lspci
    def _get_driver_info(self)     # Get driver details
    def _get_nvidia_version(self)  # NVIDIA driver ver
    def _get_amd_version(self)     # AMD driver version
    def _get_intel_version(self)   # Intel driver ver
    def _get_nvidia_info(self)     # Detailed NVIDIA info
    def _get_opengl_info(self)     # OpenGL support
    def _get_vulkan_info(self)     # Vulkan support
    def get_all_info(self)         # Return complete data
    def get_summary(self)          # Return brief summary
```

**Vendor Detection**:
```python
# GPU vendor identification:
if 'NVIDIA' in description:
    vendor = 'NVIDIA'
elif 'AMD' in description or 'ATI' in description:
    vendor = 'AMD'
elif 'Intel' in description:
    vendor = 'Intel'
```

---

### Sensors Module (`utils/sensors.py`)

**Purpose**: Monitor temperatures, fans, and battery

**Lines of Code**: 249 lines

**Data Sources**:
1. Primary: `sensors` command (lm-sensors)
2. `/sys/class/thermal/thermal_zone*/temp`
3. `/sys/class/hwmon/hwmon*/temp*_input`
4. `/sys/class/power_supply/BAT*` - Battery

**Key Methods**:
```python
class SensorInfo:
    def _get_thermal_zones(self)   # Get thermal zone temps
    def _get_hwmon_temps(self)     # Get hwmon temps
    def _get_lm_sensors_info(self) # Get lm-sensors data
    def _get_battery_info(self)    # Get battery status
    def get_all_info(self)         # Return complete data
    def get_summary(self)          # Return brief summary
```

**Temperature Sources Priority**:
```python
1. lm-sensors output (most detailed)
2. /sys/class/hwmon (direct hardware monitoring)
3. /sys/class/thermal (kernel thermal zones)
```

---

### Export Module (`utils/exporter.py`)

**Purpose**: Export system information to files

**Lines of Code**: 199 lines

**Supported Formats**:
- JSON - Machine-readable, structured data
- TXT - Human-readable, formatted report

**Key Methods**:
```python
class ExportReport:
    def export_json(self, data, filename) # Export as JSON
    def export_txt(self, data, filename)  # Export as TXT
```

**File Naming**:
```python
# Default naming scheme:
lxz_report_YYYYMMDD_HHMMSS.json
lxz_report_YYYYMMDD_HHMMSS.txt

# Saved to: ~/lxz_report_*
```

---

## 🔧 Adding New Features

### Adding a New Hardware Module

1. **Create module file** in `utils/`:
```python
# utils/network.py
class NetworkInfo:
    def __init__(self):
        self.tool_available = self._check_command("ip")
    
    def _check_command(self, command: str) -> bool:
        """Check if command exists"""
        # Implementation
    
    def get_all_info(self) -> Dict:
        """Get all network information"""
        # Implementation
    
    def get_summary(self) -> Dict:
        """Get summary information"""
        # Implementation
```

2. **Update `utils/__init__.py`**:
```python
from .network import NetworkInfo

__all__ = [
    'CPUInfo',
    'MemoryInfo',
    'StorageInfo',
    'GPUInfo',
    'SensorInfo',
    'ExportReport',
    'NetworkInfo'  # Add new module
]
```

3. **Add to main application** in `lxz.py`:
```python
from utils.network import NetworkInfo

class LXZ:
    def __init__(self):
        # ... existing modules ...
        self.network_info = NetworkInfo()
    
    def show_network_info(self):
        """Display network information"""
        # Implementation
```

4. **Add menu option** in `show_menu()`:
```python
menu_items = [
    # ... existing items ...
    ("9", "🔹 Network Information"),
]
```

5. **Add handler** in `run()`:
```python
elif choice == "9":
    self.show_network_info()
```

---

## 🧪 Testing Guidelines

### Unit Testing Example

```python
# tests/test_cpu.py
import unittest
from utils.cpu import CPUInfo

class TestCPUInfo(unittest.TestCase):
    def setUp(self):
        self.cpu = CPUInfo()
    
    def test_get_all_info(self):
        info = self.cpu.get_all_info()
        self.assertIsInstance(info, dict)
        self.assertIn('model', info)
        self.assertIn('cores', info)
    
    def test_get_summary(self):
        summary = self.cpu.get_summary()
        self.assertIsInstance(summary, dict)
        self.assertTrue(len(summary) > 0)

if __name__ == '__main__':
    unittest.main()
```

### Integration Testing

```bash
# Test on different distributions
for distro in ubuntu debian fedora arch; do
    docker run -it $distro:latest bash -c "
        cd /app &&
        ./install.sh &&
        ./lxz.py --test
    "
done
```

---

## 🎨 UI Guidelines

### Using Rich for Display

```python
from rich.console import Console
from rich.table import Table

console = Console()

# Create a table
table = Table(title="Hardware Info", box=box.ROUNDED)
table.add_column("Property", style="yellow")
table.add_column("Value", style="bright_white")
table.add_row("CPU", "Intel Core i7")

console.print(table)
```

### Color Scheme

- **Cyan** - Headers and titles
- **Yellow** - Labels and property names
- **Bright White** - Values and data
- **Green** - Success messages
- **Red** - Errors
- **Blue** - Info messages

---

## 🔍 Debugging

### Enable Debug Output

```python
# Add at top of lxz.py
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s'
)
```

### Test Individual Modules

```bash
# Test CPU module
python3 -c "from utils.cpu import CPUInfo; import json; print(json.dumps(CPUInfo().get_all_info(), indent=2))"

# Test with error handling
python3 -c "
from utils.cpu import CPUInfo
try:
    cpu = CPUInfo()
    print(cpu.get_all_info())
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
"
```

---

## 📚 Code Style Guidelines

### Follow PEP 8

```python
# Good
def get_cpu_info(self) -> Dict[str, Any]:
    """Get CPU information."""
    return {}

# Bad
def GetCPUInfo(self):
    return {}
```

### Documentation

```python
def method_name(self, param: str) -> Dict:
    """
    Brief description.
    
    Args:
        param: Description of parameter
    
    Returns:
        Dict containing the results
    
    Raises:
        ValueError: When something goes wrong
    """
    pass
```

### Error Handling

```python
# Always use try-except for external commands
try:
    output = subprocess.run(['command'], capture_output=True)
except FileNotFoundError:
    # Handle missing command
    pass
except Exception as e:
    # Handle other errors
    logging.error(f"Error: {e}")
```

---

## 🚀 Performance Optimization

### Caching

```python
class HardwareInfo:
    def __init__(self):
        self._cache = {}
    
    def get_info(self):
        if 'data' not in self._cache:
            self._cache['data'] = self._expensive_operation()
        return self._cache['data']
```

### Lazy Loading

```python
class LXZ:
    def __init__(self):
        self._cpu_info = None
    
    @property
    def cpu_info(self):
        if self._cpu_info is None:
            self._cpu_info = CPUInfo()
        return self._cpu_info
```

---

## 📦 Building & Distribution

### Creating a Release

```bash
# 1. Update version in CHANGELOG.md
# 2. Tag the release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 3. Create tarball
tar -czf lxz-v1.0.0.tar.gz LX-Z/

# 4. Create checksum
sha256sum lxz-v1.0.0.tar.gz > lxz-v1.0.0.tar.gz.sha256
```

### Package for Distributions

```bash
# Debian package structure
lxz_1.0.0/
├── DEBIAN/
│   └── control
├── usr/
│   ├── bin/
│   │   └── lxz
│   └── share/
│       └── lxz/
│           ├── lxz.py
│           └── utils/

# Build .deb
dpkg-deb --build lxz_1.0.0
```

---

## 🤝 Contributing Guidelines

### Pull Request Process

1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Make changes and test thoroughly
4. Update documentation
5. Commit with clear messages
6. Push to branch
7. Open pull request

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

Example:
```
feat: Add network adapter information module

- Implement network interface detection
- Add IP address and MAC address display
- Support for multiple interfaces
- Add to main menu

Closes #123
```

---

## 📊 Code Statistics

**Total Project Stats**:
- **Lines of Code**: 2,050 lines
- **Modules**: 7 (6 utilities + main)
- **Functions**: ~60+
- **Classes**: 7
- **Documentation**: ~30KB markdown

**Module Breakdown**:
- lxz.py: 658 lines (32%)
- sensors.py: 249 lines (12%)
- cpu.py: 246 lines (12%)
- gpu.py: 242 lines (12%)
- storage.py: 214 lines (10%)
- memory.py: 223 lines (11%)
- exporter.py: 199 lines (10%)
- __init__.py: 19 lines (1%)

---

## 🔗 Useful Resources

- **Rich Documentation**: https://rich.readthedocs.io/
- **Python lscpu**: https://docs.python.org/3/library/subprocess.html
- **Linux /proc**: https://www.kernel.org/doc/html/latest/filesystems/proc.html
- **DMI/SMBIOS**: https://www.dmtf.org/standards/smbios
- **lm-sensors**: https://github.com/lm-sensors/lm-sensors

---

**For more information, see the main [README.md](README.md)**
