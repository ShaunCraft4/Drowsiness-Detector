#Importing required libraries:
import cv2
import time
import playsound


#Initializing required variables:
Tired_Check = 0
Blink_Start_Time = None
Eye_Cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml') #Contains pre trained data for eye detection
Cap = cv2.VideoCapture(0)
Alert_Sound = 'alerting_sound.wav' #Contains the alert sound


#Initializing required functions:
def Eye_Detection(Eyes):
    for (x, y, w, h) in Eyes:
        cv2.rectangle(Frame, (x, y), (x+w,y+h) , (255, 255, 0), 2) #Draws rectangles around the eyes 
        
def Tiredness_Count(Eyes):
    global Tired_Check
    global Blink_Start_Time
    if len(Eyes) == 0: #Checking if eyes are closed
        if Blink_Start_Time is None:
            Blink_Start_Time = time.time() #Starting timer for when eye is closed
        else:
            Blinking_Time = time.time() - Blink_Start_Time #Calculating amount fo time eye was closed
            if Blinking_Time > 0.5: #Checking if the eye was closed for more than 0.5 seconds
                Tired_Check += 1 #Adding 1 to Tired_Check
                Blink_Start_Time = None #Reset the initial Timer
    else:
        Blink_Start_Time = None
    
def Tiredness_Confirmation():
    global Tired_Check
    if Tired_Check > 7:  #Checking if the person was detected for being tired more than 7 times
        playsound.playsound(Alert_Sound) #Plays the alerting sound when detected
        Tired_Check = 0 #Resets the variable to 0
        
        
#Starting Loop for camera            
while True:
    Ret, Frame = Cap.read() #Getting image from camera
    
    cv2.putText(Frame, f"Tiredness Counter: {Tired_Check}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2) #Displaying number of blinks
    
    Gray = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY) #Converting the frame into grayscale for checking eyes
    
    Eyes = Eye_Cascade.detectMultiScale(Gray, 1.3, 5) #Detects the eyes within the grayscale image
    
    Eye_Detection(Eyes) #Drawing rectangles around the eyes
    
    Tiredness_Count(Eyes)  #Checking if the person is tired
    
    Tiredness_Confirmation() #Confirming whether the person needs to stop driving and rest
    
    cv2.imshow('Drowsiness Detection', Frame) #Naming the window

    if cv2.waitKey(1) & 0xFF == ord('q'): #Providing key is terminate the code
        break


#Closing the System
Cap.release() #Stopping camera
cv2.destroyAllWindows() #Closing all windows
