import hashlib
import hmac
import json
import logging
from typing import Type

import six
from flask import Flask, request, abort

from GitHook.events import Event


class Webhook:
    def __init__(self, app: Flask):
        self._app: Flask = app
        self._logger = logging.getLogger("webhook")

    def hook(self, endpoint: str, event: Type[Event], secret=None):
        def decorator(func):
            self.add_hook(func, event, endpoint, secret)
            return func

        return decorator

    def add_hook(self, func, event: Type[Event], endpoint: str, secret=None):
        pass

    @property
    def app(self) -> Flask:
        return self._app

    @property
    def logger(self):
        return self._logger


class EventHook:
    def __init__(self, webhook: Webhook, endpoint: str, secret=None):
        self._webhook = webhook
        self._events = {}
        self._secret = secret

        self._webhook.app.add_url_rule(endpoint, endpoint, self._post_recieve, methods=['POST'])

    @property
    def secret(self):
        return self._secret

    @secret.setter
    def secret(self, secret):
        if secret is not None and not isinstance(secret, six.binary_type):
            secret = secret.encode("utf-8")
        self._secret = secret

    def add_event(self, func, event_type: Type[Event]):
        self._events.setdefault(event_type, [])
        self._events.get(event_type).append(func)

    def _get_header(self, key):
        try:
            return request.headers[key]
        except KeyError:
            abort(400, "Missing header: " + key)

    def _validate_secret(self):
        digest = hmac.new(self._secret, request.data, hashlib.sha1).hexdigest() if self._secret else None

        if digest is not None:
            sig_parts = self._get_header("X-Hub-Signature").split("=", 1)
            if not isinstance(digest, six.text_type):
                digest = six.text_type(digest)

            if len(sig_parts) < 2 or sig_parts[0] != "sha1" or not hmac.compare_digest(sig_parts[1], digest):
                abort(400, "Invalid signature")

    def _post_recieve(self):
        event_type = self._get_header("X-Github-Event")
        content_type = self._get_header("content-type")
        data = (
            json.loads(request.form.to_dict()["payload"])
            if content_type == "application/x-www-form-urlencoded"
            else request.get_json()
        )

        if data is None:
            abort(400, "Request body must contain json")

        count = 0
        fails = 0
        for event in self._events.keys():
            if event.__name__.lower() == event_type + '_event':
                for func in self._events.get(event, []):
                    try:
                        func(event(data))
                        count += 1
                    except Exception:
                        fails += 1

        if count == 0:
            return "No event was found", 204
        else:
            message = f"Executed {count} methods" + "" if fails == 0 else f" but failed to execute {fails} methods"
            return message, 200
