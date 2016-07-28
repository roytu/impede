Package.describe({
  name: 'internal',
  version: '0.0.1',
  // Brief, one-line summary of the package.
  summary: '',
  // URL to the Git repository containing the source code for this package.
  git: '',
  // By default, Meteor will default to using README.md for documentation.
  // To avoid submitting documentation, set this field to null.
  documentation: 'README.md'
});

Package.onUse(function(api) {
  api.versionsFrom('1.2.1');
  api.use('coffeescript');
  api.addFiles('elements.coffee');
  api.addFiles('units.coffee');
  api.addFiles('statarea.coffee');
  api.addFiles('descarea.coffee');
  api.addFiles('drawable.coffee');
  api.addFiles('grid.coffee');
  api.addFiles('configuration.coffee');
  api.addFiles('sprites.coffee');
  api.addFiles('metastate.coffee');
  api.addFiles('state.coffee');
  api.addFiles('impede.coffee');
});
