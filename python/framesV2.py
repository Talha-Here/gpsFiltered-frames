import cv2
y_crop = 0;


def extractFrames(videoPath, idx_arr, folderPath, genTempLink = None, index_offset = 0):
    arr_names = []
    print(f"{idx_arr} {len(idx_arr)}")
    if(genTempLink is not None):
        videoPath = genTempLink(videoPath);
    cap = cv2.VideoCapture(videoPath)
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx_arr[0])
    i = idx_arr[0]
    index = index_offset
    while i < idx_arr[-1] + 1:
        if(i in idx_arr):
            ret,frame = cap.read()
            if(ret == True):

                f1 = 852 / frame.shape[1]
                f2 = 480 / frame.shape[0]
                f = min(f1, f2)  # resizing factor
                dim = (int(frame.shape[1] * f), int(frame.shape[0] * f))
                resized = cv2.resize(frame, dim)
                cv2.imwrite(f"{folderPath}/{str(index)}.jpg", resized)
                arr_names.append(f"{str(index)}.jpg")
                index += 1
        else:
            ret = cap.grab()
        if ret == True:
            i+=1;
        print(f"{cap.get(cv2.CAP_PROP_POS_FRAMES)} {i} {ret}")
    return arr_names

def getYCrop():
    return y_crop;


videoPath = './video/Bank.mp4'
folderPath = './data_jpg'
idx_arr = [1, 2, 3]

frames = extractFrames(videoPath, idx_arr,  folderPath)
