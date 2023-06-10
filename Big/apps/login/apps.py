from django.apps import AppConfig


class LoginConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.login" # apps 폴더안에 있기에 apps. 를 추가
