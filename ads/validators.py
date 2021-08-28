from django.core.exceptions import ValidationError


def file_size(value):
    filesize =  value.size
    if filesize > 300000000 :
        raise ValidationError('File too large. Size should not exceed 3 MiB.')