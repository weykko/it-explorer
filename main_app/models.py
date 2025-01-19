from django.db import models

# Create your models here.

class Statistics(models.Model):
    title = models.CharField(max_length=255)
    table_data = models.TextField()  # HTML
    graph = models.ImageField(upload_to='graphs/', null=True, blank=True)

    def __str__(self):
        return self.title