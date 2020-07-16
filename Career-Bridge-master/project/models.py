from django.db import models
from datetime import datetime

# Create your models here.


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    project_description = models.TextField()
    company_deal = models.BooleanField(default=False)
    university_deal = models.BooleanField(default=False)
    developed_by = models.ForeignKey("university.University", on_delete=models.CASCADE, blank=True, null=True)
    developed_for = models.ForeignKey("company.Company", on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    bidding_start = models.DateTimeField(null=False)
    bidding_end = models.DateTimeField(null=False)
    company_mou = models.FileField(upload_to='CompnyMOUs', null=True, blank=True)
    company_remarks = models.TextField(null=True, blank=True)
    university_mou = models.FileField(upload_to='UniversityMOUs', null=True, blank=True)
    university_remarks = models.TextField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.project_name

    @property
    def is_bidding_started(self):        
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print(self.bidding_start.strftime('%Y-%m-%d %H:%M:%S'))
        return datetime.today().strftime('%Y-%m-%d %H:%M:%S') > self.bidding_start.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def is_bidding_end(self):
        return datetime.today().strftime('%Y-%m-%d %H:%M:%S') >= self.bidding_end.strftime('%Y-%m-%d %H:%M:%S')

    def is_bidding_ended(self):
        return datetime.today().strftime('%Y-%m-%d %H:%M:%S') >= self.bidding_end.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def is_rated(self):
        rating = Rating.objects.filter(project=self)
        if rating:
            return True
        else:
            return False

    @property
    def get_rating(self):
        rat = Rating.objects.filter(project=self).first()
        return rat.rating


class Milestones(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Rating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    q1 = models.IntegerField(default=0)
    q2 = models.IntegerField(default=0)
    q3 = models.IntegerField(default=0)
    q4 = models.IntegerField(default=0)
    feedback = models.TextField()
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.feedback
