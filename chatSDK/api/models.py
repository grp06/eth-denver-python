from django.db import models
from django.db.models.deletion import CASCADE
from datetime import datetime

# Create your models here.

## Company
class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sdk_doc = models.FileField(null=True)
    index = models.JSONField(null=True, blank=True)
    prizes = models.JSONField(null=True, blank=True)

    def __str__(self):
        return(str(self.name))

    class Meta:
        verbose_name_plural = "Companies"

#https://stackoverflow.com/questions/1197674/actions-triggered-by-field-change-in-django
    def set_state(self, newstate):
        if self.state != newstate:
            oldstate = self.state
            self.state = newstate
            if oldstate == 'S' and newstate == 'A':
                self.started = datetime.now()
                # create units, etc.

class Query(models.Model):
    query = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    company = models.ForeignKey("Company", on_delete=CASCADE)

    def __str__(self):
        return(str(self.company) + " timestamp:" + str(self.timestamp))

    class Meta:
        verbose_name_plural = "Queries"


