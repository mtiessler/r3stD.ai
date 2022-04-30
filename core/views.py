from django.shortcuts import render
from django.shortcuts import HttpResponse 
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import shutil
import cv2
import os
import json 

INTERNAL = '0c8d-79-156-141-48.eu.ngrok.io'
OUT_PATH = 'C:\\Users\\Max\Desktop\\hackupc2022\\3dmodule\\data\\nerf\\userScene\\images'


@csrf_exempt
def upload(request):
    if request.method == 'POST' and request.FILES['video']:
        myvideo = request.FILES['video']
        fs = FileSystemStorage()
        _ = fs.save(myvideo.name, myvideo)
        mytrans = None
        print(request.FILES)
        if 'transforms' in request.FILES:
            mytrans = request.FILES['transforms']
            fs = FileSystemStorage()
            transform = fs.save(mytrans.name, mytrans)
            shutil.move('media/'+mytrans.name, r"C:\Users\Max\Desktop\hackupc2022\3dmodule\data\nerf\userScene\transforms.json")
        video2frames(myvideo.name, mytrans is not None)
        os.system('python 3dmodule/scripts/run.py --scene C:\\Users\\Max\\Desktop\\hackupc2022\\3dmodule\\data\\nerf\\userScene --mode nerf --n_steps 2000 --save_mesh output.obj --near_distance 0.5')

        files = os.listdir(OUT_PATH)

        if mytrans is not None:
            os.remove(r"C:\Users\Max\Desktop\hackupc2022\3dmodule\data\nerf\userScene\transforms.json")
        for file in files:
            os.remove(OUT_PATH+"\\"+file)
    else:
        return HttpResponse("<h1>FILE NOT UPLOADED OK</h1>")


def home(request):
    return render(request, "core/index.html")

def about(request):
    return render(request, 'core/about.html')

def docs(request):
    return render(request, 'core/documentation.html')

def results(request):
    return render(request, 'core/result.html')


def video2frames(name, hasTransform):
    # Opens the inbuilt camera of laptop to capture video.
    cap = cv2.VideoCapture('media/'+name)

    i = 0

    transformFiles = []
    if hasTransform:
        file = open(r"C:\Users\Max\Desktop\hackupc2022\3dmodule\data\nerf\userScene\transforms.json", 'r')
        data = file.read()
        file.close()
        data = json.loads(data)
        transformFiles = [value['file_path'].split('/')[-1] for value in data['frames']]
    
    print(transformFiles)
    while(True):
        if not cap.isOpened():
            break
        if hasTransform and i >= len(transformFiles):
            break

        ret, frame = cap.read()
     
        # This condition prevents from infinite looping
        # incase video ends.
        if ret == False:
            break
        
        # Save Frame by Frame into disk using imwrite method
        print("Saving frame: ", i)
        if hasTransform:
            cv2.imwrite(OUT_PATH+'\\'+transformFiles[i]+".jpg", frame)
        else:
            cv2.imwrite(OUT_PATH+'\\Frame{:05d}.jpg'.format(i), frame)
        i += 1
    cap.release()
    cv2.destroyAllWindows()
    