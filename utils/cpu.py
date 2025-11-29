"""
CPU Information Module
Gathers detailed CPU information from the system
"""

import subprocess
import re
import os
from typing import Dict, List, Optional

class CPUInfo:
    """Handles CPU information gathering"""
    
    def __init__(self):
        self.cpuinfo_path = "/proc/cpuinfo"
        self.lscpu_available = self._check_command("lscpu")
    
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
    
    def _parse_cpuinfo(self) -> Dict[str, str]:
        """Parse /proc/cpuinfo"""
        data = {}
        try:
            with open(self.cpuinfo_path, 'r') as f:
                content = f.read()
                
                # Get first processor block
                first_proc = content.split('\n\n')[0]
                
                for line in first_proc.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().replace(' ', '_')
                        value = value.strip()
                        data[key] = value
        except Exception:
            pass
        
        return data
    
    def _get_lscpu_info(self) -> Dict[str, str]:
        """Get information from lscpu"""
        data = {}
        if not self.lscpu_available:
            return data
        
        output = self._run_command(['lscpu'])
        for line in output.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().replace(' ', '_').replace('(s)', '').lower()
                value = value.strip()
                data[key] = value
        
        return data
    
    def _get_cache_info(self) -> Dict[str, str]:
        """Get CPU cache information"""
        cache = {}
        
        if self.lscpu_available:
            lscpu = self._get_lscpu_info()
            cache['l1d_cache'] = lscpu.get('l1d_cache', 'Unknown')
            cache['l1i_cache'] = lscpu.get('l1i_cache', 'Unknown')
            cache['l2_cache'] = lscpu.get('l2_cache', 'Unknown')
            cache['l3_cache'] = lscpu.get('l3_cache', 'Unknown')
        else:
            # Fallback to /sys/devices/system/cpu
            try:
                cpu0_path = "/sys/devices/system/cpu/cpu0/cache"
                if os.path.exists(cpu0_path):
                    for idx in os.listdir(cpu0_path):
                        index_path = os.path.join(cpu0_path, idx)
                        if os.path.isdir(index_path):
                            level_file = os.path.join(index_path, "level")
                            size_file = os.path.join(index_path, "size")
                            type_file = os.path.join(index_path, "type")
                            
                            if os.path.exists(level_file) and os.path.exists(size_file):
                                with open(level_file) as f:
                                    level = f.read().strip()
                                with open(size_file) as f:
                                    size = f.read().strip()
                                
                                cache_type = "Cache"
                                if os.path.exists(type_file):
                                    with open(type_file) as f:
                                        cache_type = f.read().strip()
                                
                                key = f"l{level}"
                                if cache_type == "Data":
                                    key += "d"
                                elif cache_type == "Instruction":
                                    key += "i"
                                
                                cache[f"{key}_cache"] = size
            except Exception:
                pass
        
        # Set defaults for missing values
        for key in ['l1d_cache', 'l1i_cache', 'l2_cache', 'l3_cache']:
            if key not in cache:
                cache[key] = 'Unknown'
        
        return cache
    
    def _get_frequency_info(self) -> Dict[str, str]:
        """Get CPU frequency information"""
        freq = {}
        
        try:
            # Current frequency
            current_freq = 0
            freq_path = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"
            if os.path.exists(freq_path):
                with open(freq_path) as f:
                    current_freq = int(f.read().strip()) / 1000  # Convert to MHz
                freq['current_freq'] = f"{current_freq:.2f} MHz"
            
            # Max frequency
            max_freq_path = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq"
            if os.path.exists(max_freq_path):
                with open(max_freq_path) as f:
                    max_freq = int(f.read().strip()) / 1000
                freq['max_freq'] = f"{max_freq:.2f} MHz"
            
            # Min frequency
            min_freq_path = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq"
            if os.path.exists(min_freq_path):
                with open(min_freq_path) as f:
                    min_freq = int(f.read().strip()) / 1000
                freq['min_freq'] = f"{min_freq:.2f} MHz"
        except Exception:
            pass
        
        # Fallback to cpuinfo
        if not freq.get('current_freq'):
            cpuinfo = self._parse_cpuinfo()
            if 'cpu_mhz' in cpuinfo:
                freq['current_freq'] = f"{cpuinfo['cpu_mhz']} MHz"
        
        # Set defaults
        for key in ['current_freq', 'max_freq', 'min_freq']:
            if key not in freq:
                freq[key] = 'Unknown'
        
        return freq
    
    def _get_cpu_flags(self) -> List[str]:
        """Get CPU flags/features"""
        try:
            cpuinfo = self._parse_cpuinfo()
            if 'flags' in cpuinfo:
                return cpuinfo['flags'].split()
        except Exception:
            pass
        return []
    
    def _count_cores_threads(self) -> Dict[str, int]:
        """Count physical cores and logical processors"""
        cores = 0
        threads = 0
        sockets = 1
        
        if self.lscpu_available:
            lscpu = self._get_lscpu_info()
            cores = int(lscpu.get('core_per_socket', 0))
            sockets = int(lscpu.get('socket', 1))
            threads = int(lscpu.get('cpu', 0))
        else:
            # Fallback to /proc/cpuinfo
            try:
                with open(self.cpuinfo_path) as f:
                    content = f.read()
                    
                    # Count processors
                    threads = content.count('processor\t:')
                    
                    # Get core count from first processor
                    match = re.search(r'cpu cores\s*:\s*(\d+)', content)
                    if match:
                        cores = int(match.group(1))
                    else:
                        cores = threads
            except Exception:
                pass
        
        return {
            'cores': cores if cores > 0 else threads,
            'threads': threads if threads > 0 else 1,
            'sockets': sockets
        }
    
    def get_all_info(self) -> Dict:
        """Get all CPU information"""
        cpuinfo = self._parse_cpuinfo()
        lscpu = self._get_lscpu_info()
        cache = self._get_cache_info()
        freq = self._get_frequency_info()
        flags = self._get_cpu_flags()
        core_thread = self._count_cores_threads()
        
        data = {
            'model': cpuinfo.get('model_name', lscpu.get('model_name', 'Unknown')),
            'architecture': lscpu.get('architecture', cpuinfo.get('architecture', 'Unknown')),
            'vendor_id': cpuinfo.get('vendor_id', 'Unknown'),
            'cpu_family': cpuinfo.get('cpu_family', 'Unknown'),
            'model_number': cpuinfo.get('model', 'Unknown'),
            'stepping': cpuinfo.get('stepping', 'Unknown'),
            'cores': core_thread['cores'],
            'threads': core_thread['threads'],
            'sockets': core_thread['sockets'],
            'flags': flags
        }
        
        # Add cache info
        data.update(cache)
        
        # Add frequency info
        data.update(freq)
        
        return data
    
    def get_summary(self) -> Dict:
        """Get summary CPU information"""
        info = self.get_all_info()
        return {
            'Processor': info.get('model', 'Unknown'),
            'Cores': f"{info.get('cores', 'Unknown')} cores, {info.get('threads', 'Unknown')} threads",
            'Frequency': info.get('current_freq', 'Unknown'),
            'Cache L3': info.get('l3_cache', 'Unknown')
        }
