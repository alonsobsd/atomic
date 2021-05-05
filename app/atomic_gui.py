import json
import logging

from aiohttp import web
from aiohttp_jinja2 import template

from app.service.auth_svc import for_all_public_methods, check_authorization
from plugins.atomic.app.atomic_svc import AtomicService


@for_all_public_methods(check_authorization)
class AtomicGUI:

    def __init__(self, services, name, description):
        self.auth_svc = services.get('auth_svc')
        self.data_svc = services.get('data_svc')
        self.name = name
        self.description = description

        self.log = logging.getLogger('atomic_gui')

    @template('atomic.html')
    async def splash(self, request):
        abilities = [a for a in await self.data_svc.locate('abilities') if await a.which_plugin() == 'stockpile']
        adversaries = [a for a in await self.data_svc.locate('adversaries') if await a.which_plugin() == 'stockpile']
        return dict(name=self.name, description=self.description, abilities=abilities, adversaries=adversaries)
