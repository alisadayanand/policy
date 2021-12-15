from sqlalchemy import Column, Integer, Date, Time, String, ForeignKey
from sqlalchemy.orm import relationship

from models.Base import Base


class Agenda(Base):
   __tablename__ = 'agenda'
   agenda_id = Column(Integer, primary_key=True)
   meeting_id = Column(Integer, ForeignKey('meeting_calendar.meeting_id'))
   date = Column(Date)
   start_time = Column(Time)
   end_time = Column(Time)
   location = Column(String(length=30))
   chairperson = Column(String(length=100))
   attendees = Column(String(length=1000))
   by_invitation = Column(String(length=1000))
   apologies_declines = Column(String(length=1000))
   minute_taker = Column(String(length=100))
   next_meeting_date = Column(Date)
   # meeting = relationship('Meeting', primaryjoin='meeting_calendar.meeting_id == agenda.meeting_id', lazy='dynamic')
   meeting = relationship('Meeting', remote_side='Meeting.meeting_id')