import os
import sys
import itertools

PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
DAY_COLOR = (0,0,0,0)
NIGHT_COLOR = (10,10,50,150)
SUNSET_COLOR = (125,50,0,70)
COLORS = itertools.cycle([DAY_COLOR, DAY_COLOR, DAY_COLOR, SUNSET_COLOR, NIGHT_COLOR, NIGHT_COLOR, NIGHT_COLOR, SUNSET_COLOR])
CYCLE_DURATION = 40000