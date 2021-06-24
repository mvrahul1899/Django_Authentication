from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#
class userProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True)
    class Meta:
        verbose_name = 'userProfileInfo'
        verbose_name_plural = 'userProfileInfos'
    def __str__(self):
        return self.user.username