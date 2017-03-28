import { Meteor } from 'meteor/meteor';

Meteor.startup(() => {
  // code to run on server at startup
  import "../imports/api/init.coffee"
});
