
import torch
import pickle

import speech_recognition as sr
from moviepy.editor import AudioFileClip

from transformers import T5ForConditionalGeneration, T5Tokenizer

# initialize the model architecture and weights
model = T5ForConditionalGeneration.from_pretrained("t5-base")
model.save_pretrained('./t5-ForConditionalGeneration-test/')
# initialize the model tokenizer
tokenizer = T5Tokenizer.from_pretrained("t5-base")
device = torch.device('cpu')
tokenizer.save_pretrained('tokanizer.hdf5')

tokenizer2 = T5Tokenizer.from_pretrained('./t5-tokenizer-test/')
model3=T5ForConditionalGeneration.from_pretrained('./t5-ForConditionalGeneration-test/')
def summary(raw):
    file_name = raw

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
    return out1[0]

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
        text = r.recognize_google(audio_text)

        inputs = tokenizer.encode("summarize: " + str(text), return_tensors="pt", truncation=True)
        outputs = model.generate(inputs, max_length=500, min_length=100, length_penalty=2.0, num_beams=5,
                                 early_stopping=True)
        out = tokenizer.decode(outputs[0])
        o = out.split('>', 1)
        out2 = o[1].split('<')
        return out2[0]


#d=summary()
# Save the trained model as a pickle string.
#filename='pickle_model.pkl'
#saved_model = pickle.dumps(model,open('d.pkl','wb'))
# load the model from disk
#loaded_model = pickle.load(open(saved_model, 'rb'))
