from django import template
register = template.Library()

from benchmark.models import Alert

@register.simple_tag
def active_alerts_count(user):
    """
    function to return the active alerts in model
    this template tag is required because the alert_count
    is used in profile/base.html in badge of the alert nav.
    so, The alternative is to provide the alert_count in the
    context of all the templates thaty inherit the profile/base.html

    @returns (int) -> Number of active alerts for a user
    """
    ac = Alert.objects.filter(
        user=user
    ).filter(
        _pre_active=True
    ).count()
    if ac:
        return ac
    else:
        return ''
