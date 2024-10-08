from django.db import models
from django.contrib.auth.models import User

class Quote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quote = models.TextField()
    author = models.CharField(max_length=255, default=None)
   