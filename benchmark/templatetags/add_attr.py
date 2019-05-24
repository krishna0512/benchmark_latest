from django import template
register = template.Library()

@register.filter(name='add_attr')
def add_attr(field, css):
    attrs = {}
    definition = css.split(',')
    definition = [i.strip() for i in definition]

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            key, value = d.split(': ')
            attrs[key] = value
    return field.as_widget(attrs=attrs)
