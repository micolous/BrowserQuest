Bootstrap process
=================
* Upon load of index.html, the app is kicked off by the load of `require-jquery.js` at the bottom of the document.  This script reads the data-main attribute of its <script> tag and loads `home.js`.
* `home.js` loads `Class`, `Underscore`, `Stacktrace`, and `Util` modules.  It then requires `main.js`.
* `main.js` load `JQuery`, and `App`.  It defines the `initApp()` function and runs it.

initApp()
=========
