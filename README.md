# test_demo
Speech to Summary Converter is a web app that takes the input from the user in the form of video as well as audio, then by using NLP and machine learning techniques it converted into short summary. To make this I used libraries like moviepy, google's speech recognition to take the input in the form of audio-video and then use one t-5 transformer pre-trained model for text preprocessing, word tokenizing, and frequency encoding. Finally, the summarized text is displayed.
This app built-in the flask using python and planning to deploy in Heroku, but I am implementing Object Character Recognition to take input directly as text and do further processing.

requirement.txt  - This contain libraries used in this project
result.py - It's for application interface 
tts.py  -  This is the main application file 
