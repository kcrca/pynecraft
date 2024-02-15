#############################################
**pynecraft**: Write Your DataPacks in Python
#############################################

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
   pynecraft

.. include:: ../README.rst

Structure
=========

Pynecraft has the following modules:

The top module
    Support for grouping commands into functions, folders of
    functions, and the top-level data pack.

``base``
    The base-level data types, classes, and values

``enums``
    Enums for large sets of values, like effects and particles.

``commands``
    The functions, classes, and constants for writing minecraft
    commands in python. These will generate strings that are the
    minecraft commands.

``simpler``
    Simplification classes and functions. Anything done here could
    be done directly with commands, but these provide simpler
    mechanisms.

``info``
    Some useful standard information about minecraft that is useful
    in commands, such as the hex values of colors, the list of note
    block instruments, the kinds of fish, as well as a ``Fish``
    class with helpful methods, etc. Oh, and lists of all blocks,
    items, and mobs.

Notes on Design
===============

There are several choices to be made when deciding how to map the
minecraft commands into a python (and hopefully pythonic) functions
and types. For example, consider the ``fill`` command, which takes
two sets of (x, y, z) coordinates, a block to fill with and some
options, such as whether to replace only certain kinds of blocks.
Representing the coordinates as three-tuples is pretty normal in
python, but how to handle the block type? And the options?

For the block type, pynecraft lets you use several different styles.
For simple blocks, you can just name the block::

    fill((1, 2, 3), (4, 5, 6), 'air')

