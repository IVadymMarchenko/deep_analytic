from django.db import models

# Create your models here.


class Chart(models.Model):
    chart_image = models.ImageField(upload_to='charts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title