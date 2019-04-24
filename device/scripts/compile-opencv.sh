OPENCV_VERSION=4.1.0

# todo enlarge disk space
# https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/
# https://www.pyimagesearch.com/2017/10/09/optimizing-opencv-on-the-raspberry-pi

sudo apt-get install build-essential cmake unzip pkg-config -y
sudo apt-get install libjpeg-dev libpng-dev libtiff-dev -y
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev -y
sudo apt-get install libxvidcore-dev libx264-dev -y

sudo apt-get install libatlas-base-dev gfortran -y
sudo apt-get install python3-dev -y

wget -O opencv.zip https://github.com/opencv/opencv/archive/$OPENCV_VERSION.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/$OPENCV_VERSION.zip

unzip opencv.zip
unzip opencv_contrib.zip

mv opencv-$OPENCV_VERSION opencv
mv opencv_contrib-$OPENCV_VERSION opencv_contrib

cd opencv
mkdir build
cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF ..

# todo change swap size
#sudo nano /etc/dphys-swapfile
#CONF_SWAPSIZE=2048
#sudo /etc/init.d/dphys-swapfile stop
#sudo /etc/init.d/dphys-swapfile start

make -j4

#todo change swap size back
#sudo nano /etc/dphys-swapfile
#CONF_SWAPSIZE=100
#sudo /etc/init.d/dphys-swapfile stop
#sudo /etc/init.d/dphys-swapfile start