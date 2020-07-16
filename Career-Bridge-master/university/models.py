from django.db import models

# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=100)
    admin = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    logo = models.FileField(default = 'logos\defaultdp.jpg', upload_to='logos', blank=True, null=True)
    ranking = models.FloatField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class Bidding(models.Model):
    bidder = models.ForeignKey("university.University", on_delete=models.CASCADE)
    project = models.ForeignKey("project.Project", on_delete=models.CASCADE)
    performed_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    bidding_price = models.IntegerField()
    revisions = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.bidder} ==> {self.project} ==> {self.bidding_price}"

class Service(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.university} --> {self.service_name}'

