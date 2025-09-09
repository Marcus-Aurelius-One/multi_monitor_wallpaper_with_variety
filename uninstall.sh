#!/bin/bash

# Multi-Monitor Wallpaper Manager - Uninstallation Script

echo "================================================"
echo "Multi-Monitor Wallpaper Manager - Uninstaller"
echo "================================================"
echo ""

read -p "Are you sure you want to uninstall the Multi-Monitor Wallpaper Manager? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

echo ""
echo "Step 1: Stopping and disabling service..."
echo "----------------------------------------"

# Stop the service
systemctl --user stop multi-monitor-wallpaper.service 2>/dev/null
echo "Service stopped."

# Disable the service
systemctl --user disable multi-monitor-wallpaper.service 2>/dev/null
echo "Service disabled."

# Kill any running instances
pkill -f multi-monitor-wallpaper.py 2>/dev/null

echo ""
echo "Step 2: Removing files..."
echo "------------------------"

# Remove service file
if [ -f ~/.config/systemd/user/multi-monitor-wallpaper.service ]; then
    rm ~/.config/systemd/user/multi-monitor-wallpaper.service
    echo "Removed systemd service file."
fi

# Remove main script
if [ -f ~/multi-monitor-wallpaper.py ]; then
    rm ~/multi-monitor-wallpaper.py
    echo "Removed main script."
fi

# Remove cache files
if [ -f ~/.cache/multi-monitor-wallpaper.jpg ]; then
    rm ~/.cache/multi-monitor-wallpaper.jpg
    echo "Removed cached wallpaper."
fi

if [ -f ~/.cache/temp-wallpaper.jpg ]; then
    rm ~/.cache/temp-wallpaper.jpg
    echo "Removed temporary wallpaper."
fi

# Reload systemd
systemctl --user daemon-reload

echo ""
echo "Step 3: Re-enabling Variety (if installed)..."
echo "--------------------------------------------"

# Re-enable Variety if it exists
if [ -f ~/.config/variety/variety.conf ]; then
    sed -i 's/change_enabled = False/change_enabled = True/' ~/.config/variety/variety.conf
    sed -i 's/change_on_start = False/change_on_start = True/' ~/.config/variety/variety.conf
    echo "Re-enabled Variety wallpaper changing."
    
    # Restart Variety if installed
    if command -v variety &> /dev/null; then
        if pgrep -x "variety" > /dev/null; then
            killall variety
            sleep 2
        fi
        variety &>/dev/null &
        disown
        echo "Restarted Variety."
    fi
else
    echo "Variety configuration not found, skipping."
fi

echo ""
echo "================================================"
echo "Uninstallation complete!"
echo "================================================"
echo ""
echo "The Multi-Monitor Wallpaper Manager has been removed."
echo "Your wallpaper settings have been restored to use Variety."
echo ""
echo "Note: The project files in this directory have not been removed."
echo "You can safely delete this directory if you no longer need it."
echo ""