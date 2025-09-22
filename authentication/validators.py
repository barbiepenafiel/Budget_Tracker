import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ComplexPasswordValidator:
    """
    Validate that the password contains at least:
    - 1 uppercase letter
    - 1 lowercase letter  
    - 1 digit
    - 1 special character
    - Minimum 8 characters
    """
    
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("Password must be at least 8 characters long."),
                code='password_too_short',
            )
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("Password must contain at least one uppercase letter."),
                code='password_no_upper',
            )
        
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("Password must contain at least one lowercase letter."),
                code='password_no_lower',
            )
        
        if not re.search(r'\d', password):
            raise ValidationError(
                _("Password must contain at least one digit."),
                code='password_no_digit',
            )
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                _("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 8 characters including "
            "uppercase letters, lowercase letters, numbers, and special characters."
        )

class UsernameValidator:
    """
    Validate that the username is at least 6 characters long
    """
    
    def validate(self, username):
        if len(username) < 6:
            raise ValidationError(
                _("Username must be at least 6 characters long."),
                code='username_too_short',
            )
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError(
                _("Username can only contain letters, numbers, and underscores."),
                code='username_invalid_chars',
            )
    
    def get_help_text(self):
        return _(
            "Username must be at least 6 characters long and contain only "
            "letters, numbers, and underscores."
        )
