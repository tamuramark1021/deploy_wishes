from django.db import models
from login_app.models import User

# Create your models here.
class WishManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['item_name']) < 3:
            errors['item_name'] = "Item name must be at least 3 characters long"
        if len(postData['item_description']) < 3:
            errors['item_description'] = "Item description must be at least 3 characters long"
        return errors

class Wish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishes')
    item = models.CharField(max_length=100)
    desc = models.TextField()
    is_granted = models.BooleanField()
    granted_date = models.DateTimeField(null=True, blank=True)
    # likes = models.IntegerField()   # place holder for black belt options
    likes = models.ManyToManyField(User, related_name="wish_likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()
        
