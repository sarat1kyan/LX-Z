"""
Export Module
Handles exporting system information to various formats
"""

import json
import os
from datetime import datetime
from typing import Dict

class ExportReport:
    """Handles report export functionality"""
    
    def __init__(self):
        self.output_dir = os.path.expanduser("~")
    
    def export_json(self, data: Dict, filename: str = None) -> str:
        """Export data as JSON"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"lxz_report_{timestamp}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Add metadata
        export_data = {
            'generated_at': datetime.now().isoformat(),
            'generator': 'LX-Z v1.0',
            'system_info': data
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filepath
    
    def export_txt(self, data: Dict, filename: str = None) -> str:
        """Export data as formatted text"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"lxz_report_{timestamp}.txt"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w') as f:
            # Header
            f.write("="*80 + "\n")
            f.write("LX-Z - Linux Hardware Analyzer Report\n")
            f.write("="*80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            # CPU Information
            if 'cpu' in data:
                f.write("\n" + "="*80 + "\n")
                f.write("CPU INFORMATION\n")
                f.write("="*80 + "\n")
                cpu = data['cpu']
                
                f.write(f"Model: {cpu.get('model', 'Unknown')}\n")
                f.write(f"Architecture: {cpu.get('architecture', 'Unknown')}\n")
                f.write(f"Vendor ID: {cpu.get('vendor_id', 'Unknown')}\n")
                f.write(f"CPU Family: {cpu.get('cpu_family', 'Unknown')}\n")
                f.write(f"Cores: {cpu.get('cores', 'Unknown')}\n")
                f.write(f"Threads: {cpu.get('threads', 'Unknown')}\n")
                f.write(f"Current Frequency: {cpu.get('current_freq', 'Unknown')}\n")
                f.write(f"Max Frequency: {cpu.get('max_freq', 'Unknown')}\n")
                f.write(f"L1d Cache: {cpu.get('l1d_cache', 'Unknown')}\n")
                f.write(f"L1i Cache: {cpu.get('l1i_cache', 'Unknown')}\n")
                f.write(f"L2 Cache: {cpu.get('l2_cache', 'Unknown')}\n")
                f.write(f"L3 Cache: {cpu.get('l3_cache', 'Unknown')}\n")
                
                if cpu.get('flags'):
                    f.write(f"\nCPU Flags ({len(cpu['flags'])} total):\n")
                    flags_text = ', '.join(cpu['flags'])
                    # Wrap text at 80 characters
                    for i in range(0, len(flags_text), 76):
                        f.write(f"  {flags_text[i:i+76]}\n")
            
            # Memory Information
            if 'memory' in data:
                f.write("\n" + "="*80 + "\n")
                f.write("MEMORY INFORMATION\n")
                f.write("="*80 + "\n")
                mem = data['memory']
                
                f.write(f"Total RAM: {mem.get('total', 'Unknown')}\n")
                f.write(f"Available RAM: {mem.get('available', 'Unknown')}\n")
                f.write(f"Used RAM: {mem.get('used', 'Unknown')}\n")
                f.write(f"Free RAM: {mem.get('free', 'Unknown')}\n")
                f.write(f"Usage: {mem.get('percent', 'Unknown')}\n")
                f.write(f"\nSwap Total: {mem.get('swap_total', 'Unknown')}\n")
                f.write(f"Swap Used: {mem.get('swap_used', 'Unknown')}\n")
                f.write(f"Swap Free: {mem.get('swap_free', 'Unknown')}\n")
                
                if mem.get('modules'):
                    f.write(f"\nMemory Modules:\n")
                    for idx, module in enumerate(mem['modules'], 1):
                        f.write(f"  Module {idx}:\n")
                        f.write(f"    Locator: {module.get('locator', 'N/A')}\n")
                        f.write(f"    Size: {module.get('size', 'N/A')}\n")
                        f.write(f"    Type: {module.get('type', 'N/A')}\n")
                        f.write(f"    Speed: {module.get('speed', 'N/A')}\n")
                        f.write(f"    Manufacturer: {module.get('manufacturer', 'N/A')}\n")
            
            # Storage Information
            if 'storage' in data:
                f.write("\n" + "="*80 + "\n")
                f.write("STORAGE INFORMATION\n")
                f.write("="*80 + "\n")
                storage = data['storage']
                
                if storage.get('devices'):
                    f.write("\nBlock Devices:\n")
                    for device in storage['devices']:
                        f.write(f"  {device.get('name', 'Unknown')}:\n")
                        f.write(f"    Path: {device.get('path', 'Unknown')}\n")
                        f.write(f"    Model: {device.get('model', 'Unknown')}\n")
                        f.write(f"    Size: {device.get('size', 'Unknown')}\n")
                        f.write(f"    Type: {device.get('type', 'Unknown')}\n")
                
                if storage.get('partitions'):
                    f.write("\nPartitions:\n")
                    for part in storage['partitions']:
                        f.write(f"  {part.get('device', 'Unknown')}:\n")
                        f.write(f"    Mount Point: {part.get('mountpoint', 'Unknown')}\n")
                        f.write(f"    Filesystem: {part.get('fstype', 'Unknown')}\n")
                        f.write(f"    Size: {part.get('size', 'Unknown')}\n")
                        f.write(f"    Used: {part.get('used', 'Unknown')}\n")
                        f.write(f"    Free: {part.get('free', 'Unknown')}\n")
                        f.write(f"    Usage: {part.get('percent', 'Unknown')}\n")
            
            # GPU Information
            if 'gpu' in data:
                f.write("\n" + "="*80 + "\n")
                f.write("GPU INFORMATION\n")
                f.write("="*80 + "\n")
                gpu_data = data['gpu']
                
                if gpu_data.get('gpus'):
                    for idx, gpu in enumerate(gpu_data['gpus'], 1):
                        f.write(f"\nGPU #{idx}:\n")
                        f.write(f"  Vendor: {gpu.get('vendor', 'Unknown')}\n")
                        f.write(f"  Model: {gpu.get('model', 'Unknown')}\n")
                        f.write(f"  Driver: {gpu.get('driver', 'Unknown')}\n")
                        f.write(f"  Driver Version: {gpu.get('driver_version', 'Unknown')}\n")
                        if gpu.get('vram'):
                            f.write(f"  VRAM: {gpu.get('vram', 'Unknown')}\n")
                
                if gpu_data.get('opengl') or gpu_data.get('vulkan'):
                    f.write("\nGraphics API Support:\n")
                    if gpu_data.get('opengl'):
                        f.write(f"  OpenGL: {gpu_data['opengl']}\n")
                    if gpu_data.get('vulkan'):
                        f.write(f"  Vulkan: {gpu_data['vulkan']}\n")
            
            # Motherboard Information
            if 'motherboard' in data:
                f.write("\n" + "="*80 + "\n")
                f.write("MOTHERBOARD & BIOS INFORMATION\n")
                f.write("="*80 + "\n")
                mb = data['motherboard']
                
                f.write(f"Manufacturer: {mb.get('manufacturer', 'Unknown')}\n")
                f.write(f"Product: {mb.get('product', 'Unknown')}\n")
                f.write(f"Version: {mb.get('version', 'Unknown')}\n")
                f.write(f"Serial Number: {mb.get('serial', 'Unknown')}\n")
                f.write(f"\nBIOS Vendor: {mb.get('bios_vendor', 'Unknown')}\n")
                f.write(f"BIOS Version: {mb.get('bios_version', 'Unknown')}\n")
                f.write(f"BIOS Date: {mb.get('bios_date', 'Unknown')}\n")
            
            # Sensor Information
            if 'sensors' in data:
                f.write("\n" + "="*80 + "\n")
                f.write("SENSOR INFORMATION\n")
                f.write("="*80 + "\n")
                sensors = data['sensors']
                
                if sensors.get('temperatures'):
                    f.write("\nTemperatures:\n")
                    for sensor, temp in sensors['temperatures'].items():
                        f.write(f"  {sensor}: {temp}\n")
                
                if sensors.get('fans'):
                    f.write("\nFans:\n")
                    for fan, speed in sensors['fans'].items():
                        f.write(f"  {fan}: {speed}\n")
                
                if sensors.get('battery'):
                    f.write("\nBattery:\n")
                    for key, value in sensors['battery'].items():
                        f.write(f"  {key}: {value}\n")
            
            # Footer
            f.write("\n" + "="*80 + "\n")
            f.write("End of Report\n")
            f.write("="*80 + "\n")
        
        return filepath
