import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k&ard*hs82=w8b%sre##mi@!#+j5+_88=49(rz6d)s=gsld5!_'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG 值要等于True
#2021年1月24日部署nginx
DEBUG = True

ALLOWED_HOSTS = ['*']
#127.0.0.1/localhost 将不允许 Firefox 显示嵌入于其他网站的页面
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'monitor',
    'index',
    'dwebsocket',#2021年2月16日19:23:08 添加dwebsocket 实现websocket
]
WEBSOCKET_ACCEPT_ALL=True   # 可以允许每一个单独的视图使用websockets

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sniper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'sniper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.mysql',
'NAME': 'sniper', #数据库名
'USER': 'root', #数据库用户名
'PASSWORD': 'sadboy', #数据库密码
'HOST': 'localhost', #数据库服务器ip
'PORT': '3306', #数据库端口
}
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL='auth.User'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


###邮件发送配置###
# 发送邮件
# 发送邮件设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False   # 是否使用TLS安全传输协议
EMAIL_USE_SSL = False    # 是否使用SSL加密，qq企业邮箱要求使用
# SMTP地址
EMAIL_HOST = 'smtp.qq.com'
# SMTP端口 587为加密端口 25为非加密
EMAIL_PORT = 25
# 自己的邮箱
EMAIL_HOST_USER = '2912285367@qq.com'
# 自己的邮箱授权码，非密码
EMAIL_HOST_PASSWORD = 'cimfktrhhruydghe'
EMAIL_SUBJECT_PREFIX = '沉船资本'