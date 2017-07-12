import datetime
import os
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID') #"AKIAIWPRIUTTARYHLUUA"
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY') #"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"
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

DEFAULT_FILE_STORAGE = 'vidcraft.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'vidcraft.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'visumic'
S3DIRECT_REGION = 'us-east-2'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
S4_URL = 's3.%s.amazonaws.com/%s' % (S3DIRECT_REGION, AWS_STORAGE_BUCKET_NAME)
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
'Expires': expires,
'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}

# remind = "https://s3.us-east-2.amazonaws.com/visumic/static/static/css/main.css"


#from storages.backends.s3boto3 import S3Boto3Storage
import os

# AWS_ACCESS_KEY_ID = "AKIAIWPRIUTTARYHLUUA" #os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = "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" #os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = 'visumic'
#
# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#
# STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'
# ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'