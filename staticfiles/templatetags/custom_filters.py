

from django import template
from ..models import Post, Article, Updates

register = template.Library()

@register.filter
def instance_of(obj, class_name):
    if class_name == 'blog.post' and isinstance(obj, Post):
        return True
    if class_name == 'blog.article' and isinstance(obj, Article):
        return True
    if class_name == 'blog.update' and isinstance(obj, Updates):
        return True
    return False
