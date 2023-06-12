# workLog views

from django.views import View
from django.shortcuts import render
from django.http import JsonResponse


def workLog(request) :
    session_id = {
        'user' : request.session.get('user')
    }
    return render(request, 'workLog/workLog.html', session_id)

class workLogView(View) :
    def get(self, request) :
        if 'user' in request.session :
            return JsonResponse({'message' : request.session['user']}, status = 201)
        else :
            return JsonResponse({'message' : 'None'}, status = 201)