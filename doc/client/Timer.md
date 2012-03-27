Timer
=====
*js/timer.js*

Properties
----------
* `lastTime` -- `startTime` given in `init`
* `duration` -- how long the timer should last

Methods
-------
*init(`duration`, `startTime`)*
Sets timer start time and duration

*isOver(`time`)*
Returns true if `time` is greater than timer's `lastTime` + `duration`