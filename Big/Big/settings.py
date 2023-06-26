from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-mh=_xfbdr^)6@lr9_!209!mrm4mrs5-3!gtrmnjs%*z-eqd_u$"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Big Project Apps
    "django_extensions",
    "apps.login.apps.LoginConfig", # login
    "apps.workLog.apps.WorklogConfig", # workLog
    "apps.upload.apps.UploadConfig", # upload
    "apps.notice.apps.NoticeConfig", # notice
    "apps.videoLog.apps.VideologConfig", # videoLog
    "apps.sessionManagement.apps.SessionmanagementConfig" # sessionManagement
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    # Big Project MiddleWare
    'apps.sessionManagement.views.CheckSessionExpiryMiddleware', # 세션 매니저
] #"django.middleware.csrf.CsrfViewMiddleware",

ROOT_URLCONF = "Big.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [f'{BASE_DIR}/templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Big.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# LANGUAGE_CODE = "en-us"
# TIME_ZONE = "UTC"

LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"

USE_I18N = True

# USE_TZ = True 
USE_TZ = False # 로컬 시간을 저장

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 빅프로젝트 설정 --------------------------------------------
# 정적파일 
STATIC_URL = "static/"
STATICFILES_DIRS = [ # 정적파일 폴더경로 지정
    os.path.join(BASE_DIR, 'static\\'), ]

# 세션
SESSION_COOKIE_AGE = 3600  # 1시간 => (60분 x 60초)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True # 웹 브라우저 종료 시, 세션 자동 만료
CHECK_INTERVAL = 10 # 세션 검사 시간
