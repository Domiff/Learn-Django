from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.files.storage import FileSystemStorage


def get_request_method(request: HttpRequest):
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {
        "a": a,
        "b": b,
        "result": result,
    }
    return render(request, 'requestdataapp/request-params.html', context=context)


def get_post(request: HttpRequest):
    context = {
        
    }
    return render(request, 'requestdataapp/forms.html', context=context)


def upload_file(request: HttpRequest):
    if request.method == "POST" and request.FILES.get("myfile"):
        my_file = request.FILES["myfile"]
        fs = FileSystemStorage()
        file_name = fs.save(my_file.name, my_file)
        
    return render(request, 'requestdataapp/file_upload.html')