There is also a class ``simpler.Block`` that lets you specify both
block state and nbt::

    fill((1, 2, 3), (4, 5, 6), Block('oak_sign', {'rotation', 5}, {'Text2': 'Howdy!'))

You can use a ``dict`` to specify block state and NBT (more on NBT
below).  Or you can just give the specification as a tuple::

    fill((1, 2, 3), (4, 5, 6), ('oak_sign', {'rotation', 5}, {'Text2': 'Howdy!'))

That pretty will handles blocks. You can do similarly with entities::

    summon(('Zombie', {'IsBaby': True}), (1, 2, 3))

But how pynecraft should present the options for ``fill`` are less
obvious. There are several different ways, such as:

``fill((1, 2, 3), (4, 5, 6), 'air', 'replace', 'stone')``
    Just using strings as optional parameters to ``fill()``. This
    is pretty free form, and easily allows mistakes.


``fill((1, 2, 3), (4, 5, 6), 'air', FillsOptions.REPLACE, 'stone')``
    Use an enum for the possible options, still as optional to
    parameters to ``fill()``. This is less prone to errors, but
    pretty verbose.

``fill((1, 2, 3), (4, 5, 6), 'air', REPLACE, 'stone')``
    Provide pre-defined constants for the possible options, still
    as optional to parameters to ``fill()``. This is less verbose,
    although someone could still put in a string and mistype it,
    but that takes work to make the mistake.

``fill((1, 2, 3), (4, 5, 6), 'air').replace('stone')``
    Provide chaining functions for further parameters. This prevents
    typos, and allows for more complex syntax. The ``data`` command,
    for example, has far too many possible syntaxes to represent
    as just strings.

Pynecraft takes both the last two approaches, varying with the
situation.  In places where there are several choices that are
syntactically identical, such as specifying direction of North,
East, South, or West, it tends towards the pre-defined constants.
In places where the choice affects syntax, there is a strong
preference for the chaining approach.

There are other interesting places where choices can be made. For
example, in the ``data`` command, there are three kinds of targets:
blocks, entities, and storage. The command makes you specify which
one: ``data get **entity** ...``, ``data get **block** ...``, etc.
However block specification look different from entity specifications,
so that keyword is redundant, and actually complicates the syntax.
So the pynecraft commands like ``data().get(e().tag('foo'))`` to
get data from an entity, and ``data().get((1, 2, 3))`` to get data
for a block at a given position. You can be specific if you want,
by using some predefined functions, such as
``data().get(entity(e().tag('foo')))``, but this is only required
if you are using macros in your command (more on macros later).

Finally, there is an overall preference to not be significantly
more verbose than the actual commands. This means that there are
several functions that could have longer names, but they don't. For
example, as shown above, ``e()`` is the way pynecraft represents
``@e``, and relative coordinates ``-1 -2 -3`` are represented as
``r(1, 2, 3)``.  Admittedly this takes up some of the single-character
identifier space, but it seems worth it.

There are a few large-scale collections of values that are expressed
in enums, like achievements and effects. These are in ``pynecraft.enums``.

*Error Checking*
----------------

Several things are done to try to catch errors before you load the
script into minecraft:

1. Some errors are simply illegal. You cannot misspell a command
name, for example.

2. Some will be warned about by any competent IDE because of type
hints in the method signatures.

3. Runtime type checking is used for many other things. For example,
a block or entity ID must be at least lexically legal: It must be
a sequence of letters, underscores, and digits, with an an optional
namespace (``minecraft:...``). If not, pynecraft will raise an
exception.

These will not prevent all errors, but it does mean errors are much
more likely to be caught by language and runtime rules rather than
by minecraft when the script is loaded.

Example
=======

The ``example`` module contains a program that will generate an
example datapack, called ``warning``. The primary function ``monitor``
checks players who have opted in to see if they're standing on top
of a bad block. If so, the first time it tells them to run, and
subsequent times it says "NOW!!!"

.. literalinclude:: ../example/warning.py
   :language: python
   :linenos:


It starts out by creating the pack. It then adds a block tag named
``bad_blocks``, listing the types of blocks considered bad.

It then creates two ``Score`` objects, one for each player who opts
in, the other is used to tell the system to stop.

Then comes the main function ``monitor`` function.

After that, ``monitor`` is added to the pack's ``function_set``.

Then we create a ``schedule`` command to invoke the function after
one second. That is used in several places, so we just create it
here once and reuse it.

Now we create all the other functions: ``init`` starts the system
running, while ``halt`` stops it; ``start`` opts the player in to
the system, and ``stop`` opts them out.

Finally, we save the pack to a directory.

To try this out, you can create a save. If you call it 'PynecraftWorld',
then the path you give to this command is the path to that save
dir. Then you can enter the world, run::

        /function warning::init
        /function warning::start

Now if you step on a bad block, you will be warned to move off it
until you do.

You can see several of the basic features ``pynecraft`` at work here:

* The datapack has a pretty natural Python structure.

* You don't have to remember (and correctly type) a bunch of files
  into a particular tree structure.

* If you make typos or other errors, the compile will let you know
  before you get any farther.

* Simplifications like ``Score`` let you code more naturally,
  handling the actual expressions correctly for you. Similarly,
  setting a tag to a list of block names is simpler than a map with
  that list inside a ``"values"`` tag would be, and that's nearly
  always what you want.

* The ``execute`` command's ``run`` will allow you to make several
  commands conditional on a single test in your code. This will mean
  multiple executions of the same test in the generated file, but
  typically these will be fast enough that the redunancy won't
  matter. If there are more commands, you can split out all the
  work into a separate function and run it by the outer ``execute``
  command.


Usage Overview
==============

Here is an expression that will print a minecraft ``give`` command
(of course, usually you won’t want to print commands, you want to
put them in functions, more on this below)::

    from pynecraft.commands import setblock       

    print(give(a(), 'iron_sword'))

The output will be::

    give @a iron_sword

For almost every command (except a few specialized server-side
commands that seem unlikely to appear in functions or command
blocks), there is a function in ``pynecraft.commands``. These may
return strings, or intermediate objects that support further chaining
calls. Here is how you could put together an ``experience`` command::

    print(experience().add(s(), 3, LEVELS))

    experience add 3 levels

In this case, ``experience()`` returns an object has the methods
``add()``, ``set()``, and ``query()``, the three subcommands of
``experience``.

You can remember this intermediate object and re-use it. One useful
case for this is in target specifications, which can get complicated::

    tgt = e().team('red').distance((None, 20))
    who = give(tgt, 'redstone_dust', 10)
    tag(tgt).add('redstoned')

This lets you say once what the constraint is and then use it across
several commands, which is both briefer and easier to modify.

This remembers the prefix that says which entity to run the command
as, and the use it three times. (We use ``as_()`` because ``as``
is a keyword in python, which is how all such conflicts are handled).
Each returned command object is immutable, so you can reuse them
without worry.

The ``execute`` command is another place where you could do this,
but you can also give ``run()`` multiple commands, and it
will generate a command for each one.:

    print(cmd) for cmd in execute().as_(e().tag('runner')).run(
        say('Ready to go!'),
        function('my_pack:go_to_it')
        say('Done!'))

gives you::

    execute as @e[tag=runner] run say Ready to go!
    execute as @e[tag=runner] run function my_pack:go_to_it
    execute as @e[tag=runner] run say Done!

*Macro Commands*
----------------
In Minecraft, macro commands are marked with a ``$``, and substitute
incoming values using ``$(foo)``.  Pynecraft just requires you to
mark where you are using incoming arguments, and prepends the ``$``
if needed.  So for example, you could use macro arguments like this::

    execute().as_(e().tag(Arg('tag'))).run(say(Arg('msg')))

This would give you::

    $execute as @e[tag=$(tag)] run say $(msg)

You could even just make the entire target a macro::

    execute().as_(Arg('tgt')).run(say(Arg('msg')))

In most places you can also simply use a a string, which is most
useful where the macro value represents part of a value. If you
want::

    tell @e[tag=xyz_$(foo)] Shh! There's a wumpus!!!

you can use::

    tell(e().tag('xyz_$(foo)'), 'Shh! There's a wumpus!!!')

(Macros can be used even more wildly than this, such as to represent
the actual command or a part of it, such as ``$e$(cmd)`` to run any
command that starts with an 'e'. In pynecraft you can only do this
literally by using a string as a command, or using the ``literal``
function. This level of flexibility would severely limit the amount
of checking pynecraft could do, and is unlikely to be commonly used,
so it doesn't provide for it any other way.)

Packs and Functions
-------------------

Of course, usually you won't want to print commands, you want to
put them in functions and put those functions in a data pack. The
``pynecraft.functions`` module help you do this. You can start with
a top-level data pack::

        pack = DataPack('my_pack', minecraft_saves / 'my_pack_world')

This creates a data pack named ``my_pack`` that will get saved in
the minecraft world ``my_pack_world``.  You can then go into that
world and use or test the pack. But you can use any directory, not
just a save.

Each pack has a top-level ``functions`` directory, which can have
one level of function directories beneath it (that's the current
minecraft rule). If you add a function to the pack, it goes in the
top level directory::

        func = Function('hello_world').add(say('Hello, world!'))
        pack.functions.add(func)
        pack.save()

Saving will first clear out the datapack directory, removing it
entirely. This is important: *The DatPack object owns the target
directory*, and you don't want old files hanging around. If you
rename a function, you don't want the old version of the function
to still exist with an older version of the code. If another function
calls it, but you forget to change the name there, that would be
confusing and possibly harmful.

Because of the way minecraft lays out its files, if you actually
give a path to the root of a save, DataPack will use the appropriate
subpath, rather than the save itself. And it will own *that*
directory, not the entire save. This means that "my_pack_world" is
a save, the directory it will own is ``my_pack_world/datapacks/my_pack``.
It recognizes a save by the existence of the ``datapacks`` directory
inside it.

Otherwise you can point it at a directory that it will own, such
as a staging area.

But whichever path it owns, remember: The DataPack **owns the
directory and will delete it!**

And then it will write out the files. In this case, it will create
a structure like the following (assuming ``my_pack_world`` as the
world's save path)::

        my_pack_save                            Top level of save
        |-- datapack                            Where datapacks go
          |-- my_pack                           Your specific pack
            |-- README                          A warning about generated code
            |-- pack.mcmeta                     The pack's metadata
            |-- data                            The pack's data
              |-- tags                          Any defined tags
              |-- functions                     The pack's functions
                |-- hellow_world.mcfunction     The specific function


The DataPack field ``function_set`` is a FunctionSet object, and you
can add your own FunctionSet objects to it to create subdirectories.
Again, Minecraft limits you to one level of depth, pynecraft just
enforces it.

There is a special kind of function called a ``Loop``, which is a
pynecraft utility that imitates having looping functionality. It
doesn't actually run in a loop, but acts as a loop iteration each
time it is invoked.  You tell it the items to loop over (say, the
various kinds of weather), and each time you run the loop's minecraft
function it will increment a score and then work with the weather
that correlates to the score.  The ``Loop`` documentation gives
more detail.

The Rest of the Pack
====================

There are two other parts of a data pack: The ``pack.mcmeta`` file
and a slew of JSON files to configure block and entity tags, loot
tables, custom dimensions, world generation, and so on.

``pack.mcmeta``
---------------

The ``pack.mcmeta`` file lives at the top of the data pack and has
some simple configuration, including the pack format version and
filters for other packs. DataPack supports this, both in giving you
direct access to its dict that is serialized into the JSON in the
file, via the ``mcmeta`` property, and via particular methods to
set the description and filters.

JSON Files
----------

DataPack organizes the JSON files as a top-level dict that contains
the relevant directories and their contained JSON files. Under this
dict, keys that end in '/' are saved as directories. These keys
have dict values whose keys are either subdirectories (they end in
'/' also) or files (they don't). File keys have dict values that
are saved as JSON files.

For example, the dict tree:

::

    {
        'advancements/': {
            'story/': {
                'battler': { 'criteria': { ... } },
            }
            'niceness': { 'criteria': { ... } },
        }
    }

translates into the following structure

::

        my_pack_save
        |-- datapack
          |-- my_pack
            |-- README
            |-- pack.mcmeta
            |-- data
              |-- advancements
                |-- story
                  |-- batter.json
                |-- niceness.json

The standard members of a data pack's JSON file set have defined
methods, such as ``advancements()``, ``recipies()``, and ``tags()``.
You can create other directories using the pack's ``json_directory()``
method.

Minecraft Versions
==================

Mojang keeps producing new minecraft versions, and these have different
commands, command syntaxes, restrictions, etc. How does pynecraft
handle them?

Well, right now it doesn't because it has been changed for each
version.  I could do this because it only had one user (me). But
in the future, what will happen?

At one point I attempted to have pynecraft be for all versions. I
started in 1.19, and when 1.20 came out, I added a way to specify
the version, and did various runtime checks to make sure that
incoming parameters or keywords were correct for each version, that
1.20 commands were not used in 1.19, etc. This proved so complicated
I gave it up. And that was just one version change.

Currently pynecraft is built for the (as of this writing) upcoming
1.21 release.  The plan is to keep it for 1.21, and produce a
separate, new (but derived) pynecraft for 1.22 when it arrives. You
will choose to install the version you want. The details of this
are to be worked out. Possibly the version gets encoded in the name
( ``pynecraft_1_21``, ``pynecraft_1_22``, etc.). Discussion will
be had; ideas are invited.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
