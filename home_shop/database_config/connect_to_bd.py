import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'

# Если хотите — автоматически подгрузить .env
if ENV_PATH.exists():
    for line in ENV_PATH.read_text().splitlines():
        if not line or line.strip().startswith('#'):
            continue
        k, v = line.split('=', 1)
        os.environ.setdefault(k, v)


def get_env(var_name: str, default=None, required: bool = False):
    """
    Читает переменную окружения, кидает ImproperlyConfigured,
    если required=True и переменная не задана.
    """
    val = os.getenv(var_name, default)
    if required and val is None:
        raise ImproperlyConfigured(f"Set the {var_name} env variable")
    return val


def build_databases():
    return {
        'default': {
            'ENGINE': get_env('DB_ENGINE', 'django.db.backends.sqlite3'),
            'NAME': get_env('DB_NAME', BASE_DIR / 'db.sqlite3'),
            'USER': get_env('DB_USER', ''),
            'PASSWORD': get_env('DB_PASSWORD', ''),
            'HOST': get_env('DB_HOST', ''),
            'PORT': get_env('DB_PORT', ''),
        }
    }
