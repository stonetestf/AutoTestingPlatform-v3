"""
Django settings for BackService project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import djcelery
# import django_redis

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_PATH = f"{BASE_DIR}/_DataFiles/Temp/"
APIFILE_PATH = f"{BASE_DIR}/_DataFiles/ApiFile/"
CASEFILE_PATH = f"{BASE_DIR}/_DataFiles/CaseFile/"
BAKDATA_PATH = f"{BASE_DIR}/_DataFiles/BakData/"

# NginxServer
NGINX_SERVER = 'http://192.168.2.12:9092/'

# region Django Celery RabbitMQ
djcelery.setup_loader()
BROKER_URL = 'amqp://lipenglo:hbwj@123@192.168.2.8:5672'
CELERY_TIMEZONE = 'UTC'  # 这里很重要,不然会出现分钟执行 小时不执行 这里必须设置这个值
CELERY_ENABLE_UTC = True

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'  # 任务元数据保存到数据库中
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_RESULT_EXPIRES = 3600  # celery任务执行结果的超时时间，
CELERYD_CONCURRENCY = 10  # celery worker的并发数
CELERYD_MAX_TASKS_PER_CHILD = 100  # 每个worker执行了多少任务就会销毁
# endregion
# region Reids
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # 'LOCATION': 'redis://192.168.243.10:6379',  # 测试
        'LOCATION': 'redis://192.168.2.8:6379',  # GS
        # 'LOCATION': 'redis://172.16.12.3:6379',  # Docker
        # 'LOCATION': 'redis://127.0.0.1:6379',  # 生产
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "Hbwj@123",
        },
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
# endregion

# dwebsocket使用 必须要 不然异步启动报错,为所有的URL提供websocket，如果只是单独的视图需要可以不选
MIDDLEWARE_CLASSES = ['dwebsocket.middleware.WebSocketMiddleware']
WEBSOCKET_ACCEPT_ALL=True   # 可以允许每一个单独的视图使用websockets

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b@-_njx8ks!#*p=dtcuf+_gwq7v6oi_3^2a^05nyjt*n7hm&_k'

# region Request 跨域
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_WHITELIST = ( '*')#跨域增加忽略
ORS_ALLOW_METHODS = ('DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT', 'VIEW',)
# 允许的请求头
CORS_ALLOW_HEADERS = (  # 前端项目设置请求头记得添加到CORS_ALLOW_HEADERS
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
    'token',
)
ALLOWED_HOSTS = ['*']
# endregion

# region Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'corsheaders',
    'djcelery',
    # 'django_celery_beat',
    'dwebsocket',
    'login',
    'Task',
    'info',
    'home',
    'upLoad',
    'routerPar',
    'role',
    'userManagement',
    'ProjectManagement',
    'PageManagement',
    'FunManagement',
    'WorkorderManagement',
    'PageEnvironment',
    'DebugTalk',
    'GlobalVariable',
    'Api_IntMaintenance',
    'Api_TestReport',
    'Api_CaseMaintenance',
    'Api_TimingTask',
    'Api_BatchTask',
]
# endregion

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'BackService.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': []
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'BackService.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'AutoTesting_v3',
        'USER': 'root',
        'PASSWORD': 'Hbwj@123',
        'HOST': '192.168.2.8',  # 开发
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'  # 少8小时就用这种参数处理
USE_I18N = True
USE_L10N = True
USE_TZ = False  # 少8小时 此参数必须为关

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

