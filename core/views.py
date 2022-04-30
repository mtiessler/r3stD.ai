from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, "core/tryout.html")
@csrf_exempt
def upload(request):
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        return HttpResponse("<h1>FILE UPLOADED OK</h1>")
    else:
        return HttpResponse("<h1>FILE NOT UPLOADED OK</h1>")