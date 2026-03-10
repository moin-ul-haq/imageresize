from django.db import models

# Create your models here.
class ImageTask(models.Model):
    image=models.ImageField(upload_to='uploads/')
    processed_image=models.ImageField(upload_to='processed/',null=True,blank=True)
    status=models.CharField(max_length=10,default='pending')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)+ '-----' + self.status