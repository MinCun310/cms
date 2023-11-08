import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    def validate(self, password, user=None):
        print("Hello")
        if not re.search(r"[a-z]", password):
            raise ValidationError(
                _("Password must contain at least one lowercase letter ")
            )
        elif not re.search(r"[A-Z]", password):
            raise ValidationError(
                _("Password must contain at least one uppercase letter ")
            )
        elif not re.search(r"\d", password):
            raise ValidationError(_("Password must contain at least one number"))
        elif not re.search(r"[@!$%&*?]", password):
            raise ValidationError(
                _("Password must contain at least one special character (@!$%&*?)")
            )

    def get_help_text(self):
        return _(
            "Password must contain at least one lowercase, one uppercase, one number, one special character "
        )
