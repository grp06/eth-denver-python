from django.db import models
from django.db.models.deletion import CASCADE
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import pre_save
import json
from llama_index import GPTSimpleVectorIndex, Document

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


@receiver(pre_save, sender=Company)
def my_function(sender, instance, **kwargs):
    # Check if the instance has been saved before
    if instance.pk:
        # Retrieve the original instance from the database
        original_instance = Company.objects.get(pk=instance.pk)
        # Check if the field you want to update has changed
        if original_instance.sdk_doc != instance.sdk_doc:
            # Perform your updates using the update() method
            sdk_text = text = instance.sdk_doc.decode('utf-8')
            document = Document(text=sdk_text)
            index = GPTSimpleVectorIndex([])
            index.insert(document)
            index_str = index.save_to_string()
            instance.index = json.dumps({'index': index_str})
            Company.objects.filter(pk=instance.pk).update(sdk_doc=instance.sdk_doc)
    else:
        # The instance is new, so just save it normally
        instance.save()



class Query(models.Model):
    query = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    company = models.ForeignKey("Company", on_delete=CASCADE)

    def __str__(self):
        return(str(self.company) + " timestamp:" + str(self.timestamp))

    class Meta:
        verbose_name_plural = "Queries"


