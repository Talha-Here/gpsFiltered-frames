import cv2
import os

# image_folder = './compressed_webp'
# video_folder = './video/compile_video.mp4'

# images = [img for img in os.listdir(image_folder) if img.endswith(".webp")]
# frame = cv2.imread(os.path.join(image_folder, images[0]))
# height, width, layers = frame.shape

# video = cv2.VideoWriter(video_name, 0, 1, (width,height))

# for image in images:
#     video.write(cv2.imread(os.path.join(image_folder, image)))

# cv2.destroyAllWindows()
# video.release()

# print("COMPILED")

def compile_video(image_folder, video_folder):
    images = [img for img in os.listdir(image_folder) if img.endswith(('png','jpg','webp'))]
    if not images:
        print("No image files found in the specified folder.")
        return None
    print(images)
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_folder, 0, 1, (width,height))
    
    for image in images:

        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
    print("COMPILED")

    return video_folder

image_folder = './compressed_webp'
video_folder = './video/compile_video.mp4'
compile_video(image_folder, video_folder)
