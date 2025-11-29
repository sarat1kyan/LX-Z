#!/bin/bash

###############################################################################
# LX-Z Installation Script
# Automatically detects Linux distribution and installs required dependencies
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
cat << "EOF"
╦  ═╗ ╦   ╔═╗
║   ╔╝   ╔═╝
╩═╝ ╩    ╚═╝

Linux Hardware Analyzer
Installation Script v1.0
EOF
echo -e "${NC}"

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}Warning: Running as root. This is recommended for full functionality.${NC}"
    SUDO=""
else
    echo -e "${YELLOW}Note: Not running as root. Some features may be limited.${NC}"
    echo -e "${YELLOW}Consider running with sudo for full functionality.${NC}"
    SUDO="sudo"
fi

echo ""

# Function to print status messages
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Detect package manager and distribution
print_status "Detecting Linux distribution..."

if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
    DISTRO_VERSION=$VERSION_ID
    print_success "Detected: $NAME $VERSION"
else
    print_error "Cannot detect distribution. /etc/os-release not found."
    exit 1
fi

# Determine package manager
if command -v apt-get >/dev/null 2>&1; then
    PKG_MANAGER="apt"
    UPDATE_CMD="$SUDO apt-get update"
    INSTALL_CMD="$SUDO apt-get install -y"
    print_success "Package manager: APT (Debian/Ubuntu)"
elif command -v dnf >/dev/null 2>&1; then
    PKG_MANAGER="dnf"
    UPDATE_CMD="$SUDO dnf check-update || true"
    INSTALL_CMD="$SUDO dnf install -y"
    print_success "Package manager: DNF (Fedora/RHEL 8+)"
elif command -v yum >/dev/null 2>&1; then
    PKG_MANAGER="yum"
    UPDATE_CMD="$SUDO yum check-update || true"
    INSTALL_CMD="$SUDO yum install -y"
    print_success "Package manager: YUM (RHEL/CentOS)"
elif command -v pacman >/dev/null 2>&1; then
    PKG_MANAGER="pacman"
    UPDATE_CMD="$SUDO pacman -Sy"
    INSTALL_CMD="$SUDO pacman -S --noconfirm"
    print_success "Package manager: Pacman (Arch Linux)"
else
    print_error "No supported package manager found (apt, dnf, yum, pacman)"
    exit 1
fi

echo ""

# Update package list
print_status "Updating package lists..."
$UPDATE_CMD
print_success "Package lists updated"

echo ""

# Install Python 3 and pip
print_status "Checking Python 3 installation..."

if ! command -v python3 >/dev/null 2>&1; then
    print_warning "Python 3 not found. Installing..."
    
    case $PKG_MANAGER in
        apt)
            $INSTALL_CMD python3 python3-pip
            ;;
        dnf|yum)
            $INSTALL_CMD python3 python3-pip
            ;;
        pacman)
            $INSTALL_CMD python python-pip
            ;;
    esac
    
    print_success "Python 3 installed"
else
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python 3 already installed (version $PYTHON_VERSION)"
fi

# Install pip if not present
if ! command -v pip3 >/dev/null 2>&1; then
    print_warning "pip3 not found. Installing..."
    
    case $PKG_MANAGER in
        apt)
            $INSTALL_CMD python3-pip
            ;;
        dnf|yum)
            $INSTALL_CMD python3-pip
            ;;
        pacman)
            $INSTALL_CMD python-pip
            ;;
    esac
    
    print_success "pip3 installed"
fi

echo ""

# Install system packages
print_status "Installing system dependencies..."

case $PKG_MANAGER in
    apt)
        PACKAGES=(
            "lshw"
            "hwinfo"
            "dmidecode"
            "smartmontools"
            "lm-sensors"
            "pciutils"
            "usbutils"
            "util-linux"
            "mesa-utils"
        )
        ;;
    dnf|yum)
        PACKAGES=(
            "lshw"
            "hwinfo"
            "dmidecode"
            "smartmontools"
            "lm_sensors"
            "pciutils"
            "usbutils"
            "util-linux"
            "mesa-demos"
        )
        ;;
    pacman)
        PACKAGES=(
            "lshw"
            "hwinfo"
            "dmidecode"
            "smartmontools"
            "lm_sensors"
            "pciutils"
            "usbutils"
            "util-linux"
            "mesa-demos"
        )
        ;;
esac

for package in "${PACKAGES[@]}"; do
    print_status "Installing $package..."
    $INSTALL_CMD "$package" 2>/dev/null || print_warning "Could not install $package (may not be critical)"
done

print_success "System dependencies installed"

echo ""

# Install Python dependencies
print_status "Installing Python dependencies..."

# Install rich library
pip3 install rich --break-system-packages 2>/dev/null || \
pip3 install rich --user 2>/dev/null || \
$SUDO pip3 install rich 2>/dev/null || \
print_error "Could not install 'rich' library. Please install manually: pip3 install rich"

print_success "Python dependencies installed"

echo ""

# Initialize sensors (if available)
if command -v sensors-detect >/dev/null 2>&1; then
    print_status "Sensor detection is available. You can run 'sudo sensors-detect' to configure sensors."
fi

echo ""

# Make lxz.py executable
print_status "Making LX-Z executable..."
chmod +x lxz.py 2>/dev/null || print_warning "Could not make lxz.py executable"
print_success "LX-Z is now executable"

echo ""

# Create symlink (optional)
if [ "$EUID" -eq 0 ] || [ -n "$SUDO" ]; then
    read -p "Create system-wide symlink to /usr/local/bin/lxz? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
        $SUDO ln -sf "$SCRIPT_DIR/lxz.py" /usr/local/bin/lxz
        print_success "Symlink created: /usr/local/bin/lxz"
        echo -e "${GREEN}You can now run LX-Z from anywhere using: ${CYAN}lxz${NC}"
    fi
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                     Installation Complete! ✓                           ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}To run LX-Z:${NC}"
echo -e "  ${YELLOW}./lxz.py${NC}               (from this directory)"
echo -e "  ${YELLOW}python3 lxz.py${NC}        (alternative method)"
if [ -L "/usr/local/bin/lxz" ]; then
    echo -e "  ${YELLOW}lxz${NC}                   (from anywhere)"
fi
echo ""
echo -e "${CYAN}For best results:${NC}"
echo -e "  ${YELLOW}sudo ./lxz.py${NC}         (run with root privileges for full information)"
echo ""
echo -e "${CYAN}Tips:${NC}"
echo -e "  • Run with ${YELLOW}sudo${NC} for detailed motherboard, BIOS, and sensor information"
echo -e "  • Some features require specific hardware or drivers to be installed"
echo -e "  • Use option ${YELLOW}8${NC} in the menu to export reports in JSON or TXT format"
echo ""
