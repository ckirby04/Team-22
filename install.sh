#!/bin/bash
# Photon Laser Tag - Debian dependency installer
# Run with: sudo bash install.sh

set -e

echo "=== Photon Laser Tag - Dependency Installer ==="
echo ""

# System packages
echo "Installing system packages..."
apt-get update -qq
apt-get install -y python3-pip python3-tk

# Python packages
echo "Installing Python packages..."
pip3 install psycopg2-binary Pillow pygame

echo ""
echo "=== Installation complete! ==="
echo ""
echo "Required software on the virtual system:"
echo "  - Python 3.8+"
echo "  - python3-tk"
echo "  - PostgreSQL (with 'photon' database and 'student' role pre-configured)"
echo "  - psycopg2-binary (Python)"
echo "  - Pillow (Python)"
echo "  - pygame (Python)"
echo ""
echo "Run the game with: python3 main.py"
