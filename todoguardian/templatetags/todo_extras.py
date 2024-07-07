from django import template

from ..models import Todo

register = template.Library()


@register.inclusion_tag("templatetags/show_todo.html")
def show_todo(todo: Todo):
    """Renders a given todo."""
    return {"todo": todo}
