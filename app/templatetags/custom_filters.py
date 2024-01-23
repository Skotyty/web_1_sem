from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='get_avatar')
def get_avatar(avatar):
    if not avatar or not avatar.url.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        return settings.STATIC_URL + 'img/no_avatar.jpg'
    return avatar.url
