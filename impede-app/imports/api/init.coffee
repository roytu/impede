
# Initialize the server

sessions = new Meteor.Collection("sessions")
processQueue = new Meteor.Collection("processQueue")
 
if Meteor.isServer
    Meteor.publish("sessions", => return sessions.find())
    Meteor.publish("processQueue", => return processQueue.find())
