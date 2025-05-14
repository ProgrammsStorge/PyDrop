import base64
import os
path = 'level_create\\'
fileOutput=""
splitSymvol="&*$"
try:os.remove(path+"output")
except:print("No file")
with open(path+"main.py", 'r') as file:
    fileOutput += file.read()
fileOutput += splitSymvol
with open(path+"sound.mp3", 'rb') as file:
    fileC = file.read()
fileOutput += base64.b64encode(fileC).decode('utf-8')
fileOutput += splitSymvol
with open(path+"color.txt", 'r') as file:
    fileOutput += file.read()
fileOutput += splitSymvol
with open(path+"BackGround.png", 'rb') as file:
    fileC = file.read()
fileOutput += base64.b64encode(fileC).decode('utf-8')
with open(path+"output", 'w') as file:
    file.write(fileOutput)
