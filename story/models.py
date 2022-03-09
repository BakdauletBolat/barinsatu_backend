from django.db import models
from authentication.models import User
# Create your models here.


class Story(models.Model):

    video = models.FileField(upload_to='Stories/')
    thumb = models.ImageField(upload_to='StoriesThumbs/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    views = models.BigIntegerField(default=0)
    is_archive = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='stories')

    def __str__(self) -> str:
        
        return f"{self.id}"

    class Meta:
        verbose_name = 'Историй'


class StoryLike(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='story_likes')
    story = models.ForeignKey(Story,on_delete=models.CASCADE,related_name='story_likes')
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    isLiked = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Лайк для Историй'
        verbose_name_plural = 'Лайк для Историй'
        constraints = [
            models.UniqueConstraint(fields=['user', 'story'], name="unique_like_story"),
        ]
        


class StoryComments(models.Model):

    text = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='story_comments')
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    story = models.ForeignKey(Story,on_delete=models.CASCADE,related_name='story_comments')

    class Meta:

        verbose_name = 'Коммент для Историй'
        verbose_name_plural = 'Комменты для Историй'
