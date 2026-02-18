#!/bin/bash
# Installation script for GlueLang on Amazon Linux 2
# This script installs required dependencies and builds GlueLang

set -e

echo "Installing GlueLang on Amazon Linux 2..."
echo ""

# Check if running on Amazon Linux 2
if [ ! -f /etc/os-release ] || ! grep -q "Amazon Linux" /etc/os-release; then
    echo "Warning: This script is designed for Amazon Linux 2"
    echo "Continuing anyway..."
    echo ""
fi

# Install development tools and dependencies
echo "Step 1: Installing build dependencies..."
sudo yum groupinstall -y "Development Tools"
sudo yum install -y gcc-c++ glibc-static libstdc++-static

# Check gcc version
GCC_VERSION=$(gcc --version | head -n1 | awk '{print $3}' | cut -d. -f1)
echo "Detected GCC version: $GCC_VERSION"

# If gcc version is less than 7, we need to install a newer version
if [ "$GCC_VERSION" -lt 7 ]; then
    echo "GCC version $GCC_VERSION may not fully support C++17"
    echo "Installing GCC 7+ from Amazon Linux Extras..."
    sudo amazon-linux-extras install -y gcc-toolset-9
    echo ""
    echo "To use GCC 9, run:"
    echo "  source /opt/rh/gcc-toolset-9/enable"
    echo "  make"
    echo ""
    echo "Or modify src/Makefile to use: CXX = /opt/rh/gcc-toolset-9/root/usr/bin/g++"
    exit 0
fi

# Build GlueLang
echo ""
echo "Step 2: Building GlueLang..."
make clean || true
make

# Install
echo ""
echo "Step 3: Installing GlueLang..."
make install

echo ""
echo "Installation complete!"
echo "Add ~/.glue/bin to your PATH:"
echo "  export PATH=\$PATH:~/.glue/bin"
echo ""
echo "Or add to ~/.bashrc:"
echo "  echo 'export PATH=\$PATH:~/.glue/bin' >> ~/.bashrc"
