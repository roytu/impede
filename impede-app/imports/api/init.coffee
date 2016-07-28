
# Initialize the server

# Make "sessions" if it doesn't already exist
sessions = new Meteor.Collection("sessions")
 
if Meteor.isServer
    Meteor.publish("sessions", => return sessions.find())
