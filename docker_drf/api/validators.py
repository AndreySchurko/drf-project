from django.core.exceptions import ValidationError
import re
from django.utils.translation import gettext as _


def validate_file_size(value):
    # 2.5MB - 2621440
    # 5MB - 5242880
    # 10MB - 10485760
    # 20MB - 20971520
    # 50MB - 5242880
    # 100MB 104857600
    # 250MB - 214958080
    # 500MB - 429916160

    max_upload_size = 20971520
    filesize = value.size
    if filesize > max_upload_size:
        raise ValidationError("File too large. Size should not exceed 20 MB.")
    else:
        return value


class UppercaseValidator(object):
    """The password must contain at least 1 uppercase letter, A-Z."""
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _('The password must contain at least 1 uppercase letter, A-Z.'), code='password_no_upper',)

    def get_help_text(self):
        return _('Your password must contain at least 1 uppercase letter, A-Z.')


class SpecialCharValidator(object):
    """ The password must contain at least 1 special character @#$%!^&* """
    def validate(self, password, user=None):
        if not re.findall('[@#$%!^&*~]', password):
            raise ValidationError(
                _('The password must contain at least 1 special character: @#$%!^&*'), code='password_no_symbol',)

    def get_help_text(self):
        return _('Your password must contain at least 1 special character: @#$%!^&*')
