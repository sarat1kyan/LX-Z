"""
Storage Information Module
Gathers detailed storage device and partition information
"""

import subprocess
import os
import re
from typing import Dict, List

class StorageInfo:
    """Handles storage information gathering"""
    
    def __init__(self):
        self.lsblk_available = self._check_command("lsblk")
    
    def _check_command(self, command: str) -> bool:
        """Check if a command is available"""
        try:
            subprocess.run([command, "--version"], capture_output=True, check=False)
            return True
        except FileNotFoundError:
            return False
    
    def _run_command(self, command: List[str]) -> str:
        """Run a shell command and return output"""
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            return result.stdout.strip()
        except Exception:
            return ""
    
    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes to human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"
    
    def _get_block_devices(self) -> List[Dict]:
        """Get block device information"""
        devices = []
        
        if not self.lsblk_available:
            return self._get_devices_fallback()
        
        try:
            output = self._run_command(['lsblk', '-b', '-d', '-o', 'NAME,SIZE,TYPE,MODEL,ROTA,RO'])
            
            for line in output.split('\n')[1:]:  # Skip header
                parts = line.split()
                if len(parts) >= 4:
                    name = parts[0]
                    size = int(parts[1]) if parts[1].isdigit() else 0
                    dev_type = parts[2]
                    model = ' '.join(parts[3:-2]) if len(parts) > 5 else 'Unknown'
                    rotational = parts[-2] if len(parts) >= 5 else '0'
                    readonly = parts[-1] if len(parts) >= 6 else '0'
                    
                    # Determine if SSD or HDD
                    is_ssd = rotational == '0'
                    device_type = 'SSD' if is_ssd else 'HDD'
                    
                    if dev_type == 'disk':
                        devices.append({
                            'name': name,
                            'path': f'/dev/{name}',
                            'size': self._format_bytes(size),
                            'type': device_type,
                            'model': model,
                            'removable': 'No',
                            'readonly': 'Yes' if readonly == '1' else 'No'
                        })
        except Exception:
            pass
        
        return devices
    
    def _get_devices_fallback(self) -> List[Dict]:
        """Fallback method to get devices from /sys"""
        devices = []
        
        try:
            for device in os.listdir('/sys/block'):
                if device.startswith('sd') or device.startswith('nvme') or device.startswith('vd'):
                    device_path = f'/sys/block/{device}'
                    
                    # Get size
                    size = 0
                    size_file = os.path.join(device_path, 'size')
                    if os.path.exists(size_file):
                        with open(size_file) as f:
                            size = int(f.read().strip()) * 512  # Sectors to bytes
                    
                    # Check if removable
                    removable = 'No'
                    removable_file = os.path.join(device_path, 'removable')
                    if os.path.exists(removable_file):
                        with open(removable_file) as f:
                            removable = 'Yes' if f.read().strip() == '1' else 'No'
                    
                    # Check if rotational (SSD vs HDD)
                    is_ssd = True
                    rotational_file = os.path.join(device_path, 'queue/rotational')
                    if os.path.exists(rotational_file):
                        with open(rotational_file) as f:
                            is_ssd = f.read().strip() == '0'
                    
                    devices.append({
                        'name': device,
                        'path': f'/dev/{device}',
                        'size': self._format_bytes(size),
                        'type': 'SSD' if is_ssd else 'HDD',
                        'model': 'Unknown',
                        'removable': removable,
                        'readonly': 'No'
                    })
        except Exception:
            pass
        
        return devices
    
    def _get_partitions(self) -> List[Dict]:
        """Get partition and filesystem information"""
        partitions = []
        
        try:
            # Read /proc/mounts for mounted filesystems
            with open('/proc/mounts') as f:
                for line in f:
                    parts = line.split()
                    if len(parts) >= 4:
                        device = parts[0]
                        mountpoint = parts[1]
                        fstype = parts[2]
                        
                        # Skip non-disk filesystems
                        if not device.startswith('/dev/'):
                            continue
                        if fstype in ['tmpfs', 'devtmpfs', 'proc', 'sysfs', 'cgroup', 'cgroup2']:
                            continue
                        
                        # Get partition size and usage
                        try:
                            stat = os.statvfs(mountpoint)
                            size = stat.f_blocks * stat.f_frsize
                            free = stat.f_bfree * stat.f_frsize
                            used = size - free
                            percent = (used / size * 100) if size > 0 else 0
                            
                            partitions.append({
                                'device': device,
                                'mountpoint': mountpoint,
                                'fstype': fstype,
                                'size': self._format_bytes(size),
                                'used': self._format_bytes(used),
                                'free': self._format_bytes(free),
                                'percent': f"{percent:.1f}%"
                            })
                        except Exception:
                            continue
        except Exception:
            pass
        
        return partitions
    
    def _get_smart_info(self, device: str) -> Dict:
        """Get SMART information for a device"""
        smart_info = {}
        
        try:
            output = self._run_command(['sudo', 'smartctl', '-H', device])
            if not output:
                output = self._run_command(['smartctl', '-H', device])
            
            if output:
                if 'PASSED' in output:
                    smart_info['health'] = 'PASSED'
                elif 'FAILED' in output:
                    smart_info['health'] = 'FAILED'
                else:
                    smart_info['health'] = 'Unknown'
        except Exception:
            smart_info['health'] = 'Not available'
        
        return smart_info
    
    def get_all_info(self) -> Dict:
        """Get all storage information"""
        data = {
            'devices': self._get_block_devices(),
            'partitions': self._get_partitions()
        }
        
        return data
    
    def get_summary(self) -> Dict:
        """Get summary storage information"""
        info = self.get_all_info()
        
        total_devices = len(info.get('devices', []))
        device_types = {}
        
        for device in info.get('devices', []):
            dev_type = device.get('type', 'Unknown')
            device_types[dev_type] = device_types.get(dev_type, 0) + 1
        
        type_str = ', '.join([f"{count} {dtype}" for dtype, count in device_types.items()])
        
        return {
            'Devices': f"{total_devices} ({type_str})" if type_str else str(total_devices),
            'Partitions': str(len(info.get('partitions', [])))
        }
