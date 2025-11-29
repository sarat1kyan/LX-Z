# LX-Z Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2024-11-29

### 🎉 Initial Release

This is the first complete release of LX-Z - Linux Hardware Analyzer, a professional CPU-Z alternative for Linux systems.

### ✨ Added

#### Core Features
- Interactive command-line interface with beautiful Rich-based UI
- Multi-distribution support (Ubuntu, Debian, RHEL, CentOS, Fedora, Arch)
- Automated installation script with dependency management
- Modular architecture for easy maintenance and extension

#### Hardware Detection
- **CPU Module** (`utils/cpu.py`)
  - Full CPU information (model, architecture, vendor)
  - Core and thread count detection
  - CPU frequency monitoring (current, min, max)
  - Cache information (L1d, L1i, L2, L3)
  - Complete CPU flags and features
  - Support for multiple detection methods (lscpu, /proc/cpuinfo)

- **Memory Module** (`utils/memory.py`)
  - Total, available, used, free RAM statistics
  - Swap space information
  - DMI memory module detection (with sudo)
  - Module size, type, speed, manufacturer
  - Motherboard information
  - BIOS/UEFI details

- **Storage Module** (`utils/storage.py`)
  - Block device detection (HDD/SSD identification)
  - Device model, size, type information
  - Partition and filesystem details
  - Mount point and usage statistics
  - Support for multiple detection methods (lsblk, /sys/block)

- **GPU Module** (`utils/gpu.py`)
  - Graphics card detection via lspci
  - NVIDIA GPU support with nvidia-smi integration
  - Driver information and version
  - VRAM detection (NVIDIA)
  - OpenGL and Vulkan support detection
  - AMD and Intel GPU support

- **Sensors Module** (`utils/sensors.py`)
  - Temperature monitoring (CPU, GPU, motherboard)
  - Fan speed detection (RPM)
  - Battery information for laptops
  - Support for lm-sensors, /sys/class/thermal, hwmon
  - Multiple fallback mechanisms

- **Export Module** (`utils/exporter.py`)
  - JSON export for machine-readable reports
  - TXT export for human-readable documentation
  - Timestamped filename generation
  - Complete system information export

#### User Interface
- ASCII art banner
- Color-coded information tables
- Progress indicators during data collection
- Interactive menu with 9 options
- Graceful error handling
- Help text and tooltips

#### Documentation
- Comprehensive README.md with installation and usage guide
- Quick start guide (QUICKSTART.md)
- Detailed usage examples (EXAMPLES.md)
- Project summary document
- MIT License
- Complete API documentation in docstrings

#### Installation & Distribution
- Automated installation script (`install.sh`)
  - Automatic distribution detection
  - Package manager identification
  - Dependency installation
  - Python package management
  - Optional system-wide symlink creation
- Requirements.txt for Python dependencies
- Executable permissions setup
- Multi-distro compatibility testing

### 🔧 Technical Details

#### Architecture
- **Language**: Python 3.6+
- **Dependencies**: Rich library for terminal UI
- **System Tools**: lscpu, lspci, dmidecode, sensors, lsblk
- **Detection Methods**: Multiple fallback mechanisms for reliability
- **Code Structure**: Modular design with separated concerns

#### Supported Systems
- **Distributions**: Ubuntu 18.04+, Debian 9+, RHEL 7+, CentOS 7+, Fedora 30+, Arch Linux
- **Kernels**: Linux 4.x, 5.x, 6.x
- **Architectures**: x86_64, ARM (basic support)
- **Environments**: Bare-metal and virtual machines

### 📊 Statistics

- **Total Lines of Code**: ~2,500+
- **Number of Modules**: 6 utility modules + main application
- **Documentation**: ~30KB of markdown documentation
- **Code Size**: ~55KB of Python code
- **Total Project Size**: ~130KB

### 🎯 Features Comparison

Complete feature parity with CPU-Z for Windows:
- ✅ CPU information and specifications
- ✅ Memory module detection (DMI)
- ✅ Storage device information
- ✅ GPU and graphics card details
- ✅ Motherboard and BIOS information
- ✅ Sensor monitoring (temperatures, fans)
- ✅ Export functionality (JSON/TXT)
- ✅ Professional user interface

### 📝 Known Issues

See TROUBLESHOOTING section in README.md for:
- Root access requirements for certain features
- Sensor detection configuration needs
- GPU driver requirements
- Virtual machine limitations

### 🔒 Security

- No hardcoded credentials or sensitive data
- Safe handling of system information
- No remote connections or telemetry
- MIT License - fully open source

### 👥 Contributors

- Initial development and release

### 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## [Unreleased]

### 🔮 Planned Features

Future enhancements being considered:

#### High Priority
- Real-time monitoring mode with auto-refresh
- Non-interactive CLI mode for scripting
- Network adapter information
- PCIe slot detection and mapping

#### Medium Priority
- Benchmark integration
- Web-based GUI interface
- REST API server mode
- Hardware comparison database
- Overclocking detection

#### Low Priority
- Docker container packaging
- Raspberry Pi specific optimizations
- Hardware stress testing integration
- Historical data tracking
- Multi-language support

---

## Version History

- **v1.0.0** (2024-11-29) - Initial release

---

## Contributing

See CONTRIBUTING.md for guidelines on how to contribute to this project.

### Reporting Issues

When reporting issues, please include:
- LX-Z version (`./lxz.py --version` or check this file)
- Linux distribution and version
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Relevant error messages or screenshots

### Suggesting Features

Feature requests are welcome! Please:
- Check if the feature is already planned (see Unreleased section)
- Describe the use case clearly
- Explain the expected behavior
- Consider contributing a pull request

---

## Acknowledgments

- Inspired by CPU-Z for Windows
- Built with Rich library for terminal UI
- Thanks to the Linux community for hardware detection tools
- Special thanks to all contributors and testers

---

**For more information, see README.md or visit the project repository.**
