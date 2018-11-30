from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    image = models.ImageField(upload_to="avatars", default="avatars/anonymous.png", null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    stripe_id = models.CharField(max_length=80, blank=True, null=True)
    card_ending = models.CharField(max_length=4, blank=True, null=True)
    subscription_id = models.CharField(max_length=80, blank=True, null=True)
    
    def __str__(self):
        return "{0} {1}".format(self.user.first_name, self.user.last_name)
