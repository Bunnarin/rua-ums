git clone https://github.com/Bunnarin/$APP_DIR
cd $APP_DIR
mv .env.staging .env
nano .env
AT FIRST, u must set CACHE_DISABLED to true in .env simply to avoid cache migration issue
set up github secret and var
then, generate secret key for django
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# setup db
CREATE USER user WITH PASSWORD '159357';
CREATE DATABASE db OWNER user;
GRANT ALL PRIVILEGES ON DATABASE db TO user;

sudo docker compose up