import cv2
import os 
import ffmpeg
#import subprocess
import sys



from pprint import pprint  # for printing Python dictionaries in a human-readable way

url = './video/Bank.mp4'
#url = 'https://firebasestorage.googleapis.com/v0/b/deeprowserverless.appspot.com/o/Survey-Videos%2Fhero5.mp4?alt=media&token=845f71e0-8bec-46d4-87f1-4e8a31975e1d'
#url = 'https://firebasestorage.googleapis.com/v0/b/deeprowserverless.appspot.com/o/Survey-Videos%2Fvideo3_2s_1600x1200_30fps_75f.AVI?alt=media&token=08a8d005-3f9d-4a71-9f24-08368bf8d739'
cap = cv2.VideoCapture(url)

try:

    if not os.path.exists('data'):
        os.makedirs('data')
        print("data directory created")

except OSError:
    print('Error: Creating directory of data')

def imageExtraction(url):
    currentframe = 0
    # read the audio/video file from the command line arguments
    media_file = url
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    # uses ffprobe command to extract all possible metadata from the media file
    # pprint(ffmpeg.probe(media_file)["streams"])
    while (True):
     success, frame = cap.read()
     if success:
        name = './data/frame' + str(currentframe) + '.jpg'
        print('Creating...' + name)
        cv2.imwrite(name, frame)
        currentframe += 1
        cv2.imshow("ok", frame)  # Note cv2_imshow, not cv2.imshow
        cv2.waitKey(1) & 0xff
        
     else:
        break


#def runCommand(cmd: str) -> str:
 #   out = subprocess.run(cmd, shell=True, check=True, universal_newlines=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 #   strOut = out.stdout.decode('UTF-8')
 #   print(strOut)
 #   return strOut



#vid = cv2.VideoCapture("https://www.youtube.com/")   

#../GoPro-Telemetry-Tests/TelemetryTests/data/karma.mp4
#runCommand("node ../GoPro-Telemetry-Tests/TelemetryTests/index.js  ../GoPro-Telemetry-Tests/TelemetryTests/jjsondata/")
imageExtraction(url=url)
cap.release()
cv2.destroyAllWindows()
