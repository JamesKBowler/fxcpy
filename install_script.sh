#!/bin/bash
# 
# File:   install_script.sh
#
# The MIT License (MIT)
#
# Copyright (c) 2018 James K Bowler, Data Centauri Ltd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
#
apt update
apt -y install python3-pip
apt -y install build-essential
apt -y install python3.6-dev
apt -y install libtool m4 automake autogen make g++
apt -y install libcurl4-openssl-dev
apt -y install zlib1g-dev
su "$SUDO_USER" << 'EOF'
mkdir .boost_install
EOF
#      ___ __                   ___        _______          ___
#     / (_) /_  __  ___   __   <  /       <  / __ \        <  /
#    / / / __ \/ / / / | / /   / /        / / /_/ /        / / 
#   / / / /_/ / /_/ /| |/ /   / /  _     / /\__, /  _     / /  
#  /_/_/_.___/\__,_/ |___/   /_/  (_)   /_//____/  (_)   /_/   
#                                                              
su "$SUDO_USER" << 'EOF'
cd .boost_install
wget https://github.com/libuv/libuv/archive/v1.19.1/libuv-1.19.1.tar.gz
tar -xvzf libuv-1.19.1.tar.gz > /dev/null
cd libuv-1.19.1
sh autogen.sh  &&
./configure --prefix=/usr/local \
            --disable-static &&
make -s
EOF
cd .boost_install/libuv-1.19.1 || exit
make install -j2
#      ___ __                    __    _               _____         _____         ___ 
#     / (_) /_  ____ ___________/ /_  (_)   _____     |__  /        |__  /        |__ \
#    / / / __ \/ __ `/ ___/ ___/ __ \/ / | / / _ \     /_ <          /_ <         __/ /
#   / / / /_/ / /_/ / /  / /__/ / / / /| |/ /  __/   ___/ /  _     ___/ /  _     / __/ 
#  /_/_/_.___/\__,_/_/   \___/_/ /_/_/ |___/\___/   /____/  (_)   /____/  (_)   /____/ 
#                     
cd ..                           
su "$SUDO_USER" << 'EOF'
wget http://www.libarchive.org/downloads/libarchive-3.3.2.tar.gz
tar -xvzf libarchive-3.3.2.tar.gz > /dev/null
cd libarchive-3.3.2
./configure --prefix=/usr/local \
	    --disable-static &&
make -s
EOF
cd libarchive-3.3.2 || exit
make install -j2
#     ________  ___      __           _____         ____          _____
#    / ____/  |/  /___ _/ /_____     |__  /        / __ \        / ___/
#   / /   / /|_/ / __ `/ //_/ _ \     /_ <        / /_/ /       / __ \ 
#  / /___/ /  / / /_/ / ,< /  __/   ___/ /  _     \__, /  _    / /_/ / 
#  \____/_/  /_/\__,_/_/|_|\___/   /____/  (_)   /____/  (_)   \____/  
#
cd ..                                                                 
su "$SUDO_USER" << 'EOF'
wget https://cmake.org/files/v3.9/cmake-3.9.6.tar.gz
tar -xvzf cmake-3.9.6.tar.gz > /dev/null
cd cmake-3.9.6
sed -i '/"lib64"/s/64//' Modules/GNUInstallDirs.cmake &&
./bootstrap --prefix=/usr/local            \
	    --system-libs                  \
	    --mandir=/usr/local/share/man  \
	    --no-system-jsoncpp            \
	    --no-system-librhash           \
	    --docdir=/usr/local/share/doc/cmake-3.9.6 &&
make
EOF
cd cmake-3.9.6 || exit
make install -j2
#      ____                   __     ___        _____ ______        ___
#     / __ )____  ____  _____/ /_   <  /       / ___// ____/       <  /
#    / __  / __ \/ __ \/ ___/ __/   / /       / __ \/___ \         / / 
#   / /_/ / /_/ / /_/ (__  ) /_    / /  _    / /_/ /___/ /  _     / /  
#  /_____/\____/\____/____/\__/   /_/  (_)   \____/_____/  (_)   /_/   
#
cd ..                                                                    
su "$SUDO_USER" << 'EOF'
wget https://dl.bintray.com/boostorg/release/1.65.1/source/boost_1_65_1.tar.gz
tar -xvzf boost_1_65_1.tar.gz > /dev/null
cd boost_1_65_1
sed -e '/using python/ s@;@: /usr/include/python${PYTHON_VERSION/3*/${PYTHON_VERSION}m} ;@' \
    -i bootstrap.sh
./bootstrap.sh --prefix=/usr/local            \
        --with-python=/usr/bin/python3        \
        --with-python-version=3.6             \
        --with-python-root=/usr/lib/python3.6 \
        --with-libraries=python
echo "using python : 3.6 : /usr/bin/python3.6 : /usr/include/python3.6m : /usr/lib ;" >> project-config.jam
./b2 stage threading=multi link=shared -j2 -d0
EOF
cd boost_1_65_1 || exit
./b2 install threading=multi link=shared -j2 -d0

# Install FXCPY
cd ../..
# Clean install files
rm -rf .boost_install
P=$PWD
echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${P}/cpp/lib" >> /etc/environment 
su "$SUDO_USER" << 'EOF'
# Compile Forexconnect API cpp code and install fxcpy
cd cpp && mkdir build && cd build
cmake ..
EOF
cd cpp/build || exit
make install -j2
cd ../..
pip3 install . --no-cache-dir
ldconfig
exit 0
