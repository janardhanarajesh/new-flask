from flask import Flask,render_template,request
import cv2
from pymongo import MongoClient
import gridfs
client=MongoClient("mongodb+srv://janardhanarajesh2:XG2poe4SBMMuhRmB@Cluster0.yoqznfa.mongodb.net/cluster0?retryWrites=true&w=majority&appName=Cluster0")
db=client['Cluster0']
fs=gridfs.GridFS(db)
app=Flask(__name__)
@app.route("/")
def home():
    cap=cv2.VideoCapture(0)
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    cv2.imwrite("user.jpg",frame)
    cv2.waitKey(0)
    cap.release()
    with open("user.jpg","rb") as file:
        file_id=fs.put(file,filename="user.jpg")
        print("file uploadde to data base successfully")
    return render_template("index.html")
@app.route("/get")
def get():
    file_data = fs.find_one({"filename": "user.jpg"})
    if file_data:
        with open("downloaded_user.jpg", "wb") as f:
            f.write(file_data.read())
        print("File downloaded successfully")
    else:
        print("File not found")
    return "sucess"
if __name__=="__main__":
    app.run(debug=True)
