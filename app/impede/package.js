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
  api.use('ecmascript');
  api.addFiles('elements.js');
  api.addFiles('units.js');
  api.addFiles('statarea.js');
  api.addFiles('descarea.js');
  api.addFiles('drawable.js');
  api.addFiles('grid.js');
  api.addFiles('configuration.js');
  api.addFiles('sprites.js');
  api.addFiles('metastate.js');
  api.addFiles('state.js');
  api.addFiles('impede.js');
});

Package.onTest(function(api) {
  api.use('ecmascript');
  api.use('tinytest');
  api.use('internal');
  api.addFiles('internal-tests.js');
});
