from django.shortcuts import render, redirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from .extras.FirebaseAPI import FirebaseAPI
from .extras.SkfabAPI import SkfabAPI
from .extras.RbAPI import RbAPI
import requests
import shutil
import cv2
import os
import json
import uuid

from core.extras.FirebaseAPI import FirebaseAPI 


OUT_PATH = 'C:\\Users\\Max\Desktop\\hackupc2022\\3dmodule\\data\\nerf\\userScene\\images'
TRANSFORMS_PATH = r"C:\Users\Max\Desktop\hackupc2022\3dmodule\data\nerf\userScene\transforms.json"

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        if 'obj' in request.FILES:
            pass #to be implemented
        elif 'video' in request.FILES:    
            myvideo = request.FILES['video']
            fs = FileSystemStorage()
            _ = fs.save(myvideo.name, myvideo)
            mytrans = None
            if 'transforms' in request.FILES:
                mytrans = request.FILES['transforms']
                fs = FileSystemStorage()
                transform = fs.save(mytrans.name, mytrans)
                shutil.move('media/'+mytrans.name, TRANSFORMS_PATH)
            video2frames(myvideo.name, mytrans is not None)
            if mytrans is None:
                os.system('python C:/Users/Max/Desktop/hackupc2022/3dmodule/scripts/colmap2nerf.py --run_colmap --colmap_matcher exhaustive --aabb_scale 2  --images '+OUT_PATH+' --out '+ TRANSFORMS_PATH)
            os.system('python 3dmodule/scripts/run.py --scene C:\\Users\\Max\\Desktop\\hackupc2022\\3dmodule\\data\\nerf\\userScene --mode nerf --n_steps 2000 --save_mesh C:\\Users\\Max\\Desktop\\hackupc2022\\3dmodule\\data\\nerf\\userScene\\output.obj --near_distance 0.5')
            files = os.listdir(OUT_PATH)
            if mytrans is not None:
                os.remove(TRANSFORMS_PATH)
            for file in files:
                os.remove(OUT_PATH+"\\"+file)
        return redirect('results')
    else:
        return redirect('')


def home(request):
    return render(request, "core/index.html")

def about(request):
    return render(request, 'core/about.html')

def docs(request):
    return render(request, 'core/documentation.html')

def results(request):
    fb_uuid = uuid.uuid4().hex
    model_images_folder_path = 'C:\\Users\\Max\\Desktop\\hackupc2022\\3dmodule\\data\\nerf\\userScene\\model_images\\' # TODO
 
    fb = FirebaseAPI()
    rb = RbAPI()  

    ok = fb.save_model_images(fb_uuid, model_images_folder_path)
    if not ok:
        return "Failed to save images to FirebaseAPI"

    images = []
    model_image_links = fb.load_model_image_links(fb_uuid)
    for link in model_image_links:
        annotations = rb.get_all_data(link)
        # images.append({'link': link, 'annotations': annotations})

    # A su vez, como tenemos el OBJ, lo subimos a sketchfab
    # Una vez subido, accedemos a la URL para obtener el UID del sketch
    # Finalmente pasamos este UID a la template de results para cargar el sketch en el iframe
    model_path = 'C:\\Users\\Max\\Desktop\\hackupc2022\\3dmodule\\data\\nerf\\userScene\\scan.obj' # TODO
    model_url = SkfabAPI.upload_model(model_path)
    sketch_uid = model_url.split('/')[-1]
    
    #get_result = requests.get(model_url)
    #print(get_result.json()['uid'])
    print(sketch_uid, images)
    return render(request, 'core/result.html', {'images': images, 'annotations': annotations, 'sketch_uid': sketch_uid})


def video2frames(name, hasTransform):
    # Opens the inbuilt camera of laptop to capture video.
    cap = cv2.VideoCapture('media/'+name)

    i = 0

    transformFiles = []
    if hasTransform:
        file = open(TRANSFORMS_PATH, 'r')
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
            cv2.imwrite(OUT_PATH+'\\'+transformFiles[i], frame)
        else:
            cv2.imwrite(OUT_PATH+'\\Frame{:05d}.jpg'.format(i), frame)
        i += 1
    cap.release()
    cv2.destroyAllWindows()
    