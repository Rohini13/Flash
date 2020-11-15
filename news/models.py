from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class CategoryString(models.Model):
    category_obj = models.CharField(max_length=50, blank=True)


class NewspaperString(models.Model):
    newspaper_obj = models.CharField(max_length=50, blank=True)


class Article(models.Model):
    img = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=1000, blank=True)
    content = models.CharField(max_length=10000, blank=True)
    time = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=100, blank=True)


class FlashUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(CategoryString)
    newspapers = models.ManyToManyField(NewspaperString)
    bookmarked_articles = models.ManyToManyField(Article)

    # @receiver(post_save, sender=User)
    # def create_user_flashuser(sender, instance, created, **kwargs):
    #     if created:
    #         FlashUser.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_student(sender, instance, **kwargs):
    #     instance.flashuser.save()


