from django.db import models
from django.conf import settings
# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=100)
    admin = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    logo = models.FileField(default = 'logos\defaultdp.jpg', upload_to='logos', blank=True, null=True)
    # projects = models.ForeignKey("project.Project", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name