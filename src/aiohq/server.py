from __future__ import annotations
from logging import info, log
import logging

from typing import NamedTuple, Literal
from uuid import uuid4

from aiohttp import web
from aiohttp.web import (
    Response,
    Request,
)


class Ticket(NamedTuple):
    id: str
    status: Literal['OPEN', 'PROCESSING', 'DONE']


class MyApplication(web.Application):
    tickets: dict[str, Ticket]
    def __init__(self) -> None:
        logging.getLogger().setLevel(logging.INFO)
        super().__init__()
        self.add_routes([
            web.get('/health', self.health),
            web.post('/enqueue/{id}', self.enqueue),
            web.get('/poll', self.poll)
        ])
        self.tickets = {}
        info('application created')

    async def health(self, request: Request) -> Response:
        resp = dict(
            error=False,
            status='OK'
        )
        return web.json_response(resp)

    async def enqueue(self, request: Request) -> Response:
        id = request.match_info.get('id')
        start = request.match_info.get('start')
        end = request.match_info.get('end')

        uid = str(uuid4())
        ticket = Ticket(
            id=uid,
            status='OPEN'
        )
        self.tickets[uid] = ticket
        info(f'enqueued id {id} as ticket {uid}')
        return web.json_response(dict(
            error=False,
            ticket=uid,
        ))

    async def poll(self, request: Request) -> Response:
        uid = request.query.get('ticket', '')
        ticket = self.tickets.get(uid)
        if not ticket:
            return web.json_response(dict(
                error=True,
                status='NOT_FOUND'
            ))
        if ticket.status in ('OPEN', 'PROCESSING'):
            return web.json_response(dict(
                error=False,
                status=ticket.status
            ))
        if ticket.status == 'DONE':
            return web.json_response(dict(
                error=False,
                status='DONE'
            ))
        import inspect
        f = inspect.currentframe()
        assert f
        name = f.f_code.co_name
        raise RuntimeError(f'{name}: unexpected request')

def create_app() -> web.Application:
    return MyApplication()
