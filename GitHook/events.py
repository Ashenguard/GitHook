# Documents: https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads
from typing import Optional

from .classes import DataHolder, Repository, Collaborator, Installation, Release


class Event(DataHolder):
    _required_keys = ('repository', 'sender')

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
class Branch_Protection_Rule_Event(Event):
    pass


# Todo - Event Check_Run
class Check_Run_Event(Event):
    pass


# Todo - Event Check_Suite
class Check_Suite_Event(Event):
    pass


# Todo - Event Code_Scanning_Alert
class Code_Scanning_Alert_Event(Event):
    pass


# Todo - Event Commit_Comment
class Commit_Comment_Event(Event):
    pass


# Todo - Event Content_Reference
class Content_Reference_Event(Event):
    pass


# Todo - Event Create
class Create_Event(Event):
    pass


# Todo - Event Delete
class Delete_Event(Event):
    pass


# Todo - Event Deploy_Key
class Deploy_Key_Event(Event):
    pass


# Todo - Event Deployment
class Deployment_Event(Event):
    pass


# Todo - Event Deployment_Status
class Deployment_Status_Event(Event):
    pass


# Todo - Event Discussion
class Discussion_Event(Event):
    pass


# Todo - Event Discussion_Comment
class Discussion_Comment_Event(Event):
    pass


# Todo - Event Fork
class Fork_Event(Event):
    pass


# Todo - Event Github_App_Authorization
class Github_App_Authorization_Event(Event):
    pass


# Todo - Event Gollum
class Gollum_Event(Event):
    pass


# Todo - Event Installation
class Installation_Event(Event):
    pass


# Todo - Event Installation_Repositories
class Installation_Repositories_Event(Event):
    pass


# Todo - Event Issue_Comment
class Issue_Comment_Event(Event):
    pass


# Todo - Event Issues
class Issues_Event(Event):
    pass


# Todo - Event Label
class Label_Event(Event):
    pass


# Todo - Event Marketplace_Purchase
class Marketplace_Purchase_Event(Event):
    pass


# Todo - Event Member
class Member_Event(Event):
    pass


# Todo - Event Membership
class Membership_Event(Event):
    pass


# Todo - Event Meta
class Meta_Event(Event):
    pass


# Todo - Event Milestone
class Milestone_Event(Event):
    pass


# Todo - Event Organization
class Organization_Event(Event):
    pass


# Todo - Event Org_Block
class Org_Block_Event(Event):
    pass


# Todo - Event Package
class Package_Event(Event):
    pass


# Todo - Event Page_Build
class Page_Build_Event(Event):
    pass


# Todo - Event Ping
class Ping_Event(Event):
    pass


# Todo - Event Project_Card
class Project_Card_Event(Event):
    pass


# Todo - Event Project_Column
class Project_Column_Event(Event):
    pass


# Todo - Event Project
class Project_Event(Event):
    pass


# Todo - Event Public
class Public_Event(Event):
    pass


# Todo - Event Pull_Request
class Pull_Request_Event(Event):
    pass


# Todo - Event Pull_Request_Review
class Pull_Request_Review_Event(Event):
    pass


# Todo - Event Pull_Request_Review_Comment
class Pull_Request_Review_Comment_Event(Event):
    pass


class Push_Event(Event):
    _required_keys = ('repository', 'sender', 'commits')
    _optional_keys = {'created': False, 'deleted': False, 'forced': False}

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


class Release_Event(Event):
    _required_keys = ('action', 'release', 'repository', 'sender')

    @property
    def action(self) -> str:
        return self.get('action')

    @property
    def release(self) -> Release:
        return Release(self.get('release'))


# Todo - Event Repository_Dispatch
class Repository_Dispatch_Event(Event):
    pass


# Todo - Event Repository
class Repository_Event(Event):
    pass


# Todo - Event Repository_Import
class Repository_Import_Event(Event):
    pass


# Todo - Event Repository_Vulnerability_Alert
class Repository_Vulnerability_Alert_Event(Event):
    pass


# Todo - Event Secret_Scanning_Alert
class Secret_Scanning_Alert_Event(Event):
    pass


# Todo - Event Security_Advisory
class Security_Advisory_Event(Event):
    pass


# Todo - Event Sponsorship
class Sponsorship_Event(Event):
    pass


# Todo - Event Star
class Star_Event(Event):
    pass


# Todo - Event Status
class Status_Event(Event):
    pass


# Todo - Event Team
class Team_Event(Event):
    pass


# Todo - Event Team_Add
class Team_Add_Event(Event):
    pass


# Todo - Event Watch
class Watch_Event(Event):
    pass


# Todo - Event Workflow_Dispatch
class Workflow_Dispatch_Event(Event):
    pass


# Todo - Event Workflow_Job
class Workflow_Job_Event(Event):
    pass


# Todo - Event Workflow_Run
class Workflow_Run_Event(Event):
    pass
