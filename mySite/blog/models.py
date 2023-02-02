from django.db import models
from django.contrib.auth.models import auth, User
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    slug = models.CharField(max_length=300, default="")
    content = models.TextField(max_length=5000)
    author = models.CharField(max_length=30)
    time = models.DateTimeField(blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title + "   auth: " + self.author

class Comments(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:12] + "... by " + str(self.user)
