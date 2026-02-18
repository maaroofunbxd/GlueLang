#!/bin/bash
# Simplified installation script for Amazon Linux 2
# Uses non-static build if static libraries are not available

set -e

echo "Installing GlueLang on Amazon Linux 2 (simplified version)..."
echo ""

# Install basic build tools
echo "Installing build dependencies..."
sudo yum install -y gcc-c++ make

# Build without static linking (more compatible)
echo ""
echo "Building GlueLang (non-static build)..."
make clean || true
make -C src CXXFLAGS="-Wall -O2 -std=c++17" LDFLAGS="-lm"

# Install
echo ""
echo "Installing GlueLang..."
mkdir -p ${HOME}/.glue/bin/
install -m 755 src/glue ${HOME}/.glue/bin/glue
cp src/glue ./

echo ""
echo "Installation complete!"
echo "Add ~/.glue/bin to your PATH:"
echo "  export PATH=\$PATH:~/.glue/bin"
