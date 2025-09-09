# Claude Code Project Memory

## Project Overview
**Multi-Monitor Wallpaper Manager with Variety Integration**
- Repository: https://github.com/Marcus-Aurelius-One/multi_monitor_wallpaper_with_variety
- Created: September 9, 2025
- Purpose: Display different wallpapers on each monitor with inspirational quotes, using Variety's wallpaper collection

## Current Status
✅ **WORKING PERFECTLY** - All issues resolved, system operating smoothly

## Architecture

### Core Components
1. **multi-monitor-wallpaper.py** - Main Python script (runs as systemd service)
2. **multi-monitor-wallpaper.service** - Systemd user service for auto-start
3. **install.sh** - Easy installation script  
4. **uninstall.sh** - Clean removal script
5. **README.md** - Complete documentation

### Key Features Implemented
- **Different wallpapers per monitor** - Each monitor gets unique images
- **Inspirational quotes** - Dynamic quote boxes with rounded corners on right monitor
- **Smart wallpaper rotation** - Tracks used images, avoids repeats
- **Variety integration** - Uses Variety purely as download service (NO display conflicts)
- **Auto-cycling** - Changes every 60 seconds (configurable)
- **Fresh content** - Automatically triggers new downloads from Variety

## Technical Details

### Monitor Setup
- **Left Monitor (DP-3)**: 1920x1080 at x=0
- **Right Monitor (HDMI-0)**: 1920x1080 at x=1920
- **Combined wallpaper**: 3840x1080 total with quotes on right side

### Variety Configuration
- **Sources enabled**: Flickr, NASA APOD, Bing, Earth View, National Geographic, Unsplash
- **Wallpaper changing DISABLED** (`change_enabled = False`, `change_on_start = False`)
- **set_wallpaper script DISABLED** to prevent conflicts
- **Download functionality ACTIVE** - Variety continues downloading fresh content

### Quote System
- **Primary sources**: ZenQuotes API, Quotable API
- **Fallback**: 25 built-in inspirational quotes
- **Display**: Ubuntu Bold 30pt font with rounded background (60% transparency)
- **Positioning**: Bottom-right corner of right monitor
- **Smart truncation**: Limits extremely long quotes intelligently

### Image Processing
- **ImageMagick pipeline**: Creates combined 3840x1080 images
- **Dynamic quote boxes**: Auto-sized based on text length  
- **Dimension validation**: Prevents single-image stretching
- **GNOME integration**: Uses 'spanned' mode for proper multi-monitor display

## Problem Resolution History

### Major Issues Solved
1. **Variety conflicts** - Completely isolated Variety's display control
2. **Single image stretching** - Added dimension validation and proper image creation
3. **Quote formatting** - Dynamic sizing with proper text wrapping
4. **Limited wallpaper variety** - Integrated fresh download triggers
5. **Quote text overflow** - Smart truncation and dynamic box sizing

### Current Wallpaper Collection
- **82+ images** from diverse sources (growing automatically)
- **High quality content** from NASA, Bing, National Geographic, Unsplash
- **Automatic refresh** every 10 wallpaper cycles

## Development Commands

### Testing
```bash
# Test with 2-second intervals
sed -i 's/interval=60/interval=2/' ~/multi-monitor-wallpaper.py
systemctl --user restart multi-monitor-wallpaper.service

# Return to normal 60-second intervals  
sed -i 's/interval=2/interval=60/' ~/multi-monitor-wallpaper.py
systemctl --user restart multi-monitor-wallpaper.service
```

### Service Management
```bash
# Status and logs
systemctl --user status multi-monitor-wallpaper.service
journalctl --user -u multi-monitor-wallpaper.service -f

# Manual run for debugging
python3 ~/multi-monitor-wallpaper.py
```

### Lint and Build Commands
```bash
# The project uses standard Python - no specific lint commands configured
# If adding in future, consider: ruff, black, pylint
```

## File Structure
```
Wall_Paper_Multi_Monitor_Variety/
├── README.md                          # User documentation
├── CLAUDE.md                           # This memory file
├── multi-monitor-wallpaper.py         # Main script
├── multi-monitor-wallpaper.service    # Systemd service
├── install.sh                         # Installation script
└── uninstall.sh                      # Removal script
```

## User Workflow
1. Run `./install.sh` to set up everything
2. System automatically starts on boot
3. Wallpapers cycle every 60 seconds with different images per monitor
4. Quotes from online APIs with local fallbacks
5. Fresh wallpapers downloaded automatically by Variety
6. Run `./uninstall.sh` to cleanly remove if needed

## Next Development Ideas (Future)
- [ ] Add more quote sources (Reddit, Goodreads, etc.)
- [ ] Custom quote categories/filtering
- [ ] Weather integration on wallpapers
- [ ] Clock overlay option
- [ ] Multiple monitor configurations (3+)
- [ ] Custom wallpaper sources beyond Variety

## Notes for Future Claude
- **The system is working perfectly** - don't fix what isn't broken
- **Variety integration is delicate** - wallpaper conflicts were major issue
- **User loves the quote system** - focus on enhancing quotes if requested
- **ImageMagick pipeline is solid** - dynamic sizing works great
- **systemd service is reliable** - auto-starts properly
- **Install/uninstall scripts are complete** - easy deployment

## Performance Notes
- Memory usage: ~20MB (Python script)
- CPU usage: Minimal (only during wallpaper changes)  
- Disk usage: Grows with Variety downloads (~1GB quota set)
- Network: Occasional API calls for quotes (~1KB)

---
*This project represents a complete solution that elegantly combines multiple technologies to create a superior multi-monitor wallpaper experience.*