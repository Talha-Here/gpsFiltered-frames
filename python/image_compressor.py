from PIL import Image
import os


path = r"./data_jpg"
destination = r"./compressed_jpg"

def compress_image(src_location, dst_location=None):
    images = [file for file in os.listdir(path) if file.endswith(('png','jpg','jpeg','webp'))]

    if dst_location == None:
        for image in images:
            print(image)
            img = Image.open(f"{path}/{image}")
            img.save(f"{path}/{image}", optimize=True, quality=30)
    else:
        for image in images:
            print(image)
            img = Image.open(f"{path}/{image}")
            img.save(f"{dst_location}/Copressed_amd_Resized+{image}",optimize=True, quality=30)

compress_image(path,destination)