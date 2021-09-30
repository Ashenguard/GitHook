import re
from datetime import datetime
from typing import Tuple, Dict, Optional, Any, Iterable, List


class URL:
    @staticmethod
    def from_str(url: str) -> 'URL':
        url = url.replace("\\", "/")

        assert url is not None, 'url must be provided'
        assert url.startswith("https://") or url.startswith('http://'), 'invalid url format'

        https = url.startswith("https://")
        url_parts = url[7 + 1 if https else 0:].split('/')

        url = url_parts[0]
        args = tuple(url_parts[1:])

        return URL(https, url, args)

    def __init__(self, https: bool = True, url: str = None, args: Iterable[str] = None):
        assert url is not None, 'url must be provided'
        assert url.find('/') == -1 and url.find('\\') == -1, 'url can not have "/" or "\\" in it'
        args = [] if args is None else args
        for arg in args:
            placeholders = re.findall("{(.+?)}", arg)
            for placeholder in placeholders:
                arg = arg.replace(f'{{{placeholder}}}', 'HOLDER_HERE')

            assert arg.find('/') == -1 and arg.find('\\') == -1, 'arguments can not have "/" or "\\" in them'

        self._https = https
        self._url = url
        self._args = args

    def get_url(self, **args):
        url = ('https://' if self._https else 'http://') + self._url

        for arg in self._args:
            placeholders = re.findall("{(.+?)}", arg)
            for holder in placeholders:
                if holder.startswith('/'):
                    holder = holder[1:]
                    value = ''
                    if holder in args:
                        value = args.get(holder)

                    arg = arg.replace(f'{{/{holder}}}', value)
                else:
                    value = ''
                    if holder in args:
                        value = args.get(holder)
                    else:
                        raise KeyError(f'url requires an argument named "{holder}" to be created')

                    arg = arg.replace(f'{{{holder}}}', value)

            if arg:
                url += '/' + arg

        return url

    def add_args(self, *args):
        return URL(https=self._https, url=self._url, args=(*self._args, *args))

    def __repr__(self):
        return f'<URL "{self.__str__()}">'

    def __str__(self):
        args = '/'.join(self._args)
        return ('https://' if self._https else 'http://') + self._url + (f'/{args}' if args else '')


class DataHolder:
    _required_keys: Tuple[str] = ()
    _optional_keys: Dict[str, Optional[Any]] = {}

    def analyse_data(self, data: dict, keep: list):
        new_data = data.copy()

        for key in self._required_keys:
            if key not in new_data:
                raise ValueError(f'Data is missing required key: "{key}"')

        for key, value in self._optional_keys.items():
            if key not in new_data:
                new_data[key] = value

        return new_data

    def __init__(self, data: dict, keep: list = None):
        self._data = self.analyse_data(data, keep)

    def get(self, key, default=None):
        return self._data.get(key, default)


class Collaborator(DataHolder):
    _required_keys = ('id', 'login', 'node_id')
    _optional_keys = {'type': 'User', 'site_admin': False}

    @property
    def login(self) -> str:
        return self.get('login')

    @property
    def id(self) -> int:
        return self.get('id')

    @property
    def node_id(self) -> str:
        return self.get('node_id')

    @property
    def avatar_url(self) -> str:
        return self.get('avatar_url')

    @property
    def gravatar_id(self) -> str:
        return self.get('gravatar_id')

    @property
    def url(self) -> URL:
        return URL.from_str(f'https://api.github.com/users/{self.login}')

    @property
    def html_url(self) -> URL:
        return URL.from_str(f'https://github.com/{self.login}')

    @property
    def followers_url(self) -> URL:
        return self.url.add_args('followers')

    @property
    def following_url(self) -> URL:
        return self.url.add_args('following', '{/other_user}')

    @property
    def gists_url(self) -> URL:
        return self.url.add_args('gists', '{/gist_id}')

    @property
    def starred_url(self) -> URL:
        return self.url.add_args('starred', '{/owner}', '{/repo}')

    @property
    def subscriptions_url(self) -> URL:
        return self.url.add_args('subscriptions')

    @property
    def organizations_url(self) -> URL:
        return self.url.add_args('orgs')

    @property
    def repos_url(self) -> URL:
        return self.url.add_args('repos')

    @property
    def events_url(self) -> URL:
        return self.url.add_args('events', '{/privacy}')

    @property
    def received_events_url(self) -> URL:
        return self.url.add_args('received_events')

    @property
    def type(self) -> str:
        return self.get('type')

    @property
    def site_admin(self) -> bool:
        return self.get('site_admin')


class Licence(DataHolder):
    _required_keys = ('key', 'name', 'spdx_id', 'node_id')

    @property
    def key(self):
        return self.get('key')

    @property
    def name(self):
        return self.get('name')

    @property
    def spdx_id(self):
        return self.get('spdx_id')

    @property
    def url(self):
        return self.get('url')

    @property
    def node_id(self):
        return self.get('node_id')


class Repository(DataHolder):
    _required_keys = ('id', 'node_id', 'name', 'owner')
    _optional_keys = {'private': False, 'fork': False, 'is_template': False, 'has_issues': True, 'has_projects': True, 'has_wiki': True,
                      'has_pages': False, 'has_downloads': False, 'archived': False, 'visibility': 'public', 'allow_rebase_merge': True,
                      'allow_squash_merge': True, 'allow_auto_merge': False, 'delete_branch_on_merge': True, 'allow_merge_commit': True}

    @property
    def id(self) -> int:
        return self.get('id')

    @property
    def node_id(self) -> str:
        return self.get('node_id')

    @property
    def name(self) -> str:
        return self.get('name')

    @property
    def full_name(self) -> str:
        return f'{self.owner.login}/{self.name}'

    @property
    def owner(self) -> Collaborator:
        return self.get('owner')

    @property
    def private(self) -> bool:
        return self.get('private')

    @property
    def html_url(self) -> URL:
        return URL.from_str(f'https://github.com/{self.owner.login}/{self.name}')

    @property
    def description(self) -> str:
        return self.get('description')

    @property
    def fork(self) -> bool:
        return self.get('fork')

    @property
    def url(self) -> URL:
        return URL.from_str(f'https://api.github.com/repos/{self.full_name}')

    @property
    def archive_url(self) -> URL:
        return self.url.add_args('{archive_format}', '{/ref}')

    @property
    def assignees_url(self, user=None) -> URL:
        return self.url.add_args('assignees', '{/user}')

    @property
    def blobs_url(self) -> URL:
        return self.url.add_args('git', 'blobs', '{/sha}')

    @property
    def branches_url(self) -> URL:
        return self.url.add_args('branches', '{/branch}')

    @property
    def collaborators_url(self) -> URL:
        return self.url.add_args('collaborators', '{/collaborator}')

    @property
    def comments_url(self) -> URL:
        return self.url.add_args('comments', '{/number}')

    @property
    def commits_url(self) -> URL:
        return self.url.add_args('commits', '/{sha}')

    @property
    def compare_url(self) -> URL:
        return self.url.add_args('compare', '{base}...{head}')

    @property
    def contents_url(self, path=None) -> URL:
        return self.url.add_args('contents', '{/path}')

    @property
    def contributors_url(self) -> URL:
        return self.url.add_args('contributors')

    @property
    def deployments_url(self) -> URL:
        return self.url.add_args('deployments')

    @property
    def downloads_url(self) -> URL:
        return self.url.add_args('downloads')

    @property
    def events_url(self) -> URL:
        return self.url.add_args('events')

    @property
    def forks_url(self) -> URL:
        return self.url.add_args('forks')

    @property
    def git_commits_url(self) -> URL:
        return self.url.add_args('git', 'commits', '{/sha}')

    @property
    def git_refs_url(self) -> URL:
        return self.url.add_args('git', 'refs', '{/sha}')

    @property
    def git_tags_url(self) -> URL:
        return self.url.add_args('git', 'tags', '{/sha}')

    @property
    def git_url(self) -> str:
        return f'git:github.com/{self.owner.login}/{self.name}.git'

    @property
    def issue_comment_url(self) -> URL:
        return self.issues_url.add_args('comments', '{/number}')

    @property
    def issue_events_url(self) -> URL:
        return self.issues_url.add_args('events', '{/number}')

    @property
    def issues_url(self) -> URL:
        return self.url.add_args('issues', '{/number}')

    @property
    def keys_url(self) -> URL:
        return self.url.add_args('keys', '{/key_id}')

    @property
    def labels_url(self) -> URL:
        return self.url.add_args('labels', '{/name}')

    @property
    def languages_url(self) -> URL:
        return self.url.add_args('languages')

    @property
    def merges_url(self) -> URL:
        return self.url.add_args('merges')

    @property
    def milestones_url(self) -> URL:
        return self.url.add_args('milestones', '{/number}')

    @property
    def notifications_url(self) -> URL:
        return self.url.add_args('notifications')

    @property
    def pulls_url(self) -> URL:
        return self.url.add_args('pulls', '{/number}')

    @property
    def releases_url(self) -> URL:
        return self.url.add_args('releases', '{/id}')

    @property
    def ssh_url(self) -> str:
        return f'git@github.com:{self.full_name}.git'

    @property
    def stargazers_url(self) -> URL:
        return self.url.add_args('stargazers')

    @property
    def statuses_url(self) -> URL:
        return self.url.add_args('statuses', '{sha}')

    @property
    def subscribers_url(self) -> URL:
        return self.url.add_args('subscribers')

    @property
    def subscription_url(self) -> URL:
        return self.url.add_args('subscription')

    @property
    def tags_url(self) -> URL:
        return self.url.add_args('tags')

    @property
    def teams_url(self) -> URL:
        return self.url.add_args('teams')

    @property
    def trees_url(self) -> URL:
        return self.url.add_args('trees', '{/sha}')

    @property
    def clone_url(self) -> URL:
        return URL.from_str(f'https://github.com/{self.full_name}.git')

    @property
    def mirror_url(self) -> str:
        return self.get('mirror_url')

    @property
    def hooks_url(self) -> URL:
        return self.url.add_args('hooks')

    @property
    def svn_url(self) -> URL:
        return URL.from_str(f'https://svn.github.com/{self.full_name}')

    @property
    def homepage(self) -> str:
        return self.get('homepage')

    @property
    def language(self) -> str:
        return self.get('language')

    @property
    def forks_count(self) -> int:
        return self.get('forks_count')

    @property
    def forks(self) -> int:
        return self.get('forks')

    @property
    def stargazers_count(self) -> int:
        return self.get('stargazers_count')

    @property
    def watchers_count(self) -> int:
        return self.get('watchers_count')

    @property
    def watchers(self) -> int:
        return self.get('watchers')

    @property
    def size(self) -> int:
        return self.get('size')

    @property
    def default_branch(self) -> str:
        return self.get('default_branch')

    @property
    def open_issues_count(self) -> int:
        return self.get('open_issues_count')

    @property
    def open_issues(self) -> int:
        return self.get('open_issues')

    @property
    def is_template(self) -> bool:
        return self.get('is_template')

    @property
    def topics(self) -> list:
        return self.get('topics')

    @property
    def has_issues(self) -> bool:
        return self.get('has_issues')

    @property
    def has_projects(self) -> bool:
        return self.get('has_projects')

    @property
    def has_wiki(self) -> bool:
        return self.get('has_wiki')

    @property
    def has_pages(self) -> bool:
        return self.get('has_pages')

    @property
    def has_downloads(self) -> bool:
        return self.get('has_downloads')

    @property
    def archived(self) -> bool:
        return self.get('archived')

    @property
    def disabled(self) -> bool:
        return self.get('disabled')

    @property
    def visibility(self) -> str:
        return self.get('visibility')

    @property
    def pushed_at(self) -> datetime:
        time = self.get('pushed_at')
        return datetime.fromisoformat(time) if time else datetime.fromtimestamp(0)

    @property
    def created_at(self) -> datetime:
        time = self.get('created_at')
        return datetime.fromisoformat(time) if time else datetime.fromtimestamp(0)

    @property
    def updated_at(self) -> datetime:
        time = self.get('updated_at')
        return datetime.fromisoformat(time) if time else datetime.fromtimestamp(0)

    @property
    def permissions(self) -> dict:
        return self.get('permissions') or {}

    @property
    def allow_rebase_merge(self) -> bool:
        return self.get('allow_rebase_merge')

    @property
    def template_repository(self) -> Optional['Repository']:
        data = self.get('template_repository')
        return Repository(data, []) if data else None

    @property
    def temp_clone_token(self) -> str:
        return self.get('temp_clone_token')

    @property
    def allow_squash_merge(self) -> bool:
        return self.get('allow_squash_merge')

    @property
    def allow_auto_merge(self) -> bool:
        return self.get('allow_auto_merge')

    @property
    def delete_branch_on_merge(self) -> bool:
        return self.get('delete_branch_on_merge')

    @property
    def allow_merge_commit(self) -> bool:
        return self.get('allow_merge_commit')

    @property
    def subscribers_count(self) -> int:
        return self.get('subscribers_count')

    @property
    def network_count(self) -> int:
        return self.get('network_count')

    @property
    def license(self) -> Optional[Licence]:
        data = self.get('license')
        return Licence(data, []) if data else None

    @property
    def organization(self) -> Optional[Collaborator]:
        data = self.get('organization')
        return Collaborator(data, []) if data else None

    @property
    def parent(self) -> Optional['Repository']:
        data = self.get('parent')
        return Repository(data, []) if data else None

    @property
    def source(self) -> Optional['Repository']:
        data = self.get('source')
        return Repository(data, []) if data else None


# Todo - Compelete Installation class
class Installation(DataHolder):
    pass