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
        self.used_wallpapers = set()  # Track recently used wallpapers
        self.download_counter = 0  # Counter to trigger fresh downloads
        print(f"Wallpaper directory: {self.wallpaper_dir}")
        print(f"Directory exists: {self.wallpaper_dir.exists()}")
        
        # Check available images on startup
        available_images = self.count_available_images()
        print(f"Found {available_images} wallpapers in collection")
        
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
    
    def count_available_images(self):
        """Count available wallpaper images"""
        count = 0
        for root, dirs, files in os.walk(self.wallpaper_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    count += 1
        return count
    
    def trigger_variety_download(self):
        """Trigger Variety to download fresh wallpapers"""
        try:
            # Try to trigger Variety to download new images
            # This works by sending commands to the running Variety instance
            subprocess.run(['variety', '--next'], capture_output=True, timeout=5)
            subprocess.run(['variety', '--next'], capture_output=True, timeout=5)  # Trigger 2 downloads
            print("Triggered fresh wallpaper downloads from Variety")
            return True
        except:
            print("Could not trigger Variety downloads")
            return False
    
    def get_random_wallpapers(self, count=2):
        """Get random wallpaper paths from Variety's downloads"""
        wallpapers = []
        for root, dirs, files in os.walk(self.wallpaper_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    wallpapers.append(os.path.join(root, file))
        
        print(f"Found {len(wallpapers)} wallpapers in collection")
        
        if len(wallpapers) < count:
            print(f"WARNING: Only found {len(wallpapers)} wallpapers, need {count}")
            if wallpapers:
                # Duplicate what we have to meet the requirement
                while len(wallpapers) < count:
                    wallpapers.extend(wallpapers[:count-len(wallpapers)])
                return wallpapers[:count]
            else:
                print(f"ERROR: No wallpapers found in {self.wallpaper_dir}")
                return []
        
        # Trigger fresh downloads occasionally
        self.download_counter += 1
        if self.download_counter % 10 == 0:
            print("Requesting fresh downloads from Variety...")
            self.trigger_variety_download()
        
        # Smart selection: avoid recently used when possible
        unused_wallpapers = [w for w in wallpapers if w not in self.used_wallpapers]
        
        try:
            if len(unused_wallpapers) >= count:
                selected = random.sample(unused_wallpapers, count)
            else:
                # Reset used list if we've used most wallpapers
                if len(self.used_wallpapers) > len(wallpapers) * 0.8:
                    print("Resetting used wallpaper list for more variety...")
                    self.used_wallpapers.clear()
                
                # Select from all available wallpapers
                selected = random.sample(wallpapers, count)
        except Exception as e:
            print(f"ERROR in wallpaper selection: {e}")
            # Fallback: just pick the first few wallpapers
            selected = wallpapers[:count] if len(wallpapers) >= count else wallpapers
        
        # Ensure no duplicates in current selection
        while len(set(selected)) < len(selected):
            # Replace duplicates
            for i in range(1, len(selected)):
                if selected[i] in selected[:i]:
                    alternatives = [w for w in wallpapers if w not in selected]
                    if alternatives:
                        selected[i] = random.choice(alternatives)
        
        # Mark selected wallpapers as used
        self.used_wallpapers.update(selected)
        
        print(f"Selected: {[os.path.basename(w) for w in selected]} (tracking {len(self.used_wallpapers)}/{len(wallpapers)} used)")
        return selected
    
    def get_quote(self):
        """Get a random quote from multiple sources like Variety uses"""
        # Expanded local quotes database (similar to what Variety might have)
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
            ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
            ("Be yourself; everyone else is already taken.", "Oscar Wilde"),
            ("Two things are infinite: the universe and human stupidity; and I'm not sure about the universe.", "Albert Einstein"),
            ("So many books, so little time.", "Frank Zappa"),
            ("A room without books is like a body without a soul.", "Marcus Tullius Cicero"),
            ("If you want to know what a man's like, take a good look at how he treats his inferiors, not his equals.", "J.K. Rowling"),
            ("Don't walk in front of me… I may not follow. Don't walk behind me… I may not lead. Walk beside me… just be my friend.", "Albert Camus"),
            ("No one can make you feel inferior without your consent.", "Eleanor Roosevelt"),
            ("If you tell the truth, you don't have to remember anything.", "Mark Twain"),
            ("The only impossible journey is the one you never begin.", "Tony Robbins"),
            ("In the end, we will remember not the words of our enemies, but the silence of our friends.", "Martin Luther King Jr."),
            ("The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"),
            ("Your time is limited, don't waste it living someone else's life.", "Steve Jobs"),
            ("Whether you think you can or you think you can't, you're right.", "Henry Ford"),
            ("The future depends on what you do today.", "Mahatma Gandhi")
        ]
        
        # Try multiple quote APIs (similar to what Variety might use)
        quote_apis = [
            {
                'url': 'https://zenquotes.io/api/random',
                'parser': lambda data: (json.loads(data)[0]['q'], json.loads(data)[0]['a'])
            },
            {
                'url': 'https://api.quotable.io/random',
                'parser': lambda data: (json.loads(data)['content'], json.loads(data)['author'])
            }
        ]
        
        # Try each API
        for api in quote_apis:
            try:
                import ssl
                # Create SSL context that accepts weaker certificates (for older APIs)
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                
                response = urllib.request.urlopen(api['url'], timeout=3, context=ctx)
                data = response.read().decode('utf-8')
                quote_text, quote_author = api['parser'](data)
                
                # Clean up author name (remove extra info)
                if quote_author and quote_author.strip():
                    quote_author = quote_author.split(',')[0].strip()  # Remove birth dates, etc.
                else:
                    quote_author = "Unknown"
                    
                return (quote_text, quote_author)
            except Exception as e:
                continue  # Try next API
        
        # If all APIs fail, use local quotes
        return random.choice(quotes)
    
    def validate_image_dimensions(self, image_path):
        """Validate image has reasonable dimensions to prevent stretching"""
        try:
            result = subprocess.run(
                ['identify', '-format', '%wx%h', image_path],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if result.returncode == 0:
                dimensions = result.stdout.strip()
                width, height = map(int, dimensions.split('x'))
                
                # Skip very small images (likely thumbnails) or very thin images
                if width < 800 or height < 600:
                    print(f"Skipping small image {os.path.basename(image_path)}: {dimensions}")
                    return False
                
                # Skip images with extreme aspect ratios that would stretch badly
                aspect_ratio = width / height
                if aspect_ratio < 0.7 or aspect_ratio > 3.0:
                    print(f"Skipping image with extreme aspect ratio {os.path.basename(image_path)}: {dimensions} (ratio: {aspect_ratio:.2f})")
                    return False
                    
                return True
            return False
        except Exception as e:
            print(f"Could not validate {os.path.basename(image_path)}: {e}")
            return False

    def create_combined_wallpaper(self, wallpapers):
        """Create a single image spanning both monitors with quote"""
        if len(wallpapers) < 2 or len(self.monitors) < 2:
            return None
        
        # Pre-validate individual images to prevent stretching issues
        valid_wallpapers = []
        for wp in wallpapers:
            if self.validate_image_dimensions(wp):
                valid_wallpapers.append(wp)
            else:
                print(f"Replacing invalid wallpaper: {os.path.basename(wp)}")
        
        # If we don't have enough valid wallpapers, get replacements
        if len(valid_wallpapers) < 2:
            print("Need replacement wallpapers due to validation failures")
            all_wallpapers = self.get_random_wallpapers(10)  # Get more options
            for wp in all_wallpapers:
                if wp not in wallpapers and self.validate_image_dimensions(wp):
                    valid_wallpapers.append(wp)
                    if len(valid_wallpapers) >= 2:
                        break
        
        # If still not enough valid wallpapers, skip this cycle
        if len(valid_wallpapers) < 2:
            print("ERROR: Could not find enough valid wallpapers, skipping cycle")
            return None
            
        wallpapers = valid_wallpapers[:2]  # Use the validated wallpapers
            
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
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(f"ERROR: ImageMagick combine failed: {result.stderr}")
                return None
            
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
            # Create a text overlay that fits properly on the right monitor
            overlay_width = 800  # Wider to accommodate more text
            
            # Smart truncation - only truncate if really necessary
            if len(full_quote) > 250:  # Much more generous limit
                # Find a good breaking point (end of sentence or comma)
                truncate_pos = 200
                while truncate_pos > 150 and full_quote[truncate_pos] not in '.!?,':
                    truncate_pos -= 1
                if truncate_pos <= 150:  # If no good break point, use word boundary
                    words = full_quote.split()
                    truncated_words = []
                    char_count = 0
                    for word in words:
                        if char_count + len(word) + 1 > 200:
                            break
                        truncated_words.append(word)
                        char_count += len(word) + 1
                    full_quote = ' '.join(truncated_words) + '...'
                else:
                    full_quote = full_quote[:truncate_pos + 1] + '...'
            
            # Create text first to get its dimensions, then create properly sized background
            text_width = overlay_width
            padding = 40
            
            # First, create just the text to see how much space it needs
            text_cmd = [
                'convert',
                '-background', 'none',
                '-fill', 'white',
                '-font', 'Ubuntu-Bold',
                '-pointsize', '24',
                '-size', f'{text_width}x',  # Auto height
                '-gravity', 'center',
                f'caption:{full_quote}',
                str(Path.home() / '.cache' / 'text-temp.png')
            ]
            
            # Create the text image
            subprocess.run(text_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Get the dimensions of the created text
            try:
                result = subprocess.run(
                    ['identify', '-format', '%wx%h', str(Path.home() / '.cache' / 'text-temp.png')],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                if result.returncode == 0:
                    text_dimensions = result.stdout.strip()
                    text_w, text_h = map(int, text_dimensions.split('x'))
                    
                    # Calculate box dimensions with padding
                    box_width = text_w + (padding * 2)
                    box_height = text_h + (padding * 2)
                else:
                    # Fallback dimensions
                    box_width = overlay_width + 100
                    box_height = 120
            except:
                # Fallback dimensions
                box_width = overlay_width + 100
                box_height = 120
            
            # Now create the final overlay with proper background
            overlay_cmd = [
                'convert',
                '-size', f'{box_width}x{box_height}',
                'xc:none',
                # Draw rounded rectangle background
                '-fill', 'rgba(0,0,0,0.6)',
                '-draw', f'roundrectangle 0,0 {box_width-1},{box_height-1} 25,25',
                # Composite the text on top
                str(Path.home() / '.cache' / 'text-temp.png'),
                '-gravity', 'center',
                '-composite',
                str(Path.home() / '.cache' / 'quote-overlay.png')
            ]
            
            # Create the text overlay first
            subprocess.run(overlay_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Now composite the overlay onto the wallpaper
            # Position it on the right monitor, bottom-right corner
            overlay_x = monitor1_width + monitor2_width - box_width - 50
            overlay_y = height - box_height - 50  # Position from top
            
            quote_cmd_with_shadow = [
                'convert',
                str(temp_path),
                str(Path.home() / '.cache' / 'quote-overlay.png'),
                '-geometry', f'+{overlay_x}+{overlay_y}',
                '-composite',
                str(output_path)
            ]
            
            try:
                result = subprocess.run(quote_cmd_with_shadow, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode != 0:
                    raise subprocess.CalledProcessError(result.returncode, quote_cmd_with_shadow)
            except subprocess.CalledProcessError:
                # Fallback to simple text without background
                try:
                    result = subprocess.run(quote_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    if result.returncode != 0:
                        print(f"Warning: Quote overlay failed, using plain image")
                        os.rename(temp_path, output_path)
                except Exception as e:
                    print(f"Warning: Could not add quote: {e}")
                    # If adding quote fails, just use the combined image
                    if temp_path.exists():
                        os.rename(temp_path, output_path)
            
            # Clean up temp files
            if temp_path.exists():
                temp_path.unlink()
            
            # Clean up temporary files
            overlay_file = Path.home() / '.cache' / 'quote-overlay.png'
            if overlay_file.exists():
                overlay_file.unlink()
                
            text_temp_file = Path.home() / '.cache' / 'text-temp.png'
            if text_temp_file.exists():
                text_temp_file.unlink()
                
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
        
        if not wallpapers or len(wallpapers) < 2:
            print(f"ERROR: Insufficient wallpapers found! Got {len(wallpapers)}, need 2")
            return
        
        # Verify the wallpapers are different
        if wallpapers[0] == wallpapers[1]:
            print("WARNING: Selected same wallpaper twice, retrying...")
            wallpapers = self.get_random_wallpapers(len(self.monitors))
            if wallpapers[0] == wallpapers[1]:
                print("ERROR: Still got duplicates, check wallpaper directory")
                return
        
        # For GNOME, we need to use the combined wallpaper method
        print(f"Creating combined wallpaper (3840x1080)...")
        combined = self.create_combined_wallpaper(wallpapers)
        
        if combined and os.path.exists(combined):
            # Verify the combined image was created with correct dimensions
            try:
                result = subprocess.run(
                    ['identify', '-format', '%wx%h', str(combined)],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                if result.returncode == 0:
                    dimensions = result.stdout.strip()
                    print(f"Combined wallpaper dimensions: {dimensions}")
                    
                    # Check if dimensions match expected multi-monitor setup
                    expected_width = sum(int(m['resolution'].split('x')[0]) for m in self.monitors[:2])
                    expected_height = int(self.monitors[0]['resolution'].split('x')[1])
                    expected_dimensions = f"{expected_width}x{expected_height}"
                    
                    if dimensions != expected_dimensions:
                        print(f"ERROR: Wrong dimensions! Expected {expected_dimensions}, got {dimensions}")
                        print("Skipping this wallpaper cycle to prevent stretching")
                        
                        # Clean up the bad combined image
                        if os.path.exists(combined):
                            os.unlink(combined)
                        return  # Skip this cycle
                    
                    # Force GNOME to spanned mode before setting wallpaper
                    subprocess.run([
                        'gsettings', 'set',
                        'org.gnome.desktop.background',
                        'picture-options', 'spanned'
                    ])
                    
                    self.set_gnome_wallpaper(combined)
                    print(f"✓ Set combined wallpaper from:")
                    for i, wallpaper in enumerate(wallpapers[:2]):
                        monitor_name = self.monitors[i]['name'] if i < len(self.monitors) else f"Monitor {i}"
                        print(f"  {monitor_name}: {os.path.basename(wallpaper)}")
                else:
                    print("ERROR: Could not verify image dimensions")
                    return
            except Exception as e:
                print(f"ERROR: Failed to verify image: {e}")
                return
        else:
            print("ERROR: Failed to create combined wallpaper!")
    
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