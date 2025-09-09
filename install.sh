#!/bin/bash

# Multi-Monitor Wallpaper Manager - Installation Script

echo "================================================"
echo "Multi-Monitor Wallpaper Manager - Installer"
echo "================================================"

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo "Please do not run this script as root (no sudo)"
   exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install dependencies
echo ""
echo "Step 1: Installing dependencies..."
echo "--------------------------------"

PACKAGES_NEEDED=""

if ! command_exists convert; then
    PACKAGES_NEEDED="$PACKAGES_NEEDED imagemagick"
fi

if ! command_exists xwallpaper; then
    PACKAGES_NEEDED="$PACKAGES_NEEDED xwallpaper"
fi

if [ -n "$PACKAGES_NEEDED" ]; then
    echo "The following packages need to be installed: $PACKAGES_NEEDED"
    echo "Please run: sudo apt install$PACKAGES_NEEDED"
    read -p "Would you like to install them now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt update
        sudo apt install -y $PACKAGES_NEEDED
    else
        echo "Please install the required packages manually and run this script again."
        exit 1
    fi
else
    echo "All dependencies are already installed!"
fi

# Check for Variety
echo ""
echo "Step 2: Checking Variety installation..."
echo "---------------------------------------"
if ! command_exists variety; then
    echo "WARNING: Variety is not installed."
    echo "This script uses wallpapers downloaded by Variety."
    echo "Install Variety with: sudo apt install variety"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "Variety is installed."
    
    # Disable Variety's wallpaper changing
    if [ -f ~/.config/variety/variety.conf ]; then
        echo "Disabling Variety's wallpaper changing..."
        sed -i 's/change_enabled = True/change_enabled = False/' ~/.config/variety/variety.conf
        sed -i 's/change_on_start = True/change_on_start = False/' ~/.config/variety/variety.conf
        
        # Restart Variety if it's running
        if pgrep -x "variety" > /dev/null; then
            killall variety
            sleep 2
            variety &>/dev/null &
            disown
        fi
    fi
fi

# Copy files
echo ""
echo "Step 3: Installing script files..."
echo "---------------------------------"

# Copy main script
echo "Installing main script..."
cp multi-monitor-wallpaper.py ~/multi-monitor-wallpaper.py
chmod +x ~/multi-monitor-wallpaper.py

# Create systemd user directory if it doesn't exist
mkdir -p ~/.config/systemd/user

# Copy and update service file
echo "Installing systemd service..."
cat > ~/.config/systemd/user/multi-monitor-wallpaper.service << EOF
[Unit]
Description=Multi-Monitor Wallpaper Cycler
After=graphical-session.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $HOME/multi-monitor-wallpaper.py
Restart=always
RestartSec=10
Environment="DISPLAY=:0"
Environment="XAUTHORITY=$HOME/.Xauthority"

[Install]
WantedBy=default.target
EOF

# Enable and start service
echo ""
echo "Step 4: Setting up systemd service..."
echo "------------------------------------"
systemctl --user daemon-reload
systemctl --user enable multi-monitor-wallpaper.service

echo ""
read -p "Would you like to start the service now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Stop any existing instance
    systemctl --user stop multi-monitor-wallpaper.service 2>/dev/null
    pkill -f multi-monitor-wallpaper.py 2>/dev/null
    
    # Start the service
    systemctl --user start multi-monitor-wallpaper.service
    sleep 2
    
    # Check status
    if systemctl --user is-active --quiet multi-monitor-wallpaper.service; then
        echo ""
        echo "✓ Service started successfully!"
        echo ""
        echo "The wallpaper manager is now running."
        echo "Wallpapers will change every 60 seconds."
    else
        echo ""
        echo "⚠ Service failed to start. Check logs with:"
        echo "journalctl --user -u multi-monitor-wallpaper.service -n 50"
    fi
else
    echo ""
    echo "Service installed but not started."
    echo "To start manually, run:"
    echo "systemctl --user start multi-monitor-wallpaper.service"
fi

echo ""
echo "================================================"
echo "Installation complete!"
echo "================================================"
echo ""
echo "Useful commands:"
echo "  Start service:   systemctl --user start multi-monitor-wallpaper.service"
echo "  Stop service:    systemctl --user stop multi-monitor-wallpaper.service"
echo "  Check status:    systemctl --user status multi-monitor-wallpaper.service"
echo "  View logs:       journalctl --user -u multi-monitor-wallpaper.service -f"
echo "  Manual run:      python3 ~/multi-monitor-wallpaper.py"
echo ""