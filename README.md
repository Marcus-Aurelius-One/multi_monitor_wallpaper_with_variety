# Multi-Monitor Wallpaper Manager with Variety Integration

A sophisticated Python script that displays different wallpapers on each monitor with inspirational quotes, leveraging Variety's excellent wallpaper sources while maintaining complete display control.

## ✨ Features

- **🖼️ Different wallpapers per monitor** - Each monitor displays unique, high-quality images
- **💬 Dynamic inspirational quotes** - Beautiful quote overlays with rounded corners and smart text wrapping
- **🔄 Intelligent rotation** - Avoids recent repeats and automatically requests fresh downloads
- **🌐 Variety integration** - Leverages Variety's diverse sources (NASA APOD, Bing, National Geographic, Unsplash, etc.)
- **🎨 Perfect formatting** - Dynamic quote box sizing with proper transparency and positioning
- **⚡ Auto-cycling** - Configurable interval (default 60 seconds)
- **🚀 Auto-start on boot** - Runs reliably as a systemd user service
- **🛡️ Conflict-free** - Completely isolates Variety's display control to prevent interference

## 📋 Requirements

- **Python 3** - Core runtime
- **ImageMagick** - Image processing (`convert` command)  
- **Variety** - Wallpaper source provider
- **GNOME** - Desktop environment (Ubuntu, Fedora, etc.)
- **Dual monitors** - Currently optimized for two 1920x1080 displays

## 🚀 Installation

### Quick Install (Recommended)

```bash
git clone https://github.com/Marcus-Aurelius-One/multi_monitor_wallpaper_with_variety.git
cd multi_monitor_wallpaper_with_variety
chmod +x install.sh
./install.sh
```

The installer will:
- ✅ Install required dependencies (ImageMagick)
- ✅ Set up the wallpaper management service  
- ✅ Configure Variety to work as a download-only service
- ✅ Enable auto-start on boot
- ✅ Start the service immediately

## 🎨 What You Get

**Visual Experience:**
- **Left Monitor**: Beautiful wallpaper (NASA space images, nature photography, etc.)
- **Right Monitor**: Different wallpaper + inspirational quote in bottom-right corner
- **Quotes**: Elegant rounded boxes with perfect text wrapping and transparency
- **Rotation**: Fresh content every 60 seconds with intelligent variety

**Content Sources** (via Variety):
- 🚀 **NASA APOD** - Stunning space and astronomy imagery
- 🌍 **Google Earth View** - Breathtaking satellite imagery  
- 📰 **Bing Photo of the Day** - Microsoft's curated daily photos
- 📸 **National Geographic** - Professional nature and travel photography
- 🎨 **Unsplash** - High-resolution artistic photography
- 📷 **Flickr** - Community-sourced quality images

**Quote Sources:**
- 🌐 **Online APIs** - ZenQuotes, Quotable (thousands of quotes)
- 📚 **Local fallback** - 25+ built-in inspirational quotes
- 🎯 **Smart selection** - Avoids repetition, handles long quotes gracefully

### Manual Installation

<details>
<summary>Click to expand manual installation steps</summary>

1. **Install dependencies:**
```bash
sudo apt install imagemagick variety
```

2. **Clone and setup:**
```bash
git clone https://github.com/Marcus-Aurelius-One/multi_monitor_wallpaper_with_variety.git
cd multi_monitor_wallpaper_with_variety
cp multi-monitor-wallpaper.py ~/
chmod +x ~/multi-monitor-wallpaper.py
```

3. **Install systemd service:**
```bash
mkdir -p ~/.config/systemd/user
cp multi-monitor-wallpaper.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable multi-monitor-wallpaper.service
systemctl --user start multi-monitor-wallpaper.service
```

4. **Configure Variety (important):**
Edit `~/.config/variety/variety.conf` and set:
```
change_enabled = False
change_on_start = False
```

</details>

## Configuration

### Variety Setup

1. Keep Variety installed for downloading wallpapers
2. Disable Variety's wallpaper changing:
   - Edit `~/.config/variety/variety.conf`
   - Set `change_enabled = False`
   - Set `change_on_start = False`

### Monitor Configuration

The script automatically detects your monitors using `xrandr`. It will:
- Use the leftmost monitor for the first wallpaper
- Use the rightmost monitor for the second wallpaper
- Display quotes on the rightmost monitor

### Customization

Edit `multi-monitor-wallpaper.py` to customize:
- **Change interval**: Modify `interval=60` in the `run()` method
- **Quote font**: Change `'Ubuntu-Bold'` and `'30'` in the quote rendering section
- **Quote position**: Adjust the positioning calculations in `create_combined_wallpaper()`
- **Wallpaper directory**: Change `self.wallpaper_dir` in `__init__()`

## Usage

### Start the service
```bash
systemctl --user start multi-monitor-wallpaper.service
```

### Stop the service
```bash
systemctl --user stop multi-monitor-wallpaper.service
```

### Check status
```bash
systemctl --user status multi-monitor-wallpaper.service
```

### View logs
```bash
journalctl --user -u multi-monitor-wallpaper.service -f
```

### Run manually (for testing)
```bash
python3 ~/multi-monitor-wallpaper.py
```
Press Ctrl+C to stop

## Troubleshooting

### Wallpapers not changing
- Check that the service is running: `systemctl --user status multi-monitor-wallpaper.service`
- Ensure GNOME is set to 'spanned' mode: `gsettings get org.gnome.desktop.background picture-options`
- Check logs for errors: `journalctl --user -u multi-monitor-wallpaper.service -n 50`

### Quotes not appearing
- Ensure ImageMagick is installed: `which convert`
- Check that Ubuntu-Bold font is available: `fc-list | grep -i ubuntu`

### Service not starting on boot
- Enable the service: `systemctl --user enable multi-monitor-wallpaper.service`
- Check service file permissions: `ls -la ~/.config/systemd/user/`

## File Structure

```
Wall_Paper_Multi_Monitor_Variety/
├── README.md                          # This file
├── multi-monitor-wallpaper.py         # Main Python script
├── multi-monitor-wallpaper.service    # Systemd service file
├── install.sh                         # Installation script
└── uninstall.sh                      # Uninstallation script
```

## License

Free to use and modify.

## Credits

- Uses wallpapers downloaded by [Variety](https://github.com/varietywalls/variety)
- Quotes from [Quotable API](https://github.com/lukePeavey/quotable)