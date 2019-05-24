from zipfile import ZipFile

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from benchmark.models import Profile, Dataset

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Dataset)
def update_nimages_field(sender, instance, **kwargs):
    """
    using signals to update the nimages field after the Dataset is saved.
    call the save() function of this Dataset instance iff
    number of image files in zipfile is non-zero

    TODO: count only the files in zip which are images and delete/discard all non-images
          files from the zip and save again
    TODO: Further refine the condition in which this update_nimages_field calls
          the save function of the instance
    """
    # using -1 because namelist() also gives the name of the zip as a seperate file
    # e.g. namelist() = ['zipfilename/', '1.jpeg', '2.jpeg', ... , 'nimg.jpeg']
    if instance.zipfile and not instance.nimages:
        nimg = len(ZipFile(instance.zipfile.path).namelist())-1
        if nimg > 0:
            instance.nimages = nimg
            instance.save()

@receiver(pre_delete, sender=Dataset)
def delete_dataset_zipfile(sender, instance, **kwargs):
    """
    Deleting the dataset zip file and groud truth
    from the filesystem before successfully deleting model instance.
    """
    if instance.zipfile:
        instance.zipfile.delete(False)
    if instance.gtfile:
        instance.gtfile.delete(False)
