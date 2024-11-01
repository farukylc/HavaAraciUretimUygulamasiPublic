from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Departman(models.Model):
    DEPARTMENT_CHOICES = [
    ('Kanat', 'Kanat Ekibi'),
    ('Gövde', 'Gövde Ekibi'),
    ('Kuyruk', 'Kuyruk Ekibi'),
    ('Aviyonik', 'Aviyonik Ekibi'),
    ('Montaj', 'Montaj Ekibi')
]
    name = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


@receiver(post_migrate)
def create_default_departments(sender, **kwargs):
    if sender.name == 'api':
        for dept_name, display_name in Departman.DEPARTMENT_CHOICES:
            Departman.objects.get_or_create(name=dept_name)


class Person(User):

     name = models.CharField(max_length=100)
     department = models.ForeignKey(Departman, on_delete=models.CASCADE, related_name='personels')

     def __str__(self):
        return f"{self.username} - {self.department}"



class IHAPiece(models.Model):
    PART_TYPE_CHOICES = [
        ('Kanat', 'Kanat'), 
        ('Gövde', 'Gövde'), 
        ('Kuyruk', 'Kuyruk'), 
        ('Aviyonik', 'Avionik'), 
    ]

    MODEL_TYPE_CHOICES = [
        ('TB2', 'TB2'),
        ('TB3', 'TB3'),
        ('AKINCI', 'AKINCI'),
        ('KIZILELMA', 'KIZILELMA'),
    ]

    piece_type = models.CharField(max_length=100, choices=PART_TYPE_CHOICES)
    model_type = models.CharField(max_length=50, choices=MODEL_TYPE_CHOICES)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.piece_type} ({self.model_type})"
    

@receiver(post_migrate)
def create_default_departments(sender, **kwargs):
    if sender.name == 'api':
        for dept_name, display_name in Departman.DEPARTMENT_CHOICES:
            Departman.objects.get_or_create(name=dept_name, defaults={'display_name': display_name})


class Airplane(models.Model):
    MODEL_TYPE_CHOICES = [
        ('TB2', 'TB2'),
        ('TB3', 'TB3'),
        ('AKINCI', 'AKINCI'),
        ('KIZILELMA', 'KIZILELMA'),
    ]

    model_type = models.CharField(max_length=50, choices=MODEL_TYPE_CHOICES)
    pieces = models.ManyToManyField(IHAPiece, through='AirplanePiece')
    
    def __str__(self):
        return f"Airplane Model: {self.model_type}"


class AirplanePiece(models.Model):
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    piece = models.ForeignKey(IHAPiece, on_delete=models.CASCADE)

    def clean(self):
        # Uçağın model_type'ı ile parçanın model_type'ı uyumlu olmalı
        if self.airplane.model_type != self.piece.model_type:
            raise ValidationError("Parçanın model türü uçağın model türü ile eşleşmiyor.")

    def save(self, *args, **kwargs):
        # Save işleminden önce temizleme kontrolü yapılır
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.airplane} - {self.piece}"
