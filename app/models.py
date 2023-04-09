from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Code(models.Model):
    user = models.ForeignKey(User, related_name='code', on_delete=models.DO_NOTHING)
    prompt = models.TextField(max_length=5000)
    response = models.TextField(max_length=5000)
    lang = models.CharField(max_length=50)

    def __str__(self):
        return self.prompt