import os

import git
from django import template
from django.utils.html import format_html
from git import InvalidGitRepositoryError


try:
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha[:7]
except InvalidGitRepositoryError:
    if 'CURRENT_SOURCE' in os.environ:
        sha = os.environ['CURRENT_SOURCE'][:7]
    else:
        if 'HEROKU_SLUG_COMMIT' in os.environ:
            sha = os.environ['HEROKU_SLUG_COMMIT'][:7]
        else:
            sha = ""

register = template.Library()


@register.simple_tag()
def git_hash():
    if sha:
        return format_html('<p class="mb-0 text-secondary footer-text">Hash {}</p>', str(sha))
    else:
        return ""
