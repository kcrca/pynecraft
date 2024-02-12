"""
Example for using pynecraft. This is a simple datapack that warns players to move if they are standing on top of a bad
block, reminding them every second. It only warns players who have opted in, however.
"""

import sys

from pynecraft.base import TimeSpec, r
from pynecraft.commands import REPLACE, Score, a, comment, execute, return_, s, schedule, tell
from pynecraft.function import BLOCKS, DataPack, Function

# Create the 'warning' datapack
pack = DataPack('warning')

#  Set the 'bad_blocks' block tag
pack.tags(BLOCKS)['bad_blocks'] = ['magma_block', 'tnt']

self_score = Score(s(), 'warning')  # score that will be used for each player
halt = Score('halt', 'warning')  # whether to halt the process
# The overall monitoring function
monitor = Function('monitor').add(
    comment('Stop if we have been told to'),
    execute().if_().score(halt).matches(1).run(return_()),
    comment('Find players with scores, and warn them if needed'),
    execute().as_(a().scores({self_score.objective: (0, None)})).run(
        execute().at(s()).if_().block(r(0, -1, 0), '#warning:bad_blocks').run(
            execute().if_().score(self_score).matches(0).run(tell(s(), 'Run away!')),
            execute().if_().score(self_score).matches((1, None)).run(tell(s(), 'NOW!!!!')),
            self_score.add(1),  # adds 1 to the score, generates 'scoreboard players add @s warning 1'
        ),
        execute().at(s()).unless().block(r(0, -1, 0), '#warning:bad_blocks').run(self_score.set(0))
    )
)
# Add it to the pack. This sets the functions full name (which includes the pack name)
pack.function_set.add(monitor)
# This command schedules the next run of the monitor, which is used in a few places
schedule = schedule().function(monitor, TimeSpec('1s'), REPLACE)
# ... including at the end of the monitor function itself
monitor.add(schedule)

# Function to set the warning system in motion
pack.function_set.add(Function('init').add(schedule, halt.init(0)))
# Function to halt the warning system
pack.function_set.add(Function('halt').add(halt.set(1)))

# Function to start monitoring the invoking player
pack.function_set.add(Function('start').add(self_score.set(0), schedule))
# Function to stop monitoring the invoking player
pack.function_set.add(Function('stop').add(self_score.reset()))

# Write the datapack to the given directory / save
pack.save(sys.argv[1])
