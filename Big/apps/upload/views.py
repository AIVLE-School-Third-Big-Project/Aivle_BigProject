from django.shortcuts import render

def uploadIn(request) :
    return render(request, 'upload/uploadIn.html')

def uploadOut(request) :
    return render(request, 'upload/uploadOut.html')

def uploadWork(request) :
    return render(request, 'upload/uploadWork.html')