"""
Sensors Information Module
Gathers temperature, fan, and power information
"""

import subprocess
import os
import re
from typing import Dict, List

class SensorInfo:
    """Handles sensor information gathering"""
    
    def __init__(self):
        self.sensors_available = self._check_command("sensors")
    
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
    
    def _get_thermal_zones(self) -> Dict[str, str]:
        """Get temperature from thermal zones"""
        temps = {}
        
        try:
            thermal_path = "/sys/class/thermal"
            if os.path.exists(thermal_path):
                for zone in os.listdir(thermal_path):
                    if zone.startswith('thermal_zone'):
                        temp_file = os.path.join(thermal_path, zone, 'temp')
                        type_file = os.path.join(thermal_path, zone, 'type')
                        
                        if os.path.exists(temp_file):
                            try:
                                with open(temp_file) as f:
                                    temp = int(f.read().strip()) / 1000.0  # millidegrees to degrees
                                
                                # Get zone type/name
                                zone_name = zone
                                if os.path.exists(type_file):
                                    with open(type_file) as f:
                                        zone_name = f.read().strip()
                                
                                temps[zone_name] = f"{temp:.1f}°C"
                            except Exception:
                                continue
        except Exception:
            pass
        
        return temps
    
    def _get_hwmon_temps(self) -> Dict[str, str]:
        """Get temperature from hwmon"""
        temps = {}
        
        try:
            hwmon_path = "/sys/class/hwmon"
            if os.path.exists(hwmon_path):
                for hwmon in os.listdir(hwmon_path):
                    hwmon_dir = os.path.join(hwmon_path, hwmon)
                    
                    # Get device name
                    name_file = os.path.join(hwmon_dir, 'name')
                    device_name = hwmon
                    if os.path.exists(name_file):
                        with open(name_file) as f:
                            device_name = f.read().strip()
                    
                    # Find temperature inputs
                    for item in os.listdir(hwmon_dir):
                        if item.startswith('temp') and item.endswith('_input'):
                            temp_file = os.path.join(hwmon_dir, item)
                            label_file = os.path.join(hwmon_dir, item.replace('_input', '_label'))
                            
                            try:
                                with open(temp_file) as f:
                                    temp = int(f.read().strip()) / 1000.0
                                
                                # Get label if available
                                label = item.replace('_input', '')
                                if os.path.exists(label_file):
                                    with open(label_file) as f:
                                        label = f.read().strip()
                                
                                sensor_name = f"{device_name} - {label}"
                                temps[sensor_name] = f"{temp:.1f}°C"
                            except Exception:
                                continue
        except Exception:
            pass
        
        return temps
    
    def _get_lm_sensors_info(self) -> Dict:
        """Get information from lm-sensors"""
        data = {
            'temperatures': {},
            'fans': {}
        }
        
        if not self.sensors_available:
            return data
        
        try:
            output = self._run_command(['sensors'])
            
            current_adapter = None
            for line in output.split('\n'):
                line = line.strip()
                
                if not line or line.startswith('Adapter:'):
                    continue
                
                # Parse sensor line
                if ':' in line:
                    parts = line.split(':')
                    sensor_name = parts[0].strip()
                    sensor_value = parts[1].strip()
                    
                    # Temperature
                    if '°C' in sensor_value:
                        # Extract temperature value
                        temp_match = re.search(r'[+-]?\d+\.\d+°C', sensor_value)
                        if temp_match:
                            data['temperatures'][sensor_name] = temp_match.group()
                    
                    # Fan speed
                    elif 'RPM' in sensor_value:
                        rpm_match = re.search(r'\d+\s*RPM', sensor_value)
                        if rpm_match:
                            data['fans'][sensor_name] = rpm_match.group()
        except Exception:
            pass
        
        return data
    
    def _get_battery_info(self) -> Dict:
        """Get battery information if available"""
        battery = {}
        
        try:
            power_supply_path = "/sys/class/power_supply"
            if os.path.exists(power_supply_path):
                for device in os.listdir(power_supply_path):
                    if device.startswith('BAT'):
                        device_path = os.path.join(power_supply_path, device)
                        
                        # Capacity
                        capacity_file = os.path.join(device_path, 'capacity')
                        if os.path.exists(capacity_file):
                            with open(capacity_file) as f:
                                battery['Capacity'] = f"{f.read().strip()}%"
                        
                        # Status
                        status_file = os.path.join(device_path, 'status')
                        if os.path.exists(status_file):
                            with open(status_file) as f:
                                battery['Status'] = f.read().strip()
                        
                        # Energy now
                        energy_now_file = os.path.join(device_path, 'energy_now')
                        energy_full_file = os.path.join(device_path, 'energy_full')
                        if os.path.exists(energy_now_file) and os.path.exists(energy_full_file):
                            with open(energy_now_file) as f:
                                energy_now = int(f.read().strip()) / 1000000  # Convert to Wh
                            with open(energy_full_file) as f:
                                energy_full = int(f.read().strip()) / 1000000
                            battery['Energy'] = f"{energy_now:.2f} Wh / {energy_full:.2f} Wh"
                        
                        # Manufacturer
                        manufacturer_file = os.path.join(device_path, 'manufacturer')
                        if os.path.exists(manufacturer_file):
                            with open(manufacturer_file) as f:
                                battery['Manufacturer'] = f.read().strip()
                        
                        # Model
                        model_file = os.path.join(device_path, 'model_name')
                        if os.path.exists(model_file):
                            with open(model_file) as f:
                                battery['Model'] = f.read().strip()
                        
                        break  # Only process first battery
        except Exception:
            pass
        
        return battery
    
    def get_all_info(self) -> Dict:
        """Get all sensor information"""
        data = {}
        
        # Try lm-sensors first
        lm_data = self._get_lm_sensors_info()
        
        if lm_data['temperatures']:
            data['temperatures'] = lm_data['temperatures']
        else:
            # Fallback to thermal zones and hwmon
            thermal_temps = self._get_thermal_zones()
            hwmon_temps = self._get_hwmon_temps()
            
            # Merge temperature sources
            all_temps = {}
            all_temps.update(thermal_temps)
            all_temps.update(hwmon_temps)
            
            if all_temps:
                data['temperatures'] = all_temps
        
        if lm_data['fans']:
            data['fans'] = lm_data['fans']
        
        # Battery information
        battery_info = self._get_battery_info()
        if battery_info:
            data['battery'] = battery_info
        
        return data
    
    def get_summary(self) -> Dict:
        """Get summary sensor information"""
        info = self.get_all_info()
        
        summary = {}
        
        if info.get('temperatures'):
            temp_count = len(info['temperatures'])
            summary['Temperature Sensors'] = str(temp_count)
        
        if info.get('fans'):
            fan_count = len(info['fans'])
            summary['Fans Detected'] = str(fan_count)
        
        if info.get('battery'):
            summary['Battery'] = info['battery'].get('Capacity', 'Unknown')
        
        return summary if summary else {'Sensors': 'No data available'}
