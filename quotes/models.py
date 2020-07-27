from django.db import models

# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=10)

    def __str__(self):
        return self.ticker

class Youtube(models.Model):
    PublishedAt = models.DateTimeField()
    titel = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    thumbnailurl = models.URLField(blank=True)
