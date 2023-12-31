from django.db import models
from django.utils.safestring import mark_safe
from django_cleanup.signals import cleanup_pre_delete
from sorl.thumbnail import delete, get_thumbnail
from tinymce.models import HTMLField

from user.models import CustomUser


class Recipe(models.Model):
    image = models.ImageField(
        upload_to='uploads/preview/%Y/%m',
        null=True,
    )
    title = models.CharField(
        max_length=150,
        unique=True,
    )
    description = HTMLField()
    instructions = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def get_img(self):
        return get_thumbnail(
            self.photo,
            '300x300',
            crop='center',
            quality=51,
        )

    def img_tmb(self):
        if self.photo:
            return mark_safe(
                f'<img src="{self.get_img.url}">'
            )
        return 'no img'

    img_tmb.short_description = 'image'
    img_tmb.allow_tags = True

    def sorl_delete(**kwargs):
        delete(kwargs['file'])

    cleanup_pre_delete.connect(sorl_delete)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_on']
        verbose_name = "рецепт"
        verbose_name_plural = "рецепты"

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="пользователь",
		)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='рецепт',
    )
    show = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"
