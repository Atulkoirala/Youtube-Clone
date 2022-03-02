from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    path = models.FileField(upload_to='video')
    added_date = models.DateTimeField(default=timezone.now)
    cat = models.ForeignKey(Category,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    like = models.ManyToManyField(User,blank=True,related_name='vlikes')

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('cat_id',)

    def get_absolute_url(self):
        return reverse('vdodetail', kwargs={'pk': self.pk})
    
class Comment(models.Model):
    text = models.TextField()
    img = models.ImageField(upload_to='comment', blank=True)
    added_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    video = models.ForeignKey(Video,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    like = models.ManyToManyField(User,blank=True,related_name='clikes')

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-added_date',)
    
    def get_absolute_url(self):
        return reverse('vdodetail', kwargs={'pk': self.pk})
    
    @property
    def is_reply(self):
        if self.reply is not None:
            return False
        return True


class Profile(models.Model):
    A =( 
    ("Male", "Male"), 
    ("Female", "Female"), 
    ("Others", "Others"), 
)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=False)
    middle_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=False)
    Profile_Pic = models.ImageField(default='default.jpg',upload_to='profile_pic')
    Cover_pic = models.ImageField(default='default1.jpg',upload_to='cover_pic')
    Gender = models.CharField(max_length=200, blank=False, choices=A)
    date_added = models.DateField(default=timezone.now,blank=False)
    BIO = models.CharField(max_length=500)
    Contact_Number = PhoneNumberField(blank=False)
    Country = models.CharField(max_length=200, blank=False)
    Address = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return f'{self.user.username} Profile'

class Wishlist(models.Model):
    video_id = models.ForeignKey(Video,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)


