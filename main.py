import datetime
import time
import uuid
import argparse
import tomli

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from datetime import datetime
from os import listdir, path, makedirs, system
from PIL import Image

CONFIG_FILE_PATH="default.toml"

input_dir="."
output_dir="dist"
left=70
right=50
top=150
bottom=70

class EventHandler(PatternMatchingEventHandler):

    def __init__(self) -> None:
        super(EventHandler, self).__init__(ignore_patterns=["*/*.png"])

    def on_created(self, event):

        basePath = path.basename(event.src_path)
        time.sleep(1)
        crop(basePath, output_dir)

        return super().on_created(event)
    
def watch_mode():

    event_handler = EventHandler()

    observer = Observer()
    observer.schedule(event_handler, path=input_dir, recursive=True)
    print("Add Files to this folder to start cropping it")
    observer.start()
    
    try:
        while(True):
           time.sleep(1)
           
    except KeyboardInterrupt:
            observer.stop()
            observer.join()

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

    return img.crop((left, top, img.size[0] - right, img.size[1] - bottom))


def create_dir(out):

    dir = datetime.today().strftime('%Y-%m-%d')
    dir = path.join(out, dir)

    if path.exists(dir) is False:
        makedirs(dir)

    return dir

def persist_imgs(croped_img, path_to_dir):

    i = 0

    if isinstance(croped_img, list) is False:
        croped_img.save(path.join(path_to_dir, f"{uuid.uuid4()}" + ".png"))
        print(f"Image Cropped into {path_to_dir}")
        return

    for img in croped_img:
        img.save(path.join(path_to_dir, str(i) + ".png"))
        i+=1
        print(f"Image Cropped into {path_to_dir} count {i}")

def crop(input_folder, output_folder):

    path_to_dir = create_dir(output_folder)

    if path.isdir(input_folder):
        croped_img = crop_imgs(get_png(input_folder))
    else:
        croped_img = crop_img(input_folder)

    persist_imgs(croped_img, path_to_dir)

def load_configuration(header):
    
    with open(CONFIG_FILE_PATH, "rb") as conf_file:
        conf = tomli.load(conf_file)

    return conf[header]

def open_configuration_file():
    system(CONFIG_FILE_PATH)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="SLB!")

    parser.add_argument('--path', default=False, action="store_true", help="change configuration")
    parser.add_argument('--watch', default=False, action="store_true", help="listen changes on the input folder")
    parser.add_argument('--i', type=str, default=".", help="input folder")
    parser.add_argument('--o', type=str, default="dist", help="output folder")
    parser.add_argument('--conf', type=str, default="edge", help="defines cutting mode, selected from configuration file")
    arg = parser.parse_args()

    configuration = load_configuration(arg.conf)

    input_dir = arg.i
    output_dir = arg.o
    left = configuration["left"]
    right = configuration["right"]
    top = configuration["top"]
    bottom = configuration["bottom"]

    if arg.watch:
        watch_mode()
    elif arg.path:
        open_configuration_file()
    else:
        crop(input_dir, output_dir)