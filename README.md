# Simple Top-Down Shooter

WASD - Walk  
Shift - Sprint  
Arrow Keys - Fire Arrow  
Scroll - Zoom


## Todo List

 * Rewrite player movement and collisions  
 * Add enemy attacks  
 * Add player base  
 * Add inventory and drops

 ### Known Bugs

 * The player will sometimes get stuck sprinting even when WASD keys are released until shift is released. during this state the player ignores collisions. - Will be fixed after movement/collision rewrite
 * Arrows sometimes dont collide with enemies if the enemy was recently hit, there is no invincibility period programmed yet so that shouldn't happen. - Should also be fixed after collision rewrite