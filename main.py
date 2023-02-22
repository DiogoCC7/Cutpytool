import datetime

from datetime import datetime
from os import listdir, path, makedirs
from PIL import Image

LEFT=70
RIGHT=50
TOP=150
DOWN=70

def get_png(folder):

    png = []

    for dir in listdir(folder):  
        if dir.endswith(".png"):
              png.append(path.join(folder, dir))
    
    return png

def crop_imgs(arr_img):
    
    croped_img = []

    for path_img in arr_img:
        croped_img.append(crop_img(path_img))

    return croped_img

def crop_img(path_to_image: str):

    with Image.open(path_to_image) as img:
        img.load()

    return img.crop((LEFT, TOP, img.size[0] - RIGHT, img.size[1] - DOWN))


def create_dir(out):

    dir = datetime.today().strftime('%Y-%m-%d')
    dir = path.join(out, dir)

    if path.exists(dir) is False:
        makedirs(dir)

    return dir

def main(input_folder, output_folder):

    i = 1
    path_to_dir = create_dir(output_folder)
    croped_img = crop_imgs(get_png(input_folder))

    for img in croped_img:
        img.save(path.join(path_to_dir, str(i) + ".png"))
        i+=1
        print(f"Image Cropped into {path_to_dir} count {i}")

main("tmp", "dist")