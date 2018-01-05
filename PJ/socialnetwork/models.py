from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.DO_NOTHING, to_field='username')
    content = models.CharField(max_length=160)
    date = models.CharField(max_length=50)

    def __unicode__(self):
        return 'id=' + str(self.id) + ',content="' + self.content + '"'

class Profile(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.DO_NOTHING, to_field='username')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.CharField(blank=True, max_length=3)
    short_bio = models.CharField(blank=True, max_length=430)
    picture = models.FileField(blank=True, upload_to="images")
    content_type = models.CharField(blank=True, max_length=50)
    follows = ArrayField(models.CharField(blank=True, max_length=20), default=list, blank=True) 

    def __unicode__(self):
        return 'Profile(id=' + str(self.id) +')'

class Comment(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.DO_NOTHING, to_field='username')
    time = models.CharField(max_length=50)
    content = models.CharField(max_length=100)
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)

    def __unicode__(self):
        return 'Comment(id=' + str(self.id) +')'
