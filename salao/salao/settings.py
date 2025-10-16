from pathlib import Path
import os, dj_database_url
from dotenv import load_dotenv
load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG =  os.getenv('DEBUG', 'False')
print('ALLOWED HOSTS: ', os.getenv('ALLOWED_HOSTS').split(','))
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'core',
    'servicos.agendamento.apps.AgendamentoConfig',
    'cadastros.cliente.apps.CadastroClienteConfig',
    'cadastros.funcionarios.apps.CadastroClienteConfig',
    'cadastros.servicos.apps.CadastroClienteConfig',
    'login.clientes.apps.LoginClienteConfig',
    'home.apps.HomePageConfig',
    'relatorios.clientes.apps.RelatorioClienteConfig',
    'configuracao.sistema.apps.ConfiguracaoSistemaConfig',
    
    
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   
]

ROOT_URLCONF = 'salao.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'home' / 'templates',
            BASE_DIR / 'relatorios' / 'agendamentos' / 'templates',
            BASE_DIR / 'relatorios' / 'clientes' / 'templates',
            BASE_DIR / 'configuracao' / 'sistema' / 'templates',
            BASE_DIR / 'servicos' / 'agendamento' / 'templates',
            BASE_DIR / 'relatorios' / 'geral' / 'templates',

        ],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = 'salao.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,  # mantém conexões abertas por mais tempo (opcional)
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

LOGIN_URL = 'cadastros/cliente'

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

CSRF_TRUSTED_ORIGINS = [
    'https://m2a-agendamento.onrender.com',
]

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

#BASE_DIR = salao
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'relatorios', 'agendamentos', 'static'),
    os.path.join(BASE_DIR, 'relatorios', 'clientes', 'static'),
    os.path.join(BASE_DIR, 'core', 'static', 'base_static'),
    os.path.join(BASE_DIR, 'home', 'static'),
    os.path.join(BASE_DIR, 'login', 'clientes','static'),
    os.path.join(BASE_DIR, 'configuracao', 'sistema', 'static'),
    os.path.join(BASE_DIR, 'relatorios', 'geral', 'static'),
    os.path.join(BASE_DIR, 'base','static'), #
    os.path.join(BASE_DIR, 'cadastros', 'cliente', 'static'),
    os.path.join(BASE_DIR, 'cadastros', 'funcionarios', 'static'),
    os.path.join(BASE_DIR, 'cadastros', 'servicos', 'static'),  
    os.path.join(BASE_DIR, 'servicos', 'agendamento', 'static'),    
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL ='media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD ='django.db.models.BigAutoField'