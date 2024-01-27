sudo apt-get update -y
sudo apt-get install python3-pip -y
pip3 install -r requirements.txt
pip install --upgrade Flask
pip install --upgrade Werkzeug
pip install flask[async]
python3 run.py

#sudo lsof -i :3000
 
