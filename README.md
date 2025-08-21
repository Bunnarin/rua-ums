git clone https://github.com/Bunnarin/$APP_DIR
cd $APP_DIR
mv .env.staging .env
nano .env
AT FIRST, u must set CACHE_DISABLED to true in .env simply to avoid cache migration issue

sudo docker compose up