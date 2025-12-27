from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from student.models import Student

# Simple profile storage for the site administrator (and future users)
class AdminProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
	image = models.ImageField(upload_to='admins/', blank=True, null=True)
	mobile = models.CharField(max_length=20, blank=True)
	address = models.TextField(blank=True)
	joining_date = models.DateField(blank=True, null=True)

	def __str__(self):
		return f"Profile for {self.user.username}"


@receiver(post_save, sender=User)
def create_admin_profile(sender, instance, created, **kwargs):
	if created:
		AdminProfile.objects.create(user=instance)

class Fees(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="school_fees")																																																																				
    class_name = models.CharField(max_length=100)
    amount = models.IntegerField()
    status = models.CharField(max_length=20)
    date = models.DateField()
