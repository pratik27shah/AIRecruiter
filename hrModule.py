from dotenv import load_dotenv
load_dotenv()
import time
import google.generativeai as genai
import os
import pyttsx3
import speech_recognition as sr


genai.configure(api_key="AIzaSyB4KCg8smLEXmKfrgdFwaA_G1gltCWy")


model = genai.GenerativeModel('gemini-pro')
r = sr.Recognizer() 

def hr_speak(content):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices=engine.getProperty('voices')
    engine.setProperty("voice",voices[1].id)
    engine.say(content)
    engine.runAndWait()

def get_gemini_response_for_hr_intro(question,candidate_name):
    question_intro_hr="HR quick short introduction to candidate  to be said on call during start of  interview for this job description"+question +" and candidate name is " + candidate_name +" HR name is AI-Recruiter"
    response = model.generate_content(question_intro_hr)
    test=response.text.replace("\n","").replace(".","").replace("*","").split()
    words=""
    i=0
    for x in test:
        words=words+x
        i=i+1
        if(i==23):
            i=0
            hr_speak(words)
            words=""
    hr_speak(words)
    return create_gemini_response_for_hr_questions(question)

def output_ans():
    r = sr.Recognizer() 
    start_time = time.time()
    details=""
    print("Start speaking, say thank you to lock the ans")
    while(1):    
        try:         
            # use the microphone as source for input.
            with sr.Microphone() as source2:
                
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level 
                
                r.adjust_for_ambient_noise(source2, duration=1)
                #listens for the user's input 
                audio2 = r.listen(source2)
                #print("----->",audio2.get_wav_data)
                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                details=details + MyText
                print("Did you say ",MyText)
                if(MyText in "thank you"):
                    print ("Response recorded")
                    break
                if time.time() - start_time >= 60:
                    print ("Response recorded")
                    break
        except sr.RequestError as e:
            #MyText=""
            print("Could not request results; {0}".format(e))
    return details

def create_gemini_response_for_hr_questions(input):
    question_list="atleast 3 HR  interview questions to be said on call to candidate in list format without categories for thi s job"+input
    response = model.generate_content(question_list)
    anslist="";
    response=response.text.split("\n")
    if(len(response)>3):
        response=response[:3]
    ques=1
    hr_speak("You would have 60 seconds to record your response or say thank you  to record ans ")
    anslist="";
    for x in response:
        hr_speak(x.replace("*","").replace(".",""))
        candidate_ans=output_ans()
        anslist=anslist+ " Question "+x.replace("*","").replace(".","")+"Ans: "+candidate_ans
        if(ques<2):
             hr_speak("OK, next question is ")
        else:
            hr_speak("Processing your answers")
        ques=ques+1
    status="Is candidate qualified for this job description "+input + " this is summary of his interview" + anslist
    result = model.generate_content(status)
    #print(status)
    hr_speak("We will review your answers and get back to you,thank you for your time")
    return result.text
