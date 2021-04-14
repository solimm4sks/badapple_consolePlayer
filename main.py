import cv2
import pickle
import os
from timeit import default_timer as timer
from time import sleep

clear = lambda: os.system('cls')

numFrames = 6545
frameWidth = 480 // 10
frameHeight = 360 // 10

def saveVideoFrames(folderName):
    vidcap = cv2.VideoCapture('hlbadapple.mp4')
    count = 0
    success = True
    while success:
        success, image = vidcap.read()
        if success:
            image = cv2.resize(image, (frameWidth, frameHeight)) # resize to smaller rez
            cv2.imwrite(f"{folderName}/frame{count}.jpg", image)     # save frame as JPEG file     
        print('Saved frame .jpg ', count)
        count += 1
    numFrames = count

partSlice = 2500
def saveFramesMatrix(folderName, part=0):
    strt = (part - 1) * partSlice
    end = strt + partSlice
    end = min(end, numFrames)

    if part == 0:
        strt = 0
        end = numFrames

    for i in range(strt, end):
        im = cv2.imread(f"{folderName}/frame{i}.jpg", cv2.IMREAD_GRAYSCALE)
        im = im.tolist()
        for x in range(len(im)):
            for y in range(len(im[x])):
                if im[x][y] >= 127:
                    im[x][y] = True
                else:
                    im[x][y] = False

        # print(im)
        with open(f'{folderName}/data{i}.pkl', 'wb') as out:
            pickle.dump(im, out, pickle.HIGHEST_PROTOCOL)
        print(f"Saved frame pickle {i}")

def readFramesMatrix(folderName):
    frames = []
    for i in range(numFrames):
        with open(f'{folderName}/data{i}.pkl', 'rb') as inp:
            frm = pickle.load(inp)
            frames.append(frm)
        print(f'Read frame {i}')
    return frames

def consolePlay():
    frames = readFramesMatrix()
    spf = 0.02 # sleep per frame
    for fr in frames:
        start = timer()
        string = ""
        for x in fr:
            for y in x:
                if y:
                    string += "11"
                else:
                    string += "00"
            string += "\n"
        print(string)

        end = timer()
        procTime = end - start

        if spf - procTime > 0:
            sleep(spf - procTime)
        clear()

saveVideoFrames()
saveFramesMatrix()
consolePlay()