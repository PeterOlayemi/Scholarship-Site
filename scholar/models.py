from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.

class Status(models.Model):
    name = models.CharField(max_length=99)
    info = models.CharField(max_length=199, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Application(models.Model):
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, blank=True, null=True)
    scholarship = models.ForeignKey('Scholarship', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    full_name = models.CharField(max_length=99)
    email = models.EmailField()
    date_of_birth = models.DateField()
    matric_no = models.CharField(max_length=49)
    school = models.CharField(max_length=199)
    level = models.CharField(max_length=3)
    department = models.CharField(max_length=199)
    cgpa = models.CharField(max_length=4)
    picture = models.ImageField(upload_to='profile_pic/')
    admission_letter = models.FileField(upload_to='admission_letter/', validators=[FileExtensionValidator(allowed_extensions=['pdf','doc','docx'])])
    result = models.FileField(upload_to='result/', validators=[FileExtensionValidator(allowed_extensions=['pdf','doc','docx'])])
    national_identification = models.FileField(upload_to='national_id/', validators=[FileExtensionValidator(allowed_extensions=['pdf','doc','docx'])])
    id_card = models.FileField(upload_to='school_id/', validators=[FileExtensionValidator(allowed_extensions=['pdf','doc','docx'])])
    
    def __str__(self):
        return f'{self.user}'

class Scholarship(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=99)
    description = models.TextField()
    closing_date = models.DateField()

    @property
    def available(self):
        if self.closing_date > timezone.now().date():
            return True
        else:
            return False
    
    def __str__(self):
        return self.name
