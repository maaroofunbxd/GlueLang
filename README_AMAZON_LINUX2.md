# Installing GlueLang on Amazon Linux 2

Amazon Linux 2 may have issues with static linking or older GCC versions. Here are several solutions:

## Option 1: Use the Installation Script (Recommended)

Run the simplified installation script that builds without static linking:

```bash
chmod +x install_amazon_linux2_simple.sh
./install_amazon_linux2_simple.sh
```

## Option 2: Build Without Static Linking

If you encounter issues with static linking, build without it:

```bash
# Install dependencies
sudo yum install -y gcc-c++ make

# Build without static linking
make clean
make -C src STATIC=0

# Install
make install
```

## Option 3: Use Alternative Makefile

Use the Amazon Linux 2-specific Makefile:

```bash
sudo yum install -y gcc-c++ make
cd src
make -f Makefile.amazon_linux2
make -f Makefile.amazon_linux2 install
cd ..
```

## Option 4: Install GCC 9+ (If GCC version < 7)

If your GCC version is too old for C++17 support:

```bash
# Install GCC 9 via Amazon Linux Extras
sudo amazon-linux-extras install -y gcc-toolset-9

# Enable GCC 9
source /opt/rh/gcc-toolset-9/enable

# Build with GCC 9
make clean
make CXX=/opt/rh/gcc-toolset-9/root/usr/bin/g++ STATIC=0

# Install
make install
```

## Common Issues and Solutions

### Issue: "g++: command not found"
**Solution:**
```bash
sudo yum install -y gcc-c++
```

### Issue: "error: unrecognized command line option '-std=c++17'"
**Solution:** Your GCC is too old. Use Option 4 to install GCC 9+.

### Issue: "cannot find -lstdc++" or static linking errors
**Solution:** Build without static linking using `STATIC=0`:
```bash
make -C src STATIC=0
```

### Issue: Missing static libraries
**Solution:** Install static libraries (optional, only if you need static builds):
```bash
sudo yum install -y glibc-static libstdc++-static
```

## Verify Installation

After installation, add GlueLang to your PATH:

```bash
export PATH=$PATH:~/.glue/bin
```

Or add to `~/.bashrc`:
```bash
echo 'export PATH=$PATH:~/.glue/bin' >> ~/.bashrc
source ~/.bashrc
```

Test the installation:
```bash
glue --version
```
