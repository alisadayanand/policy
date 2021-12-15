from flask import Flask, render_template, request

from models.Agenda import Agenda
from models.Meeting import Meeting
from models.Base import Session

session = Session()
selectedEditAgenda = ''

main = Flask(__name__)

@main.route('/home', methods=['POST', 'GET'])
@main.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html')

@main.route('/set', methods=['POST', 'GET'])
def set():
    return render_template('agenda_set.html')

@main.route('/edit', methods=['POST', 'GET'])
def edit():
    return render_template('agenda_edit.html')

@main.route('/view', methods=['POST', 'GET'])
def view():
    return render_template('agenda_view.html')





def addAgendaToDb(meetingName, meetingDate, startTime, endTime, location, chairperson, attendees, byInvitation, apologies, minuteTaker, nextMeetingDate):
   newAgenda = Agenda(
                      meeting_id= meetingName,
                      date=meetingDate,
                      start_time=startTime,
                      end_time=endTime,
                      location=location,
                      chairperson=chairperson,
                      attendees=attendees,
                      by_invitation=byInvitation,
                      apologies_declines=apologies,
                      minute_taker=minuteTaker,
                      next_meeting_date=nextMeetingDate)
   session.add(newAgenda)
   session.commit()

def selectAllAgendas():
  return session.query(Agenda).all()



def getAgendaByDate(date):
   return session.query(Agenda).filter_by(date=date).first()



def updateAgendaInDb(id, agendaView):
   agenda = session.query(Agenda).get(id)

   agenda.date = agendaView.date
   agenda.start_time = agendaView.start_time
   agenda.end_time = agendaView.end_time
   agenda.location = agendaView.location
   agenda.chairperson = agendaView.chairperson
   agenda.attendees = agendaView.attendees
   agenda.by_invitation = agendaView.by_invitation
   agenda.apologies_declines = agendaView.apologies_declines
   agenda.minute_taker = agendaView.minute_taker
   agenda.next_meeting_date = agendaView.next_meeting_date


   session.commit()

def deleteAgenda(id):
   session.query(Agenda).filter(Agenda.agenda_id == id).delete()
   session.commit()

def selectAllMeetings():
   meetings = session.query(Meeting).all()
   for meeting in meetings:
       print("Meeting ID: {}".format(meeting.meeting_id))
   return meetings



@main.route('/getAgendas', methods=['POST', 'GET'])
def getAgenda():
    agendas = selectAllAgendas()
    return agendas


@main.route('/viewAgendaByDate', methods=['POST', 'GET'])
def viewAgendaByDate():

    date = request.form['date']
    agenda = getAgendaByDate(date)

    # set as a global variable so that I can get the id
    global selectedEditAgenda
    selectedEditAgenda = agenda

    if request.referrer == 'http://localhost:5000/view':

        return render_template('agenda_view.html',
                               meetingName="SGT SASER",
                               startTime=agenda.start_time,
                               endTime=agenda.end_time,
                               location=agenda.location,
                               chairperson=agenda.chairperson,
                               attendees=agenda.attendees,
                               byInvitation=agenda.by_invitation,
                               apologies=agenda.apologies_declines,
                               minuteTaker=agenda.minute_taker,
                               date=agenda.date,
                               nextMeetingDate=agenda.next_meeting_date
                           )

    else:
        return render_template('agenda_edit.html',
                               meetingName="SGT SASER",
                               startTime=agenda.start_time,
                               endTime=agenda.end_time,
                               location=agenda.location,
                               chairperson=agenda.chairperson,
                               attendees=agenda.attendees,
                               byInvitation=agenda.by_invitation,
                               apologies=agenda.apologies_declines,
                               minuteTaker=agenda.minute_taker,
                               date=agenda.date,
                               nextMeetingDate=agenda.next_meeting_date
                               )

@main.route('/addAgenda', methods=['POST', 'GET'])
def addAgenda():

    meetingName = request.form['name']
    meetingDate = request.form['date']
    startTime = request.form['starttime']
    endTime = request.form['endtime']
    location = request.form['locroom']
    chairperson = request.form['chairperson']
    attendees = request.form['attendees']
    byInvite = request.form['byinvite']
    apologies = request.form['apol']
    minuteTaker = request.form['mintaker']
    nextMeetingDate = request.form['nextdate']

    addAgendaToDb(meetingName, meetingDate, startTime, endTime, location, chairperson, attendees, byInvite, apologies, minuteTaker, nextMeetingDate)

    return render_template('agenda_set.html')


@main.route('/updateAgenda', methods=['POST', 'GET'])
def updateAgenda():

    global selectedEditAgenda
    meetingName = request.form['name']
    meetingDate = selectedEditAgenda.date
    startTime = request.form['starttime']
    endTime = request.form['endtime']
    location = request.form['locroom']
    chairperson = request.form['chairperson']
    attendees = request.form['attendees']
    byInvite = request.form['byinvite']
    apologies = request.form['apol']
    minuteTaker = request.form['mintaker']
    nextMeetingDate = request.form['nextdate']

    agendaUpdated = Agenda(
                      date=meetingDate,
                      start_time=startTime,
                      end_time=endTime,
                      location=location,
                      chairperson=chairperson,
                      attendees=attendees,
                      by_invitation=byInvite,
                      apologies_declines=apologies,
                      minute_taker=minuteTaker,
                      next_meeting_date=nextMeetingDate)

    updateAgendaInDb(selectedEditAgenda.agenda_id, agendaUpdated)


@main.route('/getMeetings', methods=['POST', 'GET'])
def getMeetings():
    meetings = selectAllMeetings()
    return meetings

main.run(debug=True)