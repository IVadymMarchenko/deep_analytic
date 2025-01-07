from django.db import models
from users.models import CustomUser
# Create your models here.



class MyFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='files')

    class Meta:
        db_table = 'myfile'
        verbose_name = 'file'
        verbose_name_plural = 'files'

    def __str__(self):
        return f'{self.file.name} uploaded by {self.user.email}'
