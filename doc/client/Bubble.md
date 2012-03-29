Bubble
======
*js/bubble.js*

Class to represent a speech bubble.

Properties
----------
* `id` --- value to represent bubble (mainly used by BubbleManager)
* `element` --- jQuery DOM object of speech bubble
* `timer` --- `Timer` object to destroy speech bubble after 5 seconds.

Methods
-------
**init(id, element, time)**

Assigns `this.id`, `element` should be a jQuery-ified DOM object which is assigned to `this.element`, `this.timer` is created as a 5 second timer, starting at `time`

**isOver(time)**

Returns `true` if `this.timer` has run out, false otherwise

**destroy()**

Removes `this.element` from the DOM

**reset(time)**

Resets bubble timer to begin 5 second destroy-countdown from `time`