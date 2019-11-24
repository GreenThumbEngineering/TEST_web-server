from datetime import datetime
from django import template

register = template.Library()



@register.filter(name='fromunix')
def fromunix(value):
    return datetime.fromtimestamp(int(value)).strftime("%d.%m.%Y %H:%M:%S")
	

register.filter('fromunix', fromunix)