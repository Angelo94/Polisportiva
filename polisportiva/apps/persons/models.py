from django.db import models
from django.utils.translation import ugettext_lazy as _

SPORT_TYPES = [
    ("pallavolo", "Pallavolo"),
    ("basket", "Basket"),
    ("badminton", "Badminton"),
]


class Athlete(models.Model):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    sport_type = models.CharField(_('sport type'), max_length=50, choices=SPORT_TYPES, blank=True)

    class Meta:
        verbose_name = _('athlete')
        verbose_name_plural = _('athletes')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()