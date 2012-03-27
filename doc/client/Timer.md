Timer
=====
*js/timer.js*

Properties
----------
* `lastTime` -- `startTime` given in `init`.  This is updated every time isOver is called.
* `duration` -- how long the timer should last

Methods
-------
**init(duration, startTime)**

Sets timer start time and duration


*isOver(time)*

Call this with the current tick value as `time`

Returns true if `time` is greater than timer's `lastTime` + `duration`