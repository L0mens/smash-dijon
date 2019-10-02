from django import template

register = template.Library()

@register.filter
def get_key(mydict, key):
    return mydict[key]

@register.simple_tag
def divide(nom , denom):
    try:
       return int(nom)/int(denom)
    except ValueError:
       raise template.TemplateSyntaxError('Les arguments doivent nécessairement être des entiers supérieurs à 0')

@register.simple_tag
def divide_percent(nom , denom):
    try:
       return int((int(nom)/int(denom))*100)
    except ValueError:
       raise template.TemplateSyntaxError('Les arguments doivent nécessairement être des entiers supérieurs à 0')
