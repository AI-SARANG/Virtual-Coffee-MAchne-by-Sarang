#Step 1 : Check Camera and background os and cv2
import os
from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)
cap.set(1,640)
cap.set(2,480)

#Step2 : Overlay Background Image code in line no. 11 and 17 then run it
#we got 2 images overlay after run
#for stop this we write code in line no. 18 & 19

imgBackground = cv2.imread("Resources/Background.png")

#for MODES part

# importing all the mode images to a list
folderPathModes = "Resources/Modes"
listImgModesPath = os.listdir(folderPathModes)
listImgModes = []
for imgModePath in listImgModesPath:
    listImgModes.append(cv2.imread(os.path.join(folderPathModes, imgModePath)))
print(listImgModes)

# importing all the icons to a list
folderPathIcons = "Resources/Icons"
listImgIconsPath = os.listdir(folderPathIcons)
listImgIcons = []
for imgIconsPath in listImgIconsPath:
    listImgIcons.append(cv2.imread(os.path.join(folderPathIcons, imgIconsPath)))


#importing all the icons to a list
modeType = 0 #for changing selection mode
selection = -1
counter = 0
selectionSpeed = 7  #selection speed
detector = HandDetector(detectionCon=0.8, maxHands=1)    #copy from handdetector left press button on mouse
modePositions = [(1136,196),(1000,384),(1136,581)]      #for selection of coffee, tea, latte
counterPause = 0                                        #for pause for selction circle then add to if hand & counter paused
selectionList = [-1, -1, -1]

while True:            #c n p from handfile
    success, img = cap.read()
    # Find the hand and its landmarks #hand detector C n P
    hands, img = detector.findHands(img)  #with draw

    #ovrlaying the webcam feed on the Background image here 139 is ht. 480 is img ht.

    imgBackground[139:139 + 480, 50:50 + 640] = img
    imgBackground[0:720,847:1280] = listImgModes[modeType]
    #in above here you change modeType into o to 1 for sugar




    if hands and counterPause == 0 and modeType < 3:
        # Hand 1
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        print(fingers1)

        if fingers1 == [0,1,0,0,0]:      #for first finger
            if selection != 1:
                counter = 1
            selection = 1
        elif fingers1 == [0,1,1,0,0]:      #for two finger
            if selection != 2:
                counter = 1
            selection = 2
        elif fingers1 == [0,1,1,1,0]:       #for three finger
            if selection != 3:
                counter = 1
            selection = 3
        else:
            selection = -1
            counter = 0

        if counter>0:
            counter+=1
            print(counter)
            #we creat elipse is fun. create variable arc
            cv2.ellipse(imgBackground,modePositions[selection-1],(103, 103),0,0,
                        counter * selectionSpeed, (0, 255, 0), 20)    #if counter completed then go to next page then
            if counter * selectionSpeed > 360:
                selectionList[modeType]=selection
                modeType +=1
                counter=0
                selection=-1
                counterPause=1

#To pause after selection is made


    if counterPause>0:
        counterPause+=1
        if counterPause>40:            #for selection t,c,l item for paused we should increase it by 60
            counterPause = 0

    # Add selection icon at the bottom
    if selectionList[0] != -1:
        imgBackground[636:636+65, 133:133+65] = listImgIcons[selectionList[0]-1]   #now we replacte 3 time so we code copy as same
    if selectionList[1] != -1:
        imgBackground[636:636+65, 340:340 +65] = listImgIcons[5+selectionList[1]]
    if selectionList[2] != -1:
        imgBackground[636:636 + 65, 542:542 + 65] = listImgIcons[6+selectionList[2]]

        #you can choose any number in above, we have 1-9 images so choose what you want

            # DISPLAYING THE IMAGE
    # cv2.imshow("Image", img)
    cv2.imshow("Background",imgBackground)
    cv2.waitKey(2)

