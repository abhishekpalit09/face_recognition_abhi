from flask import Flask, request
import json
import face_recognition
from urllib.request import urlopen
# ...

app = Flask(__name__)

@app.route('/hi', methods=['POST'])
def hello():
    print("Hello")

@app.route('/post_json', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'


@app.route('/post_filename', methods=['POST'])
def photo_match():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        # json = request.json
        req_body = request.get_json()
        filepath1 = req_body.get('filepath1')
        filepath2 = req_body.get('filepath2')

        # filepath1 = "Abhi_ID.jpeg"
        # filepath2 = "Abhi_Selfie.jpeg"
        
        # filepath1 = "https://imagetest12.blob.core.windows.net/angular-file/Abhi_ID.jpg"
        # filepath2 = "https://imagetest12.blob.core.windows.net/angular-file/Abhi_Selfie.jpeg"

        # filepath1 =  "https://facecont.blob.core.windows.net/facedata/Aish1_ID.jpeg",
        # filepath2 =  "https://facecont.blob.core.windows.net/facedata/Aish1_Selfie.jpeg"

        f1 = urlopen(filepath1)
        f2 = urlopen(filepath2)

        try:

   
            ID_image = face_recognition.load_image_file(f1)
            # unknown_image = face_recognition.load_image_file("For_FB2.jpg")
            Selfie_image = face_recognition.load_image_file(f2)

            ID_image_encoding = face_recognition.face_encodings(ID_image)[0]
            Selfie_image_encoding = face_recognition.face_encodings(Selfie_image)[0]

            results = face_recognition.compare_faces([Selfie_image_encoding], ID_image_encoding)

            # print(results)

            if results == [True]:
                return json.dumps('Matched')
            else:
                return json.dumps('Not Matched')

        except:
            print("Not Matched")


        # if results == [True]:
        #     return json.dumps({
        #     "file1" : filepath1,
        #     "file2" : filepath2
        # })
        # else:
        #     return 'Content-Type not supported!'



app.run(host="0.0.0.0",port=80,debug=True,use_reloader=True)
