import git
from django import template
from django.utils.html import format_html

repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha[:7]

register = template.Library()


@register.simple_tag()
def git_hash():
    return format_html('<p class="mb-0 text-secondary footer-text">Hash {}</p>', str(sha))
