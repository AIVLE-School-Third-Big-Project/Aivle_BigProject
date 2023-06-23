from django.shortcuts import render

def notice(request) :
    return render(request, 'notice/notice.html')

def noticeView(request) :
    return render(request, 'notice/noticeView.html')

def noticeWrite(request) :
    return render(request, 'notice/noticeWrite.html')

def noticeEdit(request) :
    return render(request, 'notice/noticeEdit.html')
