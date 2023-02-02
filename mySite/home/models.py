from django.db import models

# Create your models here.
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    email =models.CharField(max_length=30)
    phno = models.CharField(max_length=10)
    address =models.CharField(max_length=200)
    comment = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name


