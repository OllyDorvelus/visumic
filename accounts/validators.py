__author__ = 'OllyD'

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
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





