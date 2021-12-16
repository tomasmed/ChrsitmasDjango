from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
#from ads.models import Fav,Comment
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from gifts.utils import get_link_info


from django.db.models.signals import post_save
from django.dispatch import receiver


class Member(models.Model):
    name = models.CharField(max_length=200,validators=[MinLengthValidator(2, "Member name must be greater than 2 characters")])
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)

    # Shows up in the admin list
    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user=instance)
    instance.member.save()




    #Family = models.ForeignKey(Family, on_delete=models.CASCADE)

# class Family(models.Model) :
#     name = models.CharField(max_length=200,validators=[MinLengthValidator(2, "Family name must be greater than 2 characters")])
#     member = models.ManyToManyField(settings.AUTH_USER_MODEL,through='Member', related_name='family_member')

#     def __str__(self) :
#         return self.name


class Gift(models.Model) :
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    link = models.URLField(max_length = 256, null = True)
    text = models.TextField()
    owner = models.ForeignKey(Member, on_delete=models.CASCADE)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='ads.Comment', related_name='gift_comments_owned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    picture = models.BinaryField(null=True, editable=True)
    purchased = models.IntegerField(null = True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')

    #Tags
    # https://django-taggit.readthedocs.io/en/latest/api.html#TaggableManager
    tags = TaggableManager(blank=True)

    # Favorites
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='ads.Fav', related_name='favorite_gifts')


    # Shows up in the admin list
    def __str__(self):
        return self.title





# class Comment(models.Model) :
#     text = models.TextField(
#         validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
#     )

#     ad = models.ForeignKey(Gift, on_delete=models.CASCADE)
#     owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     # Shows up in the admin list
#     def __str__(self):
#         if len(self.text) < 15 : return self.text
#         return self.text[:11] + ' ...'

# class Gift_Fav(models.Model) :
#     gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

#     # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
#     class Meta:
#         unique_together = ('gift', 'user')

#     def __str__(self) :
#         return '%s likes %s'%(self.user.username, self.ad.title[:10])