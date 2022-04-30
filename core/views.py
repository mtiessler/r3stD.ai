from django.shortcuts import render
from django.shortcuts import HttpResponse 
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import requests
import extras.RbAPI.py

INTERNAL = '0c8d-79-156-141-48.eu.ngrok.io'


@csrf_exempt
def upload(request):
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        files = {'file': myfile}
        response = requests.post('https://'+INTERNAL+'/uploader', files=files)
        print(response.content)
        filename = fs.save(response.name, response)
        return HttpResponse("<h1>FILE UPLOADED OK</h1>")
    else:
        return HttpResponse("<h1>FILE NOT UPLOADED OK</h1>")


def home(request):
    return render(request, "core/index.html")

def about(request):
    return render(request, 'core/about.html')

def docs(request):
    return render(request, 'core/documentation.html')

def results(request):
    uuid = 'GENERATE_REQUEST_UUID'

    try:

        # Some how obtain the video
        #video = request.FILES['file']
        
        # creates /<uuid>/images/ with all the images inside
        images_path = ImageExtractor.extract_images(uuid, video) 
        
        ok = FirebaseAPI.save_images(uuid, images_path) # uploads all images from /uuid/images to Firestore at Document Path '<uuid>/images'
        
        # creates <uuid>.obj
        model_obj = ModelGenerator.new_model(images_path)


        # Feature detection with Restb.ai API
        rb_wrapper = RbAPI()
        image_urls = FirebaseAPI.load_image_links(uuid)
        for image_url in image_urls:
            detections.append(rb_wrapper.get_all_data(image_url))

        # uploads the sketch to skfabAPI and obtains its url for the iframe
        model_url = SkfabAPI.upload_model()

        return render(request, 'core/result.html')

    except Exception as e:
        return str(e.message)

        # TODO: Define Exceptions
