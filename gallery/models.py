from django.db import models
import uuid
from django.db.models.signals import post_save

# Create your models here.



class Board(models.Model):
    id_pinterest = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, default="")
    active = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return self.title

class Section(models.Model):
    id_pinterest = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.CharField(max_length=200, default="")
    title = models.CharField(max_length=200)
    active = models.BooleanField(blank=False, default=False)
    board = models.ForeignKey(to=Board, on_delete=models.CASCADE)

    def title_custom_split(self):
        return self.title.replace('[ ', '').split(' ] ')

    def slug_custom_split(self):
        return self.title.replace('[ ', '').split(' ] ')[0].replace(' ', '-').lower()

    def __str__(self):
        return self.title


class Pin(models.Model):
    id_pinterest = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    section = models.ForeignKey(to=Section, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=200)
    small_image_url = models.CharField(max_length=200)
    color = models.CharField(max_length=8, default="#ffffff")

    def __str__(self):
        return self.title


class SectionDescription(models.Model):
    description = models.TextField(max_length=1500, blank=True, default="")
    section = models.OneToOneField('Section', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        try:
            return self.section.title
        except AttributeError:
            return self.description[0:100]
