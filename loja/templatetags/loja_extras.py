from django import template

register = template.Library()

@register.filter
def string_para_titulo(value: str):
    if "_" in value:
        return value.replace("_", " ").capitalize()

