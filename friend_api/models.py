from django.db import models
from authentication.models import CustomUser

# Create your models here.
class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_user')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.from_user.username + " " + self.to_user.username
    
