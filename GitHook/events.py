# Documents: https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads
from typing import Optional

from .classes import DataHolder, Repository, Collaborator, Installation


class Event(DataHolder):
    _required_keys = ('repository', 'sender')

    def __init__(self, action, data: dict):
        super().__init__(data)
        self._action = action

    @property
    def action(self) -> str:
        return self._action

    @property
    def repository(self) -> Repository:
        return Repository(self.get('repository'))

    @property
    def sender(self) -> Collaborator:
        return Collaborator(self.get('sender'))

    @property
    def organization(self) -> Optional[Collaborator]:
        data = self.get('organization')
        return Collaborator(data) if data else None

    @property
    def installation(self) -> Optional[Installation]:
        data = self.get('installation')
        return Installation(data) if data else None


# Todo - Event Branch_Protection_Rule
class Branch_Protection_Rule(Event):
    pass


# Todo - Event Check_Run
class Check_Run(Event):
    pass


# Todo - Event Check_Suite
class Check_Suite(Event):
    pass


# Todo - Event Code_Scanning_Alert
class Code_Scanning_Alert(Event):
    pass


# Todo - Event Commit_Comment
class Commit_Comment(Event):
    pass


# Todo - Event Content_Reference
class Content_Reference(Event):
    pass


# Todo - Event Create
class Create(Event):
    pass


# Todo - Event Delete
class Delete(Event):
    pass


# Todo - Event Deploy_Key
class Deploy_Key(Event):
    pass


# Todo - Event Deployment
class Deployment(Event):
    pass


# Todo - Event Deployment_Status
class Deployment_Status(Event):
    pass


# Todo - Event Discussion
class Discussion(Event):
    pass


# Todo - Event Discussion_Comment
class Discussion_Comment(Event):
    pass


# Todo - Event Fork
class Fork(Event):
    pass


# Todo - Event Github_App_Authorization
class Github_App_Authorization(Event):
    pass


# Todo - Event Gollum
class Gollum(Event):
    pass


# Todo - Event Installation
class Installation(Event):
    pass


# Todo - Event Installation_Repositories
class Installation_Repositories(Event):
    pass


# Todo - Event Issue_Comment
class Issue_Comment(Event):
    pass


# Todo - Event Issues
class Issues(Event):
    pass


# Todo - Event Label
class Label(Event):
    pass


# Todo - Event Marketplace_Purchase
class Marketplace_Purchase(Event):
    pass


# Todo - Event Member
class Member(Event):
    pass


# Todo - Event Membership
class Membership(Event):
    pass


# Todo - Event Meta
class Meta(Event):
    pass


# Todo - Event Milestone
class Milestone(Event):
    pass


# Todo - Event Organization
class Organization(Event):
    pass


# Todo - Event Org_Block
class Org_Block(Event):
    pass


# Todo - Event Package
class Package(Event):
    pass


# Todo - Event Page_Build
class Page_Build(Event):
    pass


# Todo - Event Ping
class Ping(Event):
    pass


# Todo - Event Project_Card
class Project_Card(Event):
    pass


# Todo - Event Project_Column
class Project_Column(Event):
    pass


# Todo - Event Project
class Project(Event):
    pass


# Todo - Event Public
class Public(Event):
    pass


# Todo - Event Pull_Request
class Pull_Request(Event):
    pass


# Todo - Event Pull_Request_Review
class Pull_Request_Review(Event):
    pass


# Todo - Event Pull_Request_Review_Comment
class Pull_Request_Review_Comment(Event):
    pass


class Push(Event):
    _required_keys = ('repository', 'sender', 'commits')
    _optional_keys = {'created': False, 'deleted': False, 'forced': False}

    def __init__(self, data: dict):
        super().__init__('push', data)

    @property
    def ref(self):
        return self.get('ref')

    @property
    def before(self):
        return self.get('before')

    @property
    def after(self):
        return self.get('after')

    @property
    def created(self):
        return self.get('created')

    @property
    def deleted(self):
        return self.get('deleted')

    @property
    def forced(self):
        return self.get('forced')

    @property
    def base_ref(self):
        return self.get('base_ref')

    @property
    def compare(self):
        return self.get('compare')

    @property
    def commits(self):
        return self.get('commits')

    @property
    def head_commit(self):
        return self.get('head_commit')

    @property
    def pusher(self):
        return self.get('pusher')


# Todo - Event Release
class Release(Event):
    pass


# Todo - Event Repository_Dispatch
class Repository_Dispatch(Event):
    pass


# Todo - Event Repository
class Repository(Event):
    pass


# Todo - Event Repository_Import
class Repository_Import(Event):
    pass


# Todo - Event Repository_Vulnerability_Alert
class Repository_Vulnerability_Alert(Event):
    pass


# Todo - Event Secret_Scanning_Alert
class Secret_Scanning_Alert(Event):
    pass


# Todo - Event Security_Advisory
class Security_Advisory(Event):
    pass


# Todo - Event Sponsorship
class Sponsorship(Event):
    pass


# Todo - Event Star
class Star(Event):
    pass


# Todo - Event Status
class Status(Event):
    pass


# Todo - Event Team
class Team(Event):
    pass


# Todo - Event Team_Add
class Team_Add(Event):
    pass


# Todo - Event Watch
class Watch(Event):
    pass


# Todo - Event Workflow_Dispatch
class Workflow_Dispatch(Event):
    pass


# Todo - Event Workflow_Job
class Workflow_Job(Event):
    pass


# Todo - Event Workflow_Run
class Workflow_Run(Event):
    pass
