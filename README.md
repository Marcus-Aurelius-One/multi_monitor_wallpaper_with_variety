# Multi-Monitor Wallpaper Manager with Variety Integration

A Python script that displays different wallpapers on each monitor with inspirational quotes, using wallpapers downloaded by Variety.

## Features

- **Different wallpapers on each monitor** - Each monitor gets its own unique wallpaper
- **Inspirational quotes** - Displays quotes in the bottom-right corner of the right monitor
- **Automatic cycling** - Changes wallpapers every 60 seconds
- **Variety integration** - Uses wallpapers downloaded by Variety
- **GNOME compatible** - Works with GNOME desktop environment
- **Auto-start on boot** - Runs as a systemd service

## Requirements

- Python 3
- ImageMagick (`convert` command)
- xwallpaper (optional, for non-GNOME environments)
- Variety (for downloading wallpapers)
- GNOME desktop environment (or compatible)

## Installation

### Quick Install

Run the install script:
```bash
chmod +x install.sh
./install.sh
```

### Manual Installation

1. Install dependencies:
```bash
sudo apt install imagemagick xwallpaper
```

2. Copy the Python script to your home directory:
```bash
cp multi-monitor-wallpaper.py ~/
chmod +x ~/multi-monitor-wallpaper.py
```

3. Install the systemd service:
```bash
mkdir -p ~/.config/systemd/user
cp multi-monitor-wallpaper.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable multi-monitor-wallpaper.service
systemctl --user start multi-monitor-wallpaper.service
```

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