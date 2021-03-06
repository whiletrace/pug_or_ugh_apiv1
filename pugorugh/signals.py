from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from pugorugh.models import Dog, UserDog

user = get_user_model()


@receiver(post_save, sender=user)
def userdog_receiver(sender, instance, created, **kwargs):
    """Custom signal receiver when a User is created

        if a user object is created model.UserDog objects related to user
        are bulk created from all available model.Dog objects database
    """
    if created:
        dogs = Dog.objects.all()
        UserDog.objects.bulk_create(
            [UserDog(user=instance, dog=d) for d in dogs])
