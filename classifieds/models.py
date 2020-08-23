from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField
from unidecode import unidecode


class Profile(models.Model):
    """Model definition for Profile."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    phone = models.CharField(
        _('Contact phone'), max_length=30, null=True, blank=True)

    class Meta:
        """Meta definition for Profile."""

        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        """Unicode representation of Profile."""
        return self.user.username


# Post Signal for Profile Creation
@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Area(models.Model):
    slug = models.SlugField(blank=True, null=True,)
    title = models.CharField(_('title'), max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('area')
        verbose_name_plural = _('areas')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super(Area, self).save(*args, **kwargs)


class Section(models.Model):
    """Model definition for Profile."""
    title = models.CharField(_('title'), max_length=100)

    class Meta:
        """Meta definition for Profile."""

        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __str__(self):
        """Unicode representation of Section."""
        return self.title


class Group(models.Model):
    """Model definition for Group."""
    slug = models.SlugField(blank=True, null=True)
    title = models.CharField(_('title'), max_length=100)
    section = models.ForeignKey('Section', verbose_name=_(
        'section'), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.section.title} - {self.title}'

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        ordering = ['section__title', 'title', ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super(Group, self).save(*args, **kwargs)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(is_active=True)


class Item(models.Model):
    """Model definition for Item."""
    slug = models.SlugField(blank=True, null=True, max_length=100)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    group = models.ForeignKey(Group, verbose_name=_(
        'group'), on_delete=models.CASCADE)
    area = models.ForeignKey(Area, verbose_name=_(
        'area'), on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    is_active = models.BooleanField(_('active'), default=True, db_index=True)
    updated = models.DateTimeField(_('updated'), auto_now=True, db_index=True)
    posted = models.DateTimeField(_('posted'), auto_now_add=True)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        if not self.is_active:
            active_status = _('in active')
            return f'[{active_status}] {self.title}'
        else:
            return self.title

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('-updated', )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super(Item, self).save(*args, **kwargs)


class Image(models.Model):
    item = models.ForeignKey(
        Item, related_name='images', on_delete=models.CASCADE)
    file = ImageField(_('image'), upload_to='images')
