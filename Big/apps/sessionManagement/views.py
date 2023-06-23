from django.shortcuts import redirect,render

# 세션 검사 미들웨어
class CheckSessionExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        # 세션 만료 + 로그인/로그인검사/회원가입/회원가입검사 URL이 아닐 때
        if 'user' not in request.session and \
            request.path not in ['/', '/login/submit/', '/register/', '/priv/','/register/submit/', '/register/id_inspection/'] :
            
            return render(request, 'session/sessionAlert.html')  # 세션 만료 시 로그인 화면으로 이동

        response = self.get_response(request)   
        return response