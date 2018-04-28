from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    nickname = models.CharField(max_length=32, blank=True)
    sex         = models.CharField(max_length=10, blank=True)
    age         = models.CharField(max_length=20, blank=True)
    head_image  = models.CharField(max_length=100, blank=True)
    v           = models.CharField(max_length=16, blank=True)
    introduce   = models.CharField(max_length=600, blank=True)
    alias       = models.CharField(max_length=60, blank=True)
    attr        = models.CharField(max_length=128, blank=True)
    comment_limit = models.DateTimeField(null=True, blank=True)
    points      = models.IntegerField(null=True, blank=True,default=0)
    auto_country = models.CharField(max_length=32, blank=True)
    auto_province = models.CharField(max_length=32, blank=True)
    auto_city   = models.CharField(max_length=32, blank=True)
    auto_district = models.CharField(max_length=32, blank=True)
    be_used_points   = models.IntegerField(null=True, blank=True,default=0)
    user = models.OneToOneField(User)
    currency      = models.IntegerField(null=True, blank=True,default=0)  # 货币
    give_currency = models.IntegerField(null=True, blank=True,default=0)

    class Meta:
        db_table = 'user_profile'

