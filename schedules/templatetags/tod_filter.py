from django import template

register = template.Library()

@register.filter(name='tod_filter')
def tod_filter(values, tod):
    if 'id' in tod:
        return filter(lambda x: x.timeofday.id == tod['id'] if x.timeofday else False, values)
    return None