from django.db import models
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill,Transpose
from taggit.managers import TaggableManager
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse

# Create your models here.
# class User(auth.models.User, auth.models.PermissionsMixin):
#     def _str_(self):
#         return f'{self.username}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25,blank=True)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    image_thumbnail_user = ImageSpecField(source='image',
                                      processors=[Transpose(),ResizeToFill(170, 170)],
                                      format='JPEG',
                                      options={'quality': 100})

    description = models.CharField(max_length=100, blank=True)
    follows = models.ManyToManyField(User,related_name="follows",blank=True)
    followers = models.ManyToManyField(User,related_name="followers",blank=True)
    def _str_(self):
        return f"{self.user.username}'s Profile"

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=True,unique=True,max_length=111)
    content =  models.TextField()
    image =  models.ImageField(upload_to='post_images')
    image_thumbnail = ImageSpecField(source='image',
                                      processors=[
                                        Transpose(),
                                        ResizeToFill(1000, 500)
                                        ],
                                      format='JPEG',
                                      options={'quality': 70})

    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes',blank=True)
    tagged_users = models.ManyToManyField(User, related_name='tagged_users',blank=True)

    @property
    def total_likes(self):
        return self.likes.count()

    def _str_(self):
        return self.title


    def get_absolute_url(self):
        return reverse('accounts:post-detail', kwargs={'slug': self.slug})

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return self.comment

class Notification(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE, related_name='receiver')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    action = models.CharField(max_length=50, blank=True)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

@receiver(post_save,sender=Post)
def post_mentioned_notify(sender, instance, *args, **kwargs):
    sender = User.objects.get(pk=instance.author.pk)
    post = Post.objects.get(pk=instance.pk)
    string = instance.content
    poss_users = [i  for i in string.split() if i.startswith("@")]
    poss_users_list = []
    for user in poss_users:
        poss_users_list.append(user[1:])

    for username in poss_users_list:
        try:
            get_user = User.objects.get(username=username)
        except:
            continue
        if get_user in instance.tagged_users.all():
            continue
        elif get_user == sender:
            continue
        else:
            instance.tagged_users.add(get_user)
            notify = Notification.objects.create(sender=sender,receiver=get_user,post=post,action="mentioned you in post")


@receiver(post_save,sender=Comment)
def comment_added_notify(sender, instance, *args, **kwargs):
    sender = User.objects.get(pk=instance.author.pk)
    post = Post.objects.get(pk=instance.post.pk)
    receiver = User.objects.get(pk=instance.post.author.pk)
    if receiver == sender:
        pass
    else:
        notify = Notification.objects.create(sender=sender,receiver=receiver,post=post,action="commented on your post")


@receiver(pre_save,sender=Post)
def sulg_generator(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title+" "+str(sender.objects.count()))
