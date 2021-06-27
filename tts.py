import operator
import os
import sys
from asyncio import tasks
from idlelib.iomenu import errors

import requests
import torch
from flask import Flask, send_from_directory, flash, jsonify, render_template
# from flask import Flask
from werkzeug.utils import redirect
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, Mayur!'

import moviepy.editor as mp
import wave, math, contextlib
import speech_recognition as sr
from moviepy.editor import AudioFileClip

from transformers import T5ForConditionalGeneration, T5Tokenizer, T5Config

# initialize the model architecture and weights
model = T5ForConditionalGeneration.from_pretrained("t5-base")
# initialize the model tokenizer
tokenizer = T5Tokenizer.from_pretrained("t5-base")
device = torch.device('cpu')


def summary(raw):
    #file = askopenfile(mode='r', filetypes=[('Python Files', '*.txt')])
    #article = file.read()
    #file = askopenfile(filetypes=[("python files",'*.mp4')])
    # return content
    file_name = raw
#    l1 = Label(text="Hello, We got your file "+file_name+" Please wait to get Summary of it.", wraplength=500, justify="center", font="comicsansms 13 bold", pady=15)
#    l1.pack()
    #print("Hello, We got your file. Please wait to get Summary of it.")
    audioclip = AudioFileClip(file_name)
    audioclip.write_audiofile("new_converted.wav")

    r = sr.Recognizer()
    audio = sr.AudioFile("new_converted.wav")
    with audio as source:
        audio_file = r.record(source)
    result = r.recognize_google(audio_file)
    # encode the text into tensor of integers using the appropriate tokenizer
    inputs = tokenizer.encode("summarize: " + str(result), return_tensors="pt", truncation=True)
    outputs = model.generate(inputs, max_length=1500, min_length=50, length_penalty=2.0, num_beams=5,
                             early_stopping=True)
    out = tokenizer.decode(outputs[0])
    o = out.split('>',1)
    out1 = o[1].split('<')
    # print(tokenizer.decode(outputs[0]))
    #l = Label(text=out1[0], wraplength= 500,justify="center" ,font="comicsansms 13 bold", pady=15)
    #l.pack(fill=Y)
    return out1[0]
import pyaudio
def talk():
    import speech_recognition as sr
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()
    # Reading Microphone as source
    # listening the speech and store in audio_text variable
    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks")
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            # using google speech recognition
            text = print("Text: " + r.recognize_google(audio_text))
        except:
            print("Sorry, I did not get that")
    return text

def talk2():
    import speech_recognition as sr
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()
    # Reading Microphone as source
    # listening the speech and store in audio_text variable
    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks")
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        #try:
            # using google speech recognition
        text = r.recognize_google(audio_text)
        #except:
        #    print("Sorry, I did not get that")
        inputs = tokenizer.encode("summarize: " + str(text), return_tensors="pt", truncation=True)
        outputs = model.generate(inputs, max_length=500, min_length=100, length_penalty=2.0, num_beams=5,
                                 early_stopping=True)
        out = tokenizer.decode(outputs[0])
        o = out.split('>', 1)
        out2 = o[1].split('<')
        # print(tokenizer.decode(outputs[0]))
        # l = Label(text=out1[0], wraplength= 500,justify="center" ,font="comicsansms 13 bold", pady=15)
        # l.pack(fill=Y)
        return out2[0]
  #  return render_template('result.html', results=talk2)
@app.route('/home1', methods=['Get','POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the user has entered
        try:
            num = request.form['myfile']
            #r = requests.get(num)
            r= num
            #v = request.form['myvoice']
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return render_template('home.html', errors=errors)
        if r:
            results = summary(r)
        #if v:
        #    results = talk2()
    return render_template('result.html',results=results, errors=errors)

@app.route('/home2', methods=['GET','POST'])
def index1():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the user has entered
        try:
            v = request.form['myvoice']
        except:
            errors.append(
                "Unable to get voice. Please make sure it's valid and try again."
            )
            return render_template('home.html', errors=errors)
        if v:
            import speech_recognition as sr
            # Initialize recognizer class (for recognizing the speech)
            r = sr.Recognizer()
            # Reading Microphone as source
            # listening the speech and store in audio_text variable
            with sr.Microphone() as source:
                print("Talk")
                audio_text = r.listen(source)
                print("Time over, thanks")
                # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
                # try:
                # using google speech recognition
                text = r.recognize_google(audio_text)
                # except:
                #    print("Sorry, I did not get that")
                inputs = tokenizer.encode("summarize: " + str(text), return_tensors="pt", truncation=True)
                outputs = model.generate(inputs, max_length=100, min_length=30, length_penalty=2.0, num_beams=5,
                                         early_stopping=True)
                out = tokenizer.decode(outputs[0])
                o = out.split('>', 1)
                out2 = o[1].split('<')
                # print(tokenizer.decode(outputs[0]))
                # l = Label(text=out1[0], wraplength= 500,justify="center" ,font="comicsansms 13 bold", pady=15)
                # l.pack(fill=Y)
                #return out2[0]
                results = out2[0]
    return render_template('result.html',results=results, errors=errors)

if __name__ == '__main__':
    app.run(debug=True)
