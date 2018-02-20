__author__ = 'OllyD'
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpeg', '.jpg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

def validate_file_video_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4', '.mkv', '.avi', '.flv', '.wmv', '.webm', '.mpeg', '.mov']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')
# def validate_file_extension(value):
#     import os
#     from django.core.exceptions import ValidationError
#     ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
#     valid_extensions = ['.jpeg', '.jpg', '.png']
#     if not ext.lower() in valid_extensions:
#         raise ValidationError(u'Unsupported file extension.')

def validate_file_size(value):
    from django.core.exceptions import ValidationError
    filesize = value.file.size
    if filesize > int(settings.MAX_UPLOAD_SIZE):
        print(filesize)
        print(settings.MAX_UPLOAD_SIZE)
        raise ValidationError(u'File Size Too Large, Make sure it is under 500MB')





