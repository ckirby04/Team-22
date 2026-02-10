#!/bin/bash
# Photon Laser Tag - Debian dependency installer
# Run with: sudo bash install.sh

set -e

echo "=== Photon Laser Tag - Dependency Installer ==="
echo ""

# System packages
echo "Installing system packages..."
apt-get update -qq
apt-get install -y python3-pip python3-tk postgresql postgresql-client

# Python packages
echo "Installing Python packages..."
pip3 install psycopg2-binary Pillow pygame

# Check PostgreSQL is running
echo ""
echo "Checking PostgreSQL..."
if systemctl is-active --quiet postgresql; then
    echo "  PostgreSQL is running."
else
    echo "  Starting PostgreSQL..."
    systemctl start postgresql
    systemctl enable postgresql
fi

# Create database and role if they don't exist
echo "Setting up database..."
sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='student'" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE ROLE student WITH LOGIN;"
echo "  Role 'student' exists."

sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='photon'" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE DATABASE photon OWNER student;"
echo "  Database 'photon' exists."

# Create players table if it doesn't exist
sudo -u postgres psql -d photon -c "
CREATE TABLE IF NOT EXISTS players (
    id INT PRIMARY KEY,
    codename VARCHAR(30)
);
GRANT ALL PRIVILEGES ON TABLE players TO student;
"
echo "  Table 'players' exists."

echo ""
echo "=== Installation complete! ==="
echo "Run the game with: python3 main.py"
