from flask import Flask, render_template
from flask import request
import os
import speech_recognition as sr

r = sr.Recognizer()

app = Flask(__name__)
IMAGE_FOLDER = os.path.join('static', 'photos')
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

map = [{"image": "imageHi.jpg", "key": "HI"}, {"image": "imageHello.webp", "key": "HELLO"}]
defaultPath = "https://www.seekpng.com/png/detail/9-96714_question-mark-png-question-mark-black-png.png"


@app.route("/", methods=['POST'])
def post():
    try:
        btn_reco = request.form['text_reco']
    except:
        btn_reco = False
    try:
        try_again = request.form['try']
    except:
        try_again = False
    if try_again:
        return render_template("form.html", )
    if btn_reco:
        with sr.Microphone() as source:
            # read the audio data from the default microphone
            audio_data = r.record(source, duration=5)
            print("Recognizing...")
            # convert speech to text
            text = r.recognize_google(audio_data)
            return render_template("form.html", text_area=text)
    text = request.form['text']
    processed_text = text.strip().upper().split()
    imageUrls = []

    for userin in processed_text:
        values = next((item for item in map if item["key"] == userin), False)
        if not values == False:
            imageUrls.append(os.path.join(app.config['UPLOAD_FOLDER'], values["image"]))
        else:
            imageUrls.append(defaultPath)

    return render_template("index.html",
                           imagepath=imageUrls, len=len(imageUrls), originalText=text)


@app.route("/", methods=["GET"])
def index():
    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)
