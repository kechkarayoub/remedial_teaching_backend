from os.path import abspath, dirname, join

DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ["http://localhost:3000"]

# google storage config
GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = join(dirname(abspath(__file__)), 'dev_mafatih/healthkoolsdev_drive_storage.json')  # path to private json key file obtained by Google.
GOOGLE_DRIVE_STORAGE_SERVICE_EMAIL = "healthkoolsdev@gmail.com"
