#!/usr/bin/env python3

import os
import random
import subprocess
import time
import signal
import sys
import json
import urllib.request
import html
from pathlib import Path

class MultiMonitorWallpaper:
    def __init__(self):
        self.wallpaper_dir = Path.home() / '.config' / 'variety' / 'Downloaded'
        self.running = True
        self.monitors = self.get_monitors()
        
    def get_monitors(self):
        """Get monitor information from xrandr"""
        result = subprocess.run(['xrandr', '--query'], capture_output=True, text=True)
        monitors = []
        for line in result.stdout.split('\n'):
            if ' connected' in line and not 'disconnected' in line:
                parts = line.split()
                monitor_name = parts[0]
                # Extract resolution and position
                for part in parts:
                    if '+' in part and 'x' in part:
                        # Format: 1920x1080+1920+0
                        res_pos = part.split('+')
                        resolution = res_pos[0]
                        x_pos = res_pos[1]
                        monitors.append({
                            'name': monitor_name,
                            'resolution': resolution,
                            'x_position': int(x_pos)
                        })
                        break
        # Sort by x position to get left/right order
        monitors.sort(key=lambda x: x['x_position'])
        return monitors
    
    def get_random_wallpapers(self, count=2):
        """Get random wallpaper paths from Variety's downloads"""
        wallpapers = []
        for root, dirs, files in os.walk(self.wallpaper_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    wallpapers.append(os.path.join(root, file))
        
        if len(wallpapers) < count:
            print(f"Warning: Only found {len(wallpapers)} wallpapers")
            return wallpapers
        
        return random.sample(wallpapers, min(count, len(wallpapers)))
    
    def get_quote(self):
        """Get a random quote, similar to what Variety shows"""
        quotes = [
            ("The only way to do great work is to love what you do.", "Steve Jobs"),
            ("Life is what happens when you're busy making other plans.", "John Lennon"),
            ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
            ("It is during our darkest moments that we must focus to see the light.", "Aristotle"),
            ("The way to get started is to quit talking and begin doing.", "Walt Disney"),
            ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
            ("The pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty.", "Winston Churchill"),
            ("You learn more from failure than from success. Don't let it stop you. Failure builds character.", "Unknown"),
            ("It's not whether you get knocked down, it's whether you get up.", "Vince Lombardi"),
            ("We may encounter many defeats but we must not be defeated.", "Maya Angelou"),
        ]
        
        # Try to get quote from quotefancy or other APIs
        try:
            # Using a simple quote API
            response = urllib.request.urlopen("https://api.quotable.io/random", timeout=2)
            data = json.loads(response.read())
            return (data['content'], data['author'])
        except:
            # Fallback to local quotes
            return random.choice(quotes)
    
    def create_combined_wallpaper(self, wallpapers):
        """Create a single image spanning both monitors with quote"""
        if len(wallpapers) < 2 or len(self.monitors) < 2:
            return None
            
        output_path = Path.home() / '.cache' / 'multi-monitor-wallpaper.jpg'
        temp_path = Path.home() / '.cache' / 'temp-wallpaper.jpg'
        
        # Get dimensions for each monitor
        monitor1_width = int(self.monitors[0]['resolution'].split('x')[0])
        monitor2_width = int(self.monitors[1]['resolution'].split('x')[0])
        height = int(self.monitors[0]['resolution'].split('x')[1])
        total_width = monitor1_width + monitor2_width
        
        # Build ImageMagick command to combine images
        # Each image is resized to exactly fit its corresponding monitor
        cmd = [
            'convert',
            # First image for left monitor
            '(',
            wallpapers[0],
            '-resize', f'{monitor1_width}x{height}!',  # ! forces exact size
            ')',
            # Second image for right monitor  
            '(',
            wallpapers[1],
            '-resize', f'{monitor2_width}x{height}!',  # ! forces exact size
            ')',
            # Combine side by side
            '+append',
            str(temp_path)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Get a quote
            quote_text, quote_author = self.get_quote()
            full_quote = f'"{quote_text}"\n\n— {quote_author}'
            
            # Add quote to the bottom right using ImageMagick
            # Position on right monitor, bottom right corner
            quote_cmd = [
                'convert',
                str(temp_path),
                '-gravity', 'SouthEast',
                '-fill', 'white',
                '-font', 'Ubuntu-Bold',
                '-pointsize', '30',
                '-annotate', '+50+50',
                full_quote,
                str(output_path)
            ]
            
            # Try with shadow/background for better readability
            # Quote should appear on the right monitor (which starts at monitor1_width)
            quote_x_start = monitor1_width + 50  # 50 pixels from left edge of right monitor
            quote_y_pos = height - 150  # 150 pixels from bottom
            
            quote_cmd_with_shadow = [
                'convert',
                str(temp_path),
                # Add semi-transparent background box for quote on right monitor
                '-gravity', 'NorthWest',
                '-fill', 'rgba(0,0,0,0.4)',
                '-draw', f'roundrectangle {monitor1_width + monitor2_width - 750},{height-200} {monitor1_width + monitor2_width - 30},{height-30} 10,10',
                # Add the quote text positioned on right monitor
                '-gravity', 'NorthWest',
                '-fill', 'white',
                '-font', 'Ubuntu-Bold',
                '-pointsize', '30',
                '-annotate', f'+{monitor1_width + monitor2_width - 720}+{height-170}',
                full_quote,
                str(output_path)
            ]
            
            try:
                subprocess.run(quote_cmd_with_shadow, check=True, capture_output=True, stderr=subprocess.PIPE)
            except:
                # Fallback to simple text without background
                try:
                    subprocess.run(quote_cmd, check=True, capture_output=True)
                except:
                    # If adding quote fails, just use the combined image
                    os.rename(temp_path, output_path)
            
            # Clean up temp file
            if temp_path.exists():
                temp_path.unlink()
                
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"Error creating combined wallpaper: {e}")
            return None
    
    def set_gnome_wallpaper(self, wallpaper_path):
        """Set wallpaper using GNOME's gsettings"""
        if wallpaper_path and os.path.exists(wallpaper_path):
            uri = f"file://{wallpaper_path}"
            # First set to spanned mode for multi-monitor
            subprocess.run([
                'gsettings', 'set',
                'org.gnome.desktop.background',
                'picture-options', 'spanned'
            ])
            # Then set the wallpaper URI
            subprocess.run([
                'gsettings', 'set', 
                'org.gnome.desktop.background', 
                'picture-uri', uri
            ])
            subprocess.run([
                'gsettings', 'set',
                'org.gnome.desktop.background',
                'picture-uri-dark', uri
            ])
    
    def set_wallpapers_xwallpaper(self, wallpapers):
        """Alternative method using xwallpaper"""
        if len(wallpapers) >= 2 and len(self.monitors) >= 2:
            cmd = ['xwallpaper']
            for monitor, wallpaper in zip(self.monitors, wallpapers):
                cmd.extend(['--output', monitor['name'], '--zoom', wallpaper])
            
            try:
                subprocess.run(cmd, check=True)
                print(f"Set wallpapers with xwallpaper:")
                for monitor, wallpaper in zip(self.monitors, wallpapers):
                    print(f"  {monitor['name']}: {os.path.basename(wallpaper)}")
            except subprocess.CalledProcessError:
                print("xwallpaper failed, trying GNOME method...")
                return False
            return True
        return False
    
    def cycle_wallpapers(self):
        """Change wallpapers to new random ones"""
        wallpapers = self.get_random_wallpapers(len(self.monitors))
        
        if not wallpapers:
            print("No wallpapers found!")
            return
        
        # For GNOME, we need to use the combined wallpaper method
        print("Creating combined wallpaper for GNOME...")
        combined = self.create_combined_wallpaper(wallpapers)
        if combined:
            self.set_gnome_wallpaper(combined)
            print(f"Set combined wallpaper from:")
            for i, wallpaper in enumerate(wallpapers[:2]):
                monitor_name = self.monitors[i]['name'] if i < len(self.monitors) else f"Monitor {i}"
                print(f"  {monitor_name}: {os.path.basename(wallpaper)}")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\nShutting down wallpaper cycler...")
        self.running = False
        sys.exit(0)
    
    def run(self, interval=60):
        """Main loop to cycle wallpapers at specified interval"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print(f"Starting multi-monitor wallpaper cycler (interval: {interval}s)")
        print(f"Found {len(self.monitors)} monitors:")
        for m in self.monitors:
            print(f"  {m['name']}: {m['resolution']} at x={m['x_position']}")
        
        while self.running:
            self.cycle_wallpapers()
            time.sleep(interval)

if __name__ == "__main__":
    # Check for ImageMagick
    try:
        subprocess.run(['convert', '-version'], capture_output=True, check=True)
    except:
        print("ImageMagick not installed. Install with: sudo apt install imagemagick")
        print("Will use xwallpaper method only.")
    
    cycler = MultiMonitorWallpaper()
    cycler.run(interval=60)  # Change wallpaper every 60 seconds