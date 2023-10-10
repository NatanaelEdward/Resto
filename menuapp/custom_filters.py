from django import template

register = template.Library()

@register.filter
def dict_lookup(dictionary, key):
    return dictionary.get(key, "")

@register.filter
def get_item(value, index):
    try:
        return value[index]
    except (IndexError, KeyError):
        return ""
    
@register.filter
def related_penjualan_details(order):
    return order.penjualandetail_set.all()