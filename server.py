import socket     
import pickle   
import cv2     

sock = socket.socket()       
port = 12343               
sock.bind(('', port)) 
sock.listen(5)     
print ("socket is listening")  

cap=cv2.VideoCapture(0) 


c, addr = sock.accept()  
print ('Got connection from', addr )   
 
while True: 
    ret,frame=cap.read()

    image = cv2.resize(frame, (512, 512)) 
    try:
        c.send(pickle.dumps({'img': frame, 'info': {'speed': 3, 'angle': 200}})) 
    except:
        break

c.close()