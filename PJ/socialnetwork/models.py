from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=160)
    date = models.CharField(max_length=50)

    def __unicode__(self):
        return 'id=' + str(self.id) + ',content="' + self.content + '"'
