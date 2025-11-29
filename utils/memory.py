"""
Memory Information Module
Gathers detailed RAM and memory information
"""

import subprocess
import os
import re
from typing import Dict, List

class MemoryInfo:
    """Handles memory information gathering"""
    
    def __init__(self):
        self.meminfo_path = "/proc/meminfo"
        self.dmidecode_available = self._check_command("dmidecode")
    
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
    
    def _parse_meminfo(self) -> Dict[str, int]:
        """Parse /proc/meminfo"""
        data = {}
        try:
            with open(self.meminfo_path) as f:
                for line in f:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip().split()[0]  # Get numeric value
                        try:
                            data[key] = int(value)
                        except ValueError:
                            data[key] = value
        except Exception:
            pass
        
        return data
    
    def _get_memory_modules(self) -> List[Dict]:
        """Get memory module information from dmidecode"""
        modules = []
        
        if not self.dmidecode_available:
            return modules
        
        try:
            output = self._run_command(['sudo', 'dmidecode', '-t', 'memory'])
            if not output:
                # Try without sudo
                output = self._run_command(['dmidecode', '-t', 'memory'])
            
            if output:
                current_module = {}
                in_memory_device = False
                
                for line in output.split('\n'):
                    line = line.strip()
                    
                    if line.startswith('Memory Device'):
                        if current_module and current_module.get('size') != 'No Module Installed':
                            modules.append(current_module)
                        current_module = {}
                        in_memory_device = True
                    elif in_memory_device and ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if key == 'size':
                            current_module['size'] = value
                        elif key == 'locator':
                            current_module['locator'] = value
                        elif key == 'type':
                            current_module['type'] = value
                        elif key == 'speed':
                            current_module['speed'] = value
                        elif key == 'manufacturer':
                            current_module['manufacturer'] = value
                
                if current_module and current_module.get('size') != 'No Module Installed':
                    modules.append(current_module)
        except Exception:
            pass
        
        return modules
    
    def get_all_info(self) -> Dict:
        """Get all memory information"""
        meminfo = self._parse_meminfo()
        
        # Total memory
        total_kb = meminfo.get('MemTotal', 0)
        total_bytes = total_kb * 1024
        
        # Available memory
        available_kb = meminfo.get('MemAvailable', meminfo.get('MemFree', 0))
        available_bytes = available_kb * 1024
        
        # Free memory
        free_kb = meminfo.get('MemFree', 0)
        free_bytes = free_kb * 1024
        
        # Used memory
        used_bytes = total_bytes - free_bytes
        
        # Usage percentage
        percent = (used_bytes / total_bytes * 100) if total_bytes > 0 else 0
        
        # Swap information
        swap_total_kb = meminfo.get('SwapTotal', 0)
        swap_free_kb = meminfo.get('SwapFree', 0)
        swap_total_bytes = swap_total_kb * 1024
        swap_free_bytes = swap_free_kb * 1024
        swap_used_bytes = swap_total_bytes - swap_free_bytes
        swap_percent = (swap_used_bytes / swap_total_bytes * 100) if swap_total_bytes > 0 else 0
        
        data = {
            'total': self._format_bytes(total_bytes),
            'available': self._format_bytes(available_bytes),
            'used': self._format_bytes(used_bytes),
            'free': self._format_bytes(free_bytes),
            'percent': f"{percent:.1f}%",
            'swap_total': self._format_bytes(swap_total_bytes),
            'swap_used': self._format_bytes(swap_used_bytes),
            'swap_free': self._format_bytes(swap_free_bytes),
            'swap_percent': f"{swap_percent:.1f}%",
            'modules': self._get_memory_modules()
        }
        
        return data
    
    def get_motherboard_info(self) -> Dict:
        """Get motherboard and BIOS information"""
        data = {
            'manufacturer': 'Unknown',
            'product': 'Unknown',
            'version': 'Unknown',
            'serial': 'Unknown',
            'bios_vendor': 'Unknown',
            'bios_version': 'Unknown',
            'bios_date': 'Unknown'
        }
        
        if not self.dmidecode_available:
            return data
        
        try:
            # Motherboard info
            output = self._run_command(['sudo', 'dmidecode', '-t', 'baseboard'])
            if not output:
                output = self._run_command(['dmidecode', '-t', 'baseboard'])
            
            if output:
                for line in output.split('\n'):
                    line = line.strip()
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if key == 'manufacturer':
                            data['manufacturer'] = value
                        elif key == 'product name':
                            data['product'] = value
                        elif key == 'version':
                            data['version'] = value
                        elif key == 'serial number':
                            data['serial'] = value if value else 'Unknown'
            
            # BIOS info
            output = self._run_command(['sudo', 'dmidecode', '-t', 'bios'])
            if not output:
                output = self._run_command(['dmidecode', '-t', 'bios'])
            
            if output:
                for line in output.split('\n'):
                    line = line.strip()
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if key == 'vendor':
                            data['bios_vendor'] = value
                        elif key == 'version':
                            data['bios_version'] = value
                        elif key == 'release date':
                            data['bios_date'] = value
        except Exception:
            pass
        
        return data
    
    def get_summary(self) -> Dict:
        """Get summary memory information"""
        info = self.get_all_info()
        return {
            'Total RAM': info.get('total', 'Unknown'),
            'Available': info.get('available', 'Unknown'),
            'Usage': info.get('percent', 'Unknown')
        }
