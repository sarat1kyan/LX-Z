#!/usr/bin/env python3
"""
LX-Z - Linux Hardware Analyzer
A professional CPU-Z alternative for Linux systems
"""

import sys
import os
from typing import Optional

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.text import Text
    from rich import box
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError:
    print("Error: Required 'rich' library not found.")
    print("Please run: pip3 install rich --break-system-packages")
    sys.exit(1)

from utils.cpu import CPUInfo
from utils.memory import MemoryInfo
from utils.storage import StorageInfo
from utils.gpu import GPUInfo
from utils.sensors import SensorInfo
from utils.exporter import ExportReport

console = Console()

class LXZ:
    """Main application class for LX-Z"""
    
    def __init__(self):
        self.cpu_info = CPUInfo()
        self.memory_info = MemoryInfo()
        self.storage_info = StorageInfo()
        self.gpu_info = GPUInfo()
        self.sensor_info = SensorInfo()
        self.exporter = ExportReport()
        
    def show_banner(self):
        """Display the application banner"""
        banner = """
╦  ═╗ ╦   ╔═╗
║   ╔╝   ╔═╝
╩═╝ ╩    ╚═╝
        """
        
        title = Text(banner, style="bold cyan")
        subtitle = Text("Linux Hardware Analyzer v1.0", style="italic bright_white")
        info = Text("A professional CPU-Z alternative for Linux", style="dim")
        
        panel = Panel.fit(
            f"{title}\n{subtitle}\n{info}",
            border_style="bright_cyan",
            padding=(1, 2)
        )
        console.print(panel)
        console.print()
    
    def show_menu(self):
        """Display the main menu"""
        table = Table(
            title="[bold cyan]Main Menu[/bold cyan]",
            box=box.ROUNDED,
            border_style="cyan",
            show_header=False,
            padding=(0, 2)
        )
        
        table.add_column("Option", style="bold yellow", width=8)
        table.add_column("Description", style="bright_white")
        
        menu_items = [
            ("1", "🔹 CPU Information"),
            ("2", "🔹 Memory (RAM) Information"),
            ("3", "🔹 Storage Devices"),
            ("4", "🔹 GPU Information"),
            ("5", "🔹 Motherboard & BIOS"),
            ("6", "🔹 Sensors & Hardware Monitor"),
            ("7", "🔹 Complete System Overview"),
            ("8", "🔹 Export Report (JSON/TXT)"),
            ("0", "🔹 Exit")
        ]
        
        for option, description in menu_items:
            table.add_row(f"[{option}]", description)
        
        console.print(table)
        console.print()
    
    def show_cpu_info(self):
        """Display CPU information"""
        console.clear()
        self.show_banner()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Gathering CPU information...", total=None)
            data = self.cpu_info.get_all_info()
            progress.remove_task(task)
        
        # CPU Model & Basic Info
        basic_table = Table(
            title="[bold cyan]CPU Information[/bold cyan]",
            box=box.DOUBLE_EDGE,
            border_style="cyan",
            show_header=True,
            header_style="bold magenta"
        )
        basic_table.add_column("Property", style="yellow", width=25)
        basic_table.add_column("Value", style="bright_white")
        
        basic_table.add_row("Processor", data.get('model', 'Unknown'))
        basic_table.add_row("Architecture", data.get('architecture', 'Unknown'))
        basic_table.add_row("Vendor ID", data.get('vendor_id', 'Unknown'))
        basic_table.add_row("CPU Family", data.get('cpu_family', 'Unknown'))
        basic_table.add_row("Model Number", data.get('model_number', 'Unknown'))
        basic_table.add_row("Stepping", data.get('stepping', 'Unknown'))
        
        console.print(basic_table)
        console.print()
        
        # Core & Thread Info
        core_table = Table(
            title="[bold cyan]Core & Thread Configuration[/bold cyan]",
            box=box.ROUNDED,
            border_style="cyan"
        )
        core_table.add_column("Property", style="yellow", width=25)
        core_table.add_column("Value", style="bright_white")
        
        core_table.add_row("Physical Cores", str(data.get('cores', 'Unknown')))
        core_table.add_row("Logical Processors", str(data.get('threads', 'Unknown')))
        core_table.add_row("Sockets", str(data.get('sockets', 'Unknown')))
        
        console.print(core_table)
        console.print()
        
        # Frequency Info
        freq_table = Table(
            title="[bold cyan]Frequency Information[/bold cyan]",
            box=box.ROUNDED,
            border_style="cyan"
        )
        freq_table.add_column("Property", style="yellow", width=25)
        freq_table.add_column("Value", style="bright_white")
        
        freq_table.add_row("Current Frequency", data.get('current_freq', 'Unknown'))
        freq_table.add_row("Maximum Frequency", data.get('max_freq', 'Unknown'))
        freq_table.add_row("Minimum Frequency", data.get('min_freq', 'Unknown'))
        
        console.print(freq_table)
        console.print()
        
        # Cache Info
        cache_table = Table(
            title="[bold cyan]Cache Information[/bold cyan]",
            box=box.ROUNDED,
            border_style="cyan"
        )
        cache_table.add_column("Cache Level", style="yellow", width=25)
        cache_table.add_column("Size", style="bright_white")
        
        cache_table.add_row("L1 Data Cache", data.get('l1d_cache', 'Unknown'))
        cache_table.add_row("L1 Instruction Cache", data.get('l1i_cache', 'Unknown'))
        cache_table.add_row("L2 Cache", data.get('l2_cache', 'Unknown'))
        cache_table.add_row("L3 Cache", data.get('l3_cache', 'Unknown'))
        
        console.print(cache_table)
        console.print()
        
        # CPU Flags (Features)
        if data.get('flags'):
            flags_text = ", ".join(data['flags'][:30])  # Show first 30 flags
            flags_panel = Panel(
                flags_text,
                title="[bold cyan]CPU Features (Selected)[/bold cyan]",
                border_style="cyan",
                padding=(1, 2)
            )
            console.print(flags_panel)
            console.print()
        
        self.pause()
    
    def show_memory_info(self):
        """Display memory information"""
        console.clear()
        self.show_banner()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Gathering memory information...", total=None)
            data = self.memory_info.get_all_info()
            progress.remove_task(task)
        
        # Memory Overview
        mem_table = Table(
            title="[bold cyan]Memory Overview[/bold cyan]",
            box=box.DOUBLE_EDGE,
            border_style="cyan"
        )
        mem_table.add_column("Property", style="yellow", width=25)
        mem_table.add_column("Value", style="bright_white")
        
        mem_table.add_row("Total RAM", data.get('total', 'Unknown'))
        mem_table.add_row("Available RAM", data.get('available', 'Unknown'))
        mem_table.add_row("Used RAM", data.get('used', 'Unknown'))
        mem_table.add_row("Free RAM", data.get('free', 'Unknown'))
        mem_table.add_row("Usage Percentage", data.get('percent', 'Unknown'))
        
        console.print(mem_table)
        console.print()
        
        # Swap Information
        swap_table = Table(
            title="[bold cyan]Swap Information[/bold cyan]",
            box=box.ROUNDED,
            border_style="cyan"
        )
        swap_table.add_column("Property", style="yellow", width=25)
        swap_table.add_column("Value", style="bright_white")
        
        swap_table.add_row("Total Swap", data.get('swap_total', 'Unknown'))
        swap_table.add_row("Used Swap", data.get('swap_used', 'Unknown'))
        swap_table.add_row("Free Swap", data.get('swap_free', 'Unknown'))
        swap_table.add_row("Swap Usage", data.get('swap_percent', 'Unknown'))
        
        console.print(swap_table)
        console.print()
        
        # Memory Modules (if detected)
        if data.get('modules'):
            modules_table = Table(
                title="[bold cyan]Memory Modules (DMI)[/bold cyan]",
                box=box.ROUNDED,
                border_style="cyan"
            )
            modules_table.add_column("Slot", style="yellow")
            modules_table.add_column("Size", style="bright_white")
            modules_table.add_column("Type", style="bright_white")
            modules_table.add_column("Speed", style="bright_white")
            modules_table.add_column("Manufacturer", style="bright_white")
            
            for module in data['modules']:
                modules_table.add_row(
                    module.get('locator', 'N/A'),
                    module.get('size', 'N/A'),
                    module.get('type', 'N/A'),
                    module.get('speed', 'N/A'),
                    module.get('manufacturer', 'N/A')
                )
            
            console.print(modules_table)
            console.print()
        
        self.pause()
    
    def show_storage_info(self):
        """Display storage information"""
        console.clear()
        self.show_banner()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Gathering storage information...", total=None)
            data = self.storage_info.get_all_info()
            progress.remove_task(task)
        
        # Storage Devices
        if data.get('devices'):
            for device in data['devices']:
                device_table = Table(
                    title=f"[bold cyan]Device: {device.get('name', 'Unknown')}[/bold cyan]",
                    box=box.DOUBLE_EDGE,
                    border_style="cyan"
                )
                device_table.add_column("Property", style="yellow", width=25)
                device_table.add_column("Value", style="bright_white")
                
                device_table.add_row("Device Path", device.get('path', 'Unknown'))
                device_table.add_row("Model", device.get('model', 'Unknown'))
                device_table.add_row("Size", device.get('size', 'Unknown'))
                device_table.add_row("Type", device.get('type', 'Unknown'))
                device_table.add_row("Removable", device.get('removable', 'Unknown'))
                device_table.add_row("Read-Only", device.get('readonly', 'Unknown'))
                
                console.print(device_table)
                console.print()
        
        # Partitions
        if data.get('partitions'):
            part_table = Table(
                title="[bold cyan]Partitions & Filesystems[/bold cyan]",
                box=box.ROUNDED,
                border_style="cyan"
            )
            part_table.add_column("Device", style="yellow")
            part_table.add_column("Mount Point", style="bright_white")
            part_table.add_column("Filesystem", style="bright_white")
            part_table.add_column("Size", style="bright_white")
            part_table.add_column("Used", style="bright_white")
            part_table.add_column("Available", style="bright_white")
            part_table.add_column("Usage", style="bright_white")
            
            for part in data['partitions']:
                part_table.add_row(
                    part.get('device', 'N/A'),
                    part.get('mountpoint', 'N/A'),
                    part.get('fstype', 'N/A'),
                    part.get('size', 'N/A'),
                    part.get('used', 'N/A'),
                    part.get('free', 'N/A'),
                    part.get('percent', 'N/A')
                )
            
            console.print(part_table)
            console.print()
        
        self.pause()
    
    def show_gpu_info(self):
        """Display GPU information"""
        console.clear()
        self.show_banner()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Gathering GPU information...", total=None)
            data = self.gpu_info.get_all_info()
            progress.remove_task(task)
        
        if data.get('gpus'):
            for idx, gpu in enumerate(data['gpus'], 1):
                gpu_table = Table(
                    title=f"[bold cyan]GPU #{idx}[/bold cyan]",
                    box=box.DOUBLE_EDGE,
                    border_style="cyan"
                )
                gpu_table.add_column("Property", style="yellow", width=25)
                gpu_table.add_column("Value", style="bright_white")
                
                gpu_table.add_row("Device", gpu.get('device', 'Unknown'))
                gpu_table.add_row("Vendor", gpu.get('vendor', 'Unknown'))
                gpu_table.add_row("Model", gpu.get('model', 'Unknown'))
                gpu_table.add_row("Driver", gpu.get('driver', 'Unknown'))
                gpu_table.add_row("Driver Version", gpu.get('driver_version', 'Unknown'))
                
                if gpu.get('vram'):
                    gpu_table.add_row("VRAM", gpu.get('vram', 'Unknown'))
                
                console.print(gpu_table)
                console.print()
        else:
            console.print("[yellow]No GPU information available[/yellow]")
            console.print()
        
        # Graphics API Support
        if data.get('opengl') or data.get('vulkan'):
            api_table = Table(
                title="[bold cyan]Graphics API Support[/bold cyan]",
                box=box.ROUNDED,
                border_style="cyan"
            )
            api_table.add_column("API", style="yellow", width=25)
            api_table.add_column("Status", style="bright_white")
            
            if data.get('opengl'):
                api_table.add_row("OpenGL", data['opengl'])
            if data.get('vulkan'):
                api_table.add_row("Vulkan", data['vulkan'])
            
            console.print(api_table)
            console.print()
        
        self.pause()
    
    def show_motherboard_info(self):
        """Display motherboard and BIOS information"""
        console.clear()
        self.show_banner()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Gathering motherboard information...", total=None)
            data = self.memory_info.get_motherboard_info()
            progress.remove_task(task)
        
        # Motherboard Info
        mb_table = Table(
            title="[bold cyan]Motherboard Information[/bold cyan]",
            box=box.DOUBLE_EDGE,
            border_style="cyan"
        )
        mb_table.add_column("Property", style="yellow", width=25)
        mb_table.add_column("Value", style="bright_white")
        
        mb_table.add_row("Manufacturer", data.get('manufacturer', 'Unknown'))
        mb_table.add_row("Product Name", data.get('product', 'Unknown'))
        mb_table.add_row("Version", data.get('version', 'Unknown'))
        mb_table.add_row("Serial Number", data.get('serial', 'Unknown'))
        
        console.print(mb_table)
        console.print()
        
        # BIOS Info
        bios_table = Table(
            title="[bold cyan]BIOS/UEFI Information[/bold cyan]",
            box=box.ROUNDED,
            border_style="cyan"
        )
        bios_table.add_column("Property", style="yellow", width=25)
        bios_table.add_column("Value", style="bright_white")
        
        bios_table.add_row("Vendor", data.get('bios_vendor', 'Unknown'))
        bios_table.add_row("Version", data.get('bios_version', 'Unknown'))
        bios_table.add_row("Release Date", data.get('bios_date', 'Unknown'))
        
        console.print(bios_table)
        console.print()
        
        self.pause()
    
    def show_sensor_info(self):
        """Display sensor and hardware monitor information"""
        console.clear()
        self.show_banner()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Gathering sensor information...", total=None)
            data = self.sensor_info.get_all_info()
            progress.remove_task(task)
        
        # Temperature Sensors
        if data.get('temperatures'):
            temp_table = Table(
                title="[bold cyan]Temperature Sensors[/bold cyan]",
                box=box.DOUBLE_EDGE,
                border_style="cyan"
            )
            temp_table.add_column("Sensor", style="yellow", width=30)
            temp_table.add_column("Temperature", style="bright_white")
            temp_table.add_column("Status", style="bright_white")
            
            for sensor, temp in data['temperatures'].items():
                temp_value = float(temp.replace('°C', '').strip()) if '°C' in temp else 0
                if temp_value > 80:
                    status = "[red]Hot[/red]"
                elif temp_value > 60:
                    status = "[yellow]Warm[/yellow]"
                else:
                    status = "[green]Normal[/green]"
                
                temp_table.add_row(sensor, temp, status)
            
            console.print(temp_table)
            console.print()
        
        # Fan Speeds
        if data.get('fans'):
            fan_table = Table(
                title="[bold cyan]Fan Speeds[/bold cyan]",
                box=box.ROUNDED,
                border_style="cyan"
            )
            fan_table.add_column("Fan", style="yellow", width=30)
            fan_table.add_column("Speed (RPM)", style="bright_white")
            
            for fan, speed in data['fans'].items():
                fan_table.add_row(fan, speed)
            
            console.print(fan_table)
            console.print()
        
        # Battery Info (if laptop)
        if data.get('battery'):
            battery_table = Table(
                title="[bold cyan]Battery Information[/bold cyan]",
                box=box.ROUNDED,
                border_style="cyan"
            )
            battery_table.add_column("Property", style="yellow", width=25)
            battery_table.add_column("Value", style="bright_white")
            
            for key, value in data['battery'].items():
                battery_table.add_row(key, value)
            
            console.print(battery_table)
            console.print()
        
        if not data.get('temperatures') and not data.get('fans') and not data.get('battery'):
            console.print("[yellow]No sensor information available. Run with sudo for better results.[/yellow]")
            console.print()
        
        self.pause()
    
    def show_complete_overview(self):
        """Display a complete system overview"""
        console.clear()
        self.show_banner()
        
        console.print("[bold cyan]Generating complete system report...[/bold cyan]\n")
        
        # Show all sections in compact form
        sections = [
            ("CPU", self.cpu_info.get_summary),
            ("Memory", self.memory_info.get_summary),
            ("Storage", self.storage_info.get_summary),
            ("GPU", self.gpu_info.get_summary),
        ]
        
        for title, getter in sections:
            data = getter()
            table = Table(
                title=f"[bold cyan]{title}[/bold cyan]",
                box=box.SIMPLE,
                border_style="cyan",
                show_header=False
            )
            table.add_column("Property", style="yellow")
            table.add_column("Value", style="bright_white")
            
            for key, value in data.items():
                table.add_row(key, str(value))
            
            console.print(table)
            console.print()
        
        self.pause()
    
    def export_report(self):
        """Export system information to file"""
        console.clear()
        self.show_banner()
        
        console.print("[bold cyan]Export Options:[/bold cyan]\n")
        console.print("[1] Export as JSON")
        console.print("[2] Export as TXT")
        console.print("[3] Export both formats")
        console.print("[0] Cancel\n")
        
        choice = console.input("[bold yellow]Select option:[/bold yellow] ").strip()
        
        if choice == "0":
            return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Collecting system information...", total=None)
            
            # Gather all data
            all_data = {
                'cpu': self.cpu_info.get_all_info(),
                'memory': self.memory_info.get_all_info(),
                'storage': self.storage_info.get_all_info(),
                'gpu': self.gpu_info.get_all_info(),
                'sensors': self.sensor_info.get_all_info(),
                'motherboard': self.memory_info.get_motherboard_info()
            }
            
            progress.update(task, description="[cyan]Exporting report...")
            
            if choice in ["1", "3"]:
                json_file = self.exporter.export_json(all_data)
                console.print(f"\n[green]✓[/green] JSON report exported to: [bold]{json_file}[/bold]")
            
            if choice in ["2", "3"]:
                txt_file = self.exporter.export_txt(all_data)
                console.print(f"[green]✓[/green] TXT report exported to: [bold]{txt_file}[/bold]")
            
            progress.remove_task(task)
        
        console.print()
        self.pause()
    
    def pause(self):
        """Pause and wait for user input"""
        console.print()
        console.input("[dim]Press Enter to continue...[/dim]")
    
    def run(self):
        """Main application loop"""
        while True:
            console.clear()
            self.show_banner()
            self.show_menu()
            
            choice = console.input("[bold yellow]Select an option:[/bold yellow] ").strip()
            
            if choice == "1":
                self.show_cpu_info()
            elif choice == "2":
                self.show_memory_info()
            elif choice == "3":
                self.show_storage_info()
            elif choice == "4":
                self.show_gpu_info()
            elif choice == "5":
                self.show_motherboard_info()
            elif choice == "6":
                self.show_sensor_info()
            elif choice == "7":
                self.show_complete_overview()
            elif choice == "8":
                self.export_report()
            elif choice == "0":
                console.clear()
                console.print("\n[bold cyan]Thank you for using LX-Z![/bold cyan]")
                console.print("[dim]Goodbye![/dim]\n")
                sys.exit(0)
            else:
                console.print("[red]Invalid option. Please try again.[/red]")
                self.pause()

def main():
    """Entry point"""
    if os.geteuid() != 0:
        console.print("[yellow]Warning: Running without root privileges.[/yellow]")
        console.print("[yellow]Some information may be limited. Consider running with sudo.[/yellow]\n")
    
    try:
        app = LXZ()
        app.run()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
