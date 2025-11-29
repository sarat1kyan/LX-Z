"""
GPU Information Module
Gathers detailed GPU and graphics information
"""

import subprocess
import re
from typing import Dict, List

class GPUInfo:
    """Handles GPU information gathering"""
    
    def __init__(self):
        self.lspci_available = self._check_command("lspci")
        self.nvidia_smi_available = self._check_command("nvidia-smi")
        self.glxinfo_available = self._check_command("glxinfo")
        self.vulkaninfo_available = self._check_command("vulkaninfo")
    
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
            result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=5)
            return result.stdout.strip()
        except Exception:
            return ""
    
    def _get_pci_gpus(self) -> List[Dict]:
        """Get GPU information from lspci"""
        gpus = []
        
        if not self.lspci_available:
            return gpus
        
        try:
            output = self._run_command(['lspci'])
            
            for line in output.split('\n'):
                if 'VGA compatible controller' in line or '3D controller' in line:
                    parts = line.split(':', 2)
                    if len(parts) >= 3:
                        device_id = parts[0].strip()
                        description = parts[2].strip()
                        
                        # Parse vendor and model
                        vendor = 'Unknown'
                        model = description
                        
                        if 'NVIDIA' in description:
                            vendor = 'NVIDIA'
                            model = description.replace('NVIDIA Corporation', '').strip()
                        elif 'AMD' in description or 'ATI' in description:
                            vendor = 'AMD'
                            model = description.replace('Advanced Micro Devices, Inc.', '').strip()
                            model = model.replace('[AMD/ATI]', '').strip()
                        elif 'Intel' in description:
                            vendor = 'Intel'
                            model = description.replace('Intel Corporation', '').strip()
                        
                        # Get driver info
                        driver_info = self._get_driver_info(device_id)
                        
                        gpus.append({
                            'device': device_id,
                            'vendor': vendor,
                            'model': model,
                            'driver': driver_info.get('driver', 'Unknown'),
                            'driver_version': driver_info.get('version', 'Unknown')
                        })
        except Exception:
            pass
        
        return gpus
    
    def _get_driver_info(self, device_id: str) -> Dict:
        """Get driver information for a device"""
        info = {'driver': 'Unknown', 'version': 'Unknown'}
        
        try:
            output = self._run_command(['lspci', '-v', '-s', device_id])
            
            for line in output.split('\n'):
                if 'Kernel driver in use:' in line:
                    driver = line.split(':')[-1].strip()
                    info['driver'] = driver
                    
                    # Try to get driver version
                    if driver == 'nvidia':
                        version = self._get_nvidia_version()
                        if version:
                            info['version'] = version
                    elif driver in ['amdgpu', 'radeon']:
                        version = self._get_amd_version()
                        if version:
                            info['version'] = version
                    elif driver in ['i915', 'xe']:
                        version = self._get_intel_version()
                        if version:
                            info['version'] = version
        except Exception:
            pass
        
        return info
    
    def _get_nvidia_version(self) -> str:
        """Get NVIDIA driver version"""
        if not self.nvidia_smi_available:
            return 'Unknown'
        
        try:
            output = self._run_command(['nvidia-smi', '--query-gpu=driver_version', '--format=csv,noheader'])
            if output:
                return output.split('\n')[0].strip()
        except Exception:
            pass
        
        return 'Unknown'
    
    def _get_amd_version(self) -> str:
        """Get AMD driver version"""
        try:
            output = self._run_command(['modinfo', 'amdgpu'])
            for line in output.split('\n'):
                if line.startswith('version:'):
                    return line.split(':', 1)[1].strip()
        except Exception:
            pass
        
        return 'Unknown'
    
    def _get_intel_version(self) -> str:
        """Get Intel driver version"""
        try:
            output = self._run_command(['modinfo', 'i915'])
            for line in output.split('\n'):
                if line.startswith('version:'):
                    return line.split(':', 1)[1].strip()
        except Exception:
            pass
        
        return 'Unknown'
    
    def _get_nvidia_info(self) -> List[Dict]:
        """Get detailed NVIDIA GPU information"""
        gpus = []
        
        if not self.nvidia_smi_available:
            return gpus
        
        try:
            output = self._run_command([
                'nvidia-smi',
                '--query-gpu=name,memory.total,driver_version',
                '--format=csv,noheader'
            ])
            
            for line in output.split('\n'):
                if line.strip():
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) >= 3:
                        gpus.append({
                            'device': 'NVIDIA GPU',
                            'vendor': 'NVIDIA',
                            'model': parts[0],
                            'vram': parts[1],
                            'driver': 'nvidia',
                            'driver_version': parts[2]
                        })
        except Exception:
            pass
        
        return gpus
    
    def _get_opengl_info(self) -> str:
        """Get OpenGL support information"""
        if not self.glxinfo_available:
            return 'Unknown'
        
        try:
            output = self._run_command(['glxinfo'])
            for line in output.split('\n'):
                if 'OpenGL version string:' in line:
                    return line.split(':', 1)[1].strip()
        except Exception:
            pass
        
        return 'Unknown'
    
    def _get_vulkan_info(self) -> str:
        """Get Vulkan support information"""
        if not self.vulkaninfo_available:
            return 'Unknown'
        
        try:
            output = self._run_command(['vulkaninfo', '--summary'])
            for line in output.split('\n'):
                if 'apiVersion' in line:
                    match = re.search(r'(\d+\.\d+\.\d+)', line)
                    if match:
                        return match.group(1)
        except Exception:
            pass
        
        return 'Unknown'
    
    def get_all_info(self) -> Dict:
        """Get all GPU information"""
        # Try NVIDIA first (provides more detailed info)
        nvidia_gpus = self._get_nvidia_info()
        
        # Fall back to lspci for all GPUs
        pci_gpus = self._get_pci_gpus()
        
        # Merge results (prefer NVIDIA detailed info)
        gpus = nvidia_gpus if nvidia_gpus else pci_gpus
        
        data = {
            'gpus': gpus,
            'opengl': self._get_opengl_info(),
            'vulkan': self._get_vulkan_info()
        }
        
        return data
    
    def get_summary(self) -> Dict:
        """Get summary GPU information"""
        info = self.get_all_info()
        
        gpu_count = len(info.get('gpus', []))
        gpu_names = [gpu.get('model', 'Unknown') for gpu in info.get('gpus', [])]
        
        return {
            'GPU Count': str(gpu_count),
            'Primary GPU': gpu_names[0] if gpu_names else 'Unknown'
        }
