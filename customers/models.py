from django.db import models
from django.db.models import UniqueConstraint
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
    # full_name = models.CharField(max_length=254, null=True, blank=True)
    # profile_pic_url = models.CharField(max_length=254, null=True, blank=True)
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


# @receiver(post_save, sender=User)
# def create_user_from_social_account(sender, instance, created, **kwargs):
#     """
#     Create a user profile from a social account login
#     """
#     if created:
#         UserProfile.objects.create(user=instance)

#     instance.userprofile.save()


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