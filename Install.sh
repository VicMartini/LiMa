sudo apt-get install python-pip
clear
pip install --allow-external pil qrcode
clear
add-apt-repository ppa:qr-tools-developers/qr-tools-stable
clear
apt-get update
clear
sudo apt-get install python-qrtools
clear
echo python ./main/lima.py >> LiMa.sh
chmod +777 LiMa.sh



