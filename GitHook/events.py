from typing import Optional

from .classes import DataHolder, Repository, Collaborator, Installation


class Event(DataHolder):
    _required_keys = ('action', 'repository', 'sender')
    _keep = ['organization', 'installation']

    @property
    def action(self) -> str:
        return self.get('action')

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


class Push(Event):
