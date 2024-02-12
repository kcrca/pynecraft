from pathlib import Path

from pynecraft.base import TimeSpec, r
from pynecraft.commands import REPLACE, Score, a, comment, execute, return_, s, schedule, tell
from pynecraft.function import BLOCKS, DataPack, Function

pack = DataPack('warning')

pack.tags(BLOCKS)['bad_blocks'] = {'values': ['magma_block', 'tnt']}

self_score = Score(s(), 'warning')
halt = Score('halt', 'warning')
monitor = Function('monitor').add(
    comment('Stop if we have been told to'),
    execute().if_().score(halt).matches(1).run(return_()),
    comment('Find players with scores, and warn them if needed'),
    execute().as_(a().scores({self_score.objective: (0, None)})).run(
        execute().at(s()).if_().block(r(0, -1, 0), '#warning:bad_blocks').run(
            execute().if_().score(self_score).matches(0).run(tell(s(), 'Run away!')),
            execute().if_().score(self_score).matches((1, None)).run(tell(s(), 'NOW!!!!')),
            self_score.add(1),
        ),
        execute().at(s()).unless().block(r(0, -1, 0), '#warning:bad_blocks').run(self_score.set(0))
    )
)
pack.function_set.add(monitor)
schedule = schedule().function(monitor, TimeSpec('1s'), REPLACE)
monitor.add(schedule)

pack.function_set.add(Function('init').add(schedule, halt.init(0)))
pack.function_set.add(Function('halt').add(halt.set(1)))

pack.function_set.add(Function('start').add(self_score.set(0), schedule))
pack.function_set.add(Function('stop').add(self_score.reset()))

dir = f'{Path.home()}/clarity/home/saves/PynecraftWorld'
print(dir)
pack.save(dir)
