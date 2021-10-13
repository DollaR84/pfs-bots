"""
API methods for events PayForSay Bot.

created on 09.10.2021

@author: Ruslan Dolovanyuk

"""

from dataclasses import dataclass

import datetime

from base import Agent as ag

from events.models import User, Event


@dataclass
class EventData:
    owner_id: int
    owner_name: str
    event_id: int
    name: str
    title: str
    description: str
    media: str
    created: datetime.datetime
    expiry: datetime.datetime = None


async def get_count_events():
    """Return active events count."""
    session = ag.db.get_session()
    result = session.query(Event.id).filter(Event.expiry.is_(None) | (Event.expiry < datetime.datetime.now())).count()
    return result


async def read_event_from_db(index):
    session = ag.db.get_session()
    row = session.query(Event).filter(Event.id == index).first()
    return EventData(row.owner.user_id, row.owner.full_name, row.id, row.name, row.title, row.description, row.media, row.created, row.expiry)


async def read_events_from_db(offset, step):
    session = ag.db.get_session()
    results = session.query(Event).filter(Event.expiry.is_(None) | (Event.expiry < datetime.datetime.now())).offset(offset).limit(step)
    return results


async def write_event_to_db(data):
    session = ag.db.get_session()
    user = session.query(User).filter(User.user_id == data['user_id']).first()
    if not user:
        user = User(user_id=data['user_id'], full_name=data['user_name'])
        session.add(user)
        session.commit()
    event = Event(owner_id=user.id, name=data['event_name'], title=data['event_title'], description=data['event_description'], media=data['event_media'], expiry=data['date_expiry'])
    session.add(event)
    session.commit()
    return event


async def delete_event_from_db(index):
    session = ag.db.get_session()
    session.query(Event).filter(Event.id == index).delete()
    session.commit()
