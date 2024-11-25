from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from short_url import UrlEncoder

encoder = UrlEncoder(alphabet='mh8EfAByDnXqHFajGb9eT3r24utP7gvJdw6ZK5zMkURsWCYScVNpx')


class Wishlist(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='wishlists_images', null=True, blank=True)
    event_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    slug_url = models.CharField(max_length=255, blank=True, unique=True)


    def __str__(self) -> str:
        return f'{self.title} ({self.user})'


    class Meta:
        verbose_name = 'вишлист'
        verbose_name_plural = 'вишлисты'


@receiver(post_save, sender=Wishlist)
def generate_slug(sender, instance, created, **kwargs):
    if created and not instance.slug_url:
        instance.slug_url = encoder.encode_url(instance.pk)
        instance.save(update_fields=['slug_url'])



class Present(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField(max_length=40, null=True, blank=True)
    image = models.ImageField(upload_to='presents_images', null=True, blank=True)
    link = models.URLField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    reserved_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reserved_presents', default=None, null=True, blank=True)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='presents')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.title


    class Meta:
        verbose_name = 'подарок'
        verbose_name_plural = 'подарки'
