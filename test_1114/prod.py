from .settings import *
import os
DEBUG = os.environ.get('DEBUG') in ['1', 't', 'true', 'T', 'True']

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", '').split(',')

STATICFILES_STORAGE = "test_1114.storages.StaticAzureStorage"

DEFAULT_FILE_STORAGE = "test_1114.storages.MediaAzureStorage"



AZURE_ACCOUNT_NAME = os.environ["AZURE_ACCOUNT_NAME"]
AZURE_ACCOUNT_KEY = os.environ["AZURE_ACCOUNT_KEY"]


DATABASES = {
    'default': {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
        "HOST": os.environ["DB_HOST"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "NAME": os.environ.get("DB_NAME", "postgres"),
    },
}

# docker run --rm --publish 9966:80 ^
# -e DJANGO_SETTINGS_MODULE=test_1114.prod ^
# -e AZURE_ACCOUNT_NAME=gwanholee ^
# -e AZURE_ACCOUNT_KEY="1pxZCpuYMvPSG1/3ujZunNHtk2NxLPdbWpppoKP4OvSQ2JWvs2BXfiUq7tnfY7j5SZTpe1scyWkxWKWbtv6LUQ==" ^
# -e ALLOWED_HOSTS=localhost ^
# -e DB_HOST=leegwanho.postgres.database.azure.com ^
# -e DB_USER=gwanholee@leegwanho ^
# -e DB_PASSWORD=shirthdagara1! ^
# -e DB_NAME=postgres ^
# -it test1114 sh
