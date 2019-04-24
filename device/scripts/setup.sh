# config ###############################################################################
PYTHON_VERSION=3.7.3

# general ##############################################################################
sudo apt-get update -y
sudo apt-get upgrade -y

# python ###############################################################################
if [ ! -d "/usr/bin/python$PYTHON_VERSION" ]; then
    sudo apt-get purge python2.7 -y
    sudo apt-get purge python3.5 -y
    sudo rm -Rf /usr/bin/py*
    sudo rm -Rf /usr/local/bin/pip*

    sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y
    wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz
    tar xf Python-$PYTHON_VERSION.tar.xz
    cd Python-$PYTHON_VERSION
    ./configure
    make -j 4
    sudo make altinstall

    # cleanup
    cd ..
    sudo rm -r Python-$PYTHON_VERSION
    rm Python-$PYTHON_VERSION.tar.xz
    sudo apt-get --purge remove build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y
    sudo apt-get autoremove -y
    sudo apt-get clean

    sudo update-alternatives --install /usr/local/bin/python python /usr/local/bin/python3.7 1
    sudo update-alternatives --install /usr/local/bin/python3 python3 /usr/local/bin/python3.7 1
    sudo update-alternatives --install /usr/local/bin/pip pip /usr/local/bin/pip3.7 1
    sudo update-alternatives --install /usr/local/bin/pip3 pip3 /usr/local/bin/pip3.7 1
fi

# git ##################################################################################
if [ ! -d "/usr/bin/git" ]; then
    sudo apt-get install git -y
    sudo apt-get --fix-broken install
fi

# grovepi ##############################################################################
if [ ! -d "grovepi" ]; then
    git clone https://github.com/DexterInd/GrovePi grovepi
    sudo chmod +x ./grovepi/Script/update_grovepi.sh    
    ./grovepi/Script/update_grovepi.sh --user-local --bypass-gui-installation
    sudo shutdown -r now

    sudo chmod +x ./grovepi/Script/firmware_update.sh
    ./grovepi/Script/firmware_update.sh
fi

# opencv ###############################################################################
# todo: if

sudo make install
sudo ldconfig

# video stuff ##########################################################################
sudo apt-get install libav-tools -y

# kicker activity stuff ################################################################

#todo
#pip install -r /mnt/device/scripts/requirements.txt --user



# test #################################################################################
#maybe check if everythin is installed