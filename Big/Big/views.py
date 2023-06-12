from django.shortcuts import render

# 메인 화면
def main(request) :
    return render(request, 'main.html')