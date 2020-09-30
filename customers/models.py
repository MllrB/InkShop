from django.db import models
from django.db.models import UniqueConstraint
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount

from jsonfield import JSONField
from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    User profile model for maintaining user data
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=254, null=True, blank=True)
    profile_pic_url = models.CharField(max_length=254, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)
    email = models.EmailField(default='placeholder@mllrb.com')
    favourites = JSONField(null=True, blank=True)
    default_phone_number = models.CharField(
        max_length=254, null=True, blank=True)
    billing_address_line1 = models.CharField(
        max_length=254, null=True, blank=True)
    billing_address_line2 = models.CharField(
        max_length=254, null=True, blank=True)
    billing_town_or_city = models.CharField(
        max_length=254, null=True, blank=True)
    billing_county = models.CharField(max_length=254, null=True, blank=True)
    billing_post_code = models.CharField(max_length=254, null=True, blank=True)
    billing_country = CountryField(
        blank_label="Select Country", null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=SocialAccount)
def create_user_from_social_account(sender, instance, created, **kwargs):
    """
    Create a user profile from a social account login
    """
    if created:
        if instance.provider == 'google':
            email = instance.extra_data['email']
            full_name = instance.extra_data['name']
            profile_pic_url = instance.extra_data['picture']
            user = get_object_or_404(User, email=email)
            user_profile = get_object_or_404(UserProfile, user=user)
            user_profile.email = email
            user_profile.full_name = full_name
            user_profile.profile_pic_url = profile_pic_url
            user_profile.save()


@receiver(post_save, sender=User)
def create_user_from_signup(sender, instance, created, **kwargs):
    """
    Create a user profile from a social account login
    """
    if created:
        email = instance.email.split('@')
        instance.username = email[0]
        try:
            username_exists = get_object_or_404(
                User, username=instance.username)
            email_tail = email[1].split('.')
            new_username = f'{email[0]}_{email_tail[0]}'
            instance.username = new_username
            instance.save()
            UserProfile.objects.create(user=instance)
        except:
            instance.save()
            UserProfile.objects.create(user=instance)


class DeliveryAddress(models.Model):
    """
    Delivery details model allowing users to store multiple delivery addresses
    """
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="delivery_address")
    address_ref = models.CharField(max_length=60)
    contact_name = models.CharField(max_length=254, null=True, blank=True)
    contact_phone_number = models.CharField(
        max_length=20, null=True, blank=True)
    address_line1 = models.CharField(max_length=254, null=True, blank=True)
    address_line2 = models.CharField(max_length=254, null=True, blank=True)
    town_or_city = models.CharField(max_length=254, null=True, blank=True)
    county = models.CharField(max_length=254, null=True, blank=True)
    post_code = models.CharField(max_length=254, null=True, blank=True)
    country = CountryField(blank_label="Select Country", null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'address_ref'], name='unique address')
        ]

    def __str__(self):
        return self.address_ref
