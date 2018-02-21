import datetime
import os
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY') 
AWS_STORAGE_BUCKET_NAME = 'visumic-bucket'
AWS_S3_FILE_OVERWRITE = False
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True
#AWS_S3_SECURE_URLS = False
S3DIRECT_REGION = 'us-east-2'
# AWS_S3_URL_PROTOCOL = ''
#WORKING MEDIA
# DEFAULT_FILE_STORAGE = 'vidcraft.aws.utils.MediaRootS3BotoStorage'
# MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
# MEDIA_ROOT =


# STATICFILES_STORAGE = 'vidcraft.aws.utils.StaticRootS3BotoStorage'
# AWS_STORAGE_BUCKET_NAME = 'visumic-bucket'
#
# S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

# STATIC_URL = S3_URL + 'static/'
#ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
#

#TWO
AWS_S3_CUSTOM_DOMAIN = 's3.%s.amazonaws.com/%s' % (S3DIRECT_REGION, AWS_STORAGE_BUCKET_NAME)

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'vidcraft.aws.utils.MediaRootS3BotoStorage'

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'vidcraft.aws.utils.StaticRootS3BotoStorage' #'vidcraft.aws.custom_storages.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)



two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
'Expires': expires,
'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}

#END TWO
# remind = "https://s3.us-east-2.amazonaws.com/visumic/static/static/css/main.css"
#https://s3.us-east-2.amazonaws.com/visumic-bucket/static/css/main.css
# We also use it in the next setting.


#AWS_S3_CUSTOM_DOMAIN = AWS_S3_CUSTOM_DOMAIN + '/static'

# This is used by the `static` template tag from `static`, if you're using that. Or if anything else
# refers directly to STATIC_URL. So it's safest to always set it.
#STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN


# Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
# you run `collectstatic`).
#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'




# MEDIAFILES_LOCATION = 'media'
# MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
# DEFAULT_FILE_STORAGE = 'vidcraft.aws.custom_storages.MediaStorage'










#DONT USE
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

#ONE
# DEFAULT_FILE_STORAGE = 'vidcraft.aws.utils.MediaRootS3BotoStorage'
# STATICFILES_STORAGE = 'vidcraft.aws.utils.StaticRootS3BotoStorage'
# AWS_STORAGE_BUCKET_NAME = 'visumic-bucket'
# S3DIRECT_REGION = 'us-east-2'
# S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
# MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
# MEDIA_ROOT = MEDIA_URL
# STATIC_URL = S3_URL + 'static/'
# ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
#
# two_months = datetime.timedelta(days=61)
# date_two_months_later = datetime.date.today() + two_months
# expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")
#
# AWS_HEADERS = {
#  'Expires': expires,
#  'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
# }
 #ENDONE
