from django.db import models
import datetime
from django.utils import timezone


class Blogs(models.Model):
    blog_header = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.blog_header

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Content(models.Model):
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    content_text = models.CharField(max_length=3000)
# Likes?    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.content_text
