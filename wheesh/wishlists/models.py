from django.db import models


class Wishlist(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='wishlists_images', null=True, blank=True)
    event_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.title} ({self.user})'


    class Meta:
        verbose_name = 'вишлист'
        verbose_name_plural = 'вишлисты'


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
