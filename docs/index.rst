pynecraft
=========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
   pynecraft

Introduction
============

Minecraft data packs have several complexities. The most complex
part is the minecraft commands that go in functions. The syntax is
rather haphazard, and small typos can be difficult to figure out.

Pynecraft is designed to help with this. You can write your scripts
in python, and then save the resulting commands in functions. It
also has simplifications of several odd or complicated parts of the
minecraft commands. For example, the scoreboard is complicated, but
pynecraft's ``Score`` class lets you say things like ``score.set(1)``
instead of the command ``scoreboard players set score_name
score_objective 0`` or whatever.

Beyond the functions, pynecraft has other mechanisms to support
data packs, although these are still rudimentary, currently covering
only tags.

Currently pynecraft only supports Java Edition commands.

Why?
----

Python has tools: Editors, debuggers, formatters, etc. It also
checks syntax at compile time and is easy to add run-time type
checking. It has a full language, so even though you cannot loop
or use other control structures in your actual minecraft function,
you can use them to build your functions. This provides a much
better infrastructure for writing you minecraft functions.

Also, it is possible to use these to provide the simpler tools
mentioned above. You don't have to remember which ``ArmorItem``
slot is the chestplate, or what the syntax is for either defining
an action for when the player touches a sign, or the rules about
how that syntax is quoted when embedding it into the sign's NBT.

At some future date, maybe someone can add a python interpreter to
minecraft so you can write your actual scripts in python instead
of the rather hacky non-programming language that is minecraft
commands.  Until then, this can make your life much easier.

Structure
=========

Pynecraft has the following modules:

``base``
    The base-level data types and values

``enums``
    Enums for large sets of values, like effects and particles.

``commands``
    The functions, classes, and constants for writing minecraft
    commands in python. These will generate strings that are the
    minecraft commands.

``functions``
    Support for grouping commands into functions, folders of
    functions, and the top-level data pack.

``simpler``
    Simplification classes and functions. Anything done here could
    be done directly with commands, but these provide simpler
    mechanisms.

Notes on Design
==============-

There are several choices to be made when deciding how to map the
minecraft commands into a python (and hopefully pythonic) functions
and types. For example, consider the ``fill`` command, which takes
two sets of (x, y, z) coordinates, a block to fill with and some
optional commands, such as whether to replace only certain kinds
of blocks.  Representing the coordinates as three-tuples is pretty
normal in other packages, but how to handle the block type? And the
options?

For the block type, you can use several different styles. For simple
blocks, you can just name the block:

::

    fill((1, 2, 3), (4, 5, 6), 'air')

There is also a class ``simpler.Block`` that lets you specify both
block state and nbt:

::

    fill((1, 2, 3), (4, 5, 6), Block('oak_sign', {'rotation', 5}, {'Text2': 'Howdy!'))

We use a dict to specify block state and NBT (more on NBT below).
Or you can just give the specification as a tuple:

::

    fill((1, 2, 3), (4, 5, 6), ('oak_sign', {'rotation', 5}, {'Text2': 'Howdy!'))

That pretty will handles blocks. You can do similarly with entities:

::

    summon(('Zombie', {'IsBaby': True}), (1, 2, 3))

But the options for ``fill`` are less obvious. One could present
them in several different ways:

``fill((1, 2, 3), (4, 5, 6), 'air', 'replace', 'stone')``
    Just using strings as optional to parameters to ``fill()``.
    This is pretty free form, and easily allows mistakes.


``fill((1, 2, 3), (4, 5, 6), 'air', FillsOptions.REPLACE, 'stone')``
    Use an enum for the possible options, still as optional to
    parameters to ``fill()``.  This is less prone to errors, but
    pretty verbose.

``fill((1, 2, 3), (4, 5, 6), 'air', REPLACE, 'stone')``
    Provide pre-defined constants for the possible options, still
    as optional to parameters to ``fill()``.  This is less verbose,
    although someone could still put in a string and mistype it,
    but that takes work to make the mistake.

``fill((1, 2, 3), (4, 5, 6), 'air').replace('stone')``
    Provide chaining functions for further parameters. This prevents
    typos, and allows for more complex syntax. The ``data`` command,
    for example, has far too many possible syntaxes to represent
    as just strings.

Pynecraft takes the last two approaches, varying with the situation.
In places where there are several choices that are syntactically
identical, such as specifying direction of North, East, South, or
West, it tends towards the pre-defined constants. In places where
the choice affects syntax, there is a strong preference for the
chaining approach.

There are other interesting places where choices can be made. For
example, in the ``data`` command, there are three kinds of targets:
blocks, entities, and storage. The command makes you specify which
one: ``data get entity...``, ``data get block...`` etc. However
block specification look different from entity specifications, so
that keyword is redundant, and actually complicates the syntax. So
the pynecraft commands like ``data().get(e().tag('foo'))`` to get
data from an entity, and ``data().get((1, 2, 3))`` to get data for
a block at a given position.

Finally, there is an overall preference to not be significantly
more verbose than the actual commands. This means that there are
several functions that could have longer names, but they don't. For
example, as shown above, ``e()`` is equivalent to '@e', and to
specify relative coordinates, ``r(1, 2, 3)`` will generate ``-1 -2
-3``. Admittedly this takes up some of the single-character identifier
space, but it seems worth it.

There are a few large-scale collections of values that are expressed
in enums, like the achievements and effects. These are in
``pynecraft.enums``

*Error Checking*
----------------

Several things are done to try to catch errors before you load the
script into minecraft:

1. Some errors are simply illegal. You cannot misspell a command
name, for example.

2. Some will be warned about by any competent IDE, due to type hints
in the method signatures.

3. Runtime type checking is used for many other things. For example,
a block or entity ID must be at least lexically legal: It must be
a sequence of letters, underscores, and digits, with an an optional
namespace (``minecraft:...``). If not, pynecraft will raise an
exception.

These will not prevent all errors, but it does mean errors are much
more likely to be caught by language and runtime rules rather than
by minecraft when the script is loaded.


Usage
=====

Here is an expression that will print a minecraft ``setblock`` command:

::

    from pynecraft.commands import setblock       

    print(setblock(r(0, 2, 0), 'stone'))

The output will be

::

    setblock -0 -2 -0 stone

For almost every command (except a few specialized server-side
commands that seem unlikely to appear in functions or command
blocks), there is a function in ``pynecraft.commands``. These may
return strings, or intermediate objects that support further chaining
calls. Here is how you could put together an ``experience`` command:

::

    print(experience().add(s(), 3, LEVELS))

    experience add 3 levels

In this case, ``experience()`` returns an object has the methods
``add()``, ``set()``, and ``query()``, the three subcommands of
``experience``.

You can remember this intermediate object and re-use it. This is
probably most useful with the ``execute`` command which can get
complicated:

::

    who = execute().as_(e().tag('runner'))

    print(who.run(say('Ready to go!')))
    print(who.run(function('my_pack:go_to_it')))
    print(who.run(say('Done!')))

This remembers the prefix that says which entity to run the command
as, and the use it three times (it is ``as_()`` because ``as`` is
a keyword in python.) Each returned command object is immutable,
so you can reuse them without worrying about affecting future calls.

You can also do this by giving ``run()`` multiple commands to
run, and it will generate a command for each one.
::

    print(cmd) for cmd in execute().as_(e().tag('runner')).run(
        say('Ready to go!'),
        function('my_pack:go_to_it')
        say('Done!'))

*Functions*
-----------

Usually you don't want to print commands, but to instead put them
in functions, and usually put those functions in a data pack. The
``pynecraft.functions`` types help you do this. You can start with
a top-level data pack:

::

        pack = DataPack('my_pack', minecraft_saves / 'my_pack_world')

This creates a data pack named "my_pack" that will get saved in the
minecraft world "my_pack_world". This is often useful for testing,
because you can then go into that world and test the pack. Any
directory will work.

Each pack has a top-level 'functions' directory, which can have one
level of function directories beneath it (that's the current minecraft
rule). If you add a function to the pack, it goes in the top level
directory:

::

        func = Function('hello_world').add(say('Hello, world!'))
        pack.functions.add(func)
        pack.save()

This will first clear out the datapack directory, removing it
entirely. This is important: The DatPack object owns the target
directory, and you don't want old files hanging around. If you
rename a function, you don't want the old vesion of the function
to still exist with an older version of the code. If another function
calls it, but you forget to change the name there, that would be
confusing and possibly harmful.

Because of how minecraft lays out its files, if you actually give
a path to the root of a save, DataPack will use the appropriate
subpath, rather than the save itself. And it will own *that*
directory, not the entire save. This means that "my_pack_world" is
a save, the directory it will own is ``my_pack_world/datapacks/my_pack``.
it recognizes a save by the existence of the ``datapacks`` directory
inside it.

Otherwise you can point it at a directory that it will own, such
as a staging area.

But whichever path it owns, remember: The DataPack **owns the
directory and will delete it!**

And then it will write out the files. In this case, it will create
a structure like the following (assuming ``my_pack_world`` as the
path):

::

        my_pack_save                            Top level of save
        |-- datapack                            Where datapacks go
          |-- my_pack                           Your specific pack
            |-- README                          A warning about generated code
            |-- pack.mcmeta                     The pack's metadata
            |-- data                            The pack's data
              |-- tags                          Any defined tags
              |-- functions                     The pack's functions
                |-- hellow_world.mcfunction     The specific function


The DataPack field ``functions`` is a FunctionSet object, and you
can add your own FunctionSet objects to it to create subdirectories.
Again, Minecraft limits you to one level of depth, pynecraft just
enforces it.

There is a special kind of function called a Loop, which is a way
to imitate having looping functionality. It doesn't actually run
in a loop, but acts as a loop iteration each time it is invoked.
You tell it the items to loop over (say, the various kinds of
weather), and each time you run the loop function it will increment
a score and then produce the weather that correlates to the score.
The Loop documentation gives more detail.

The Rest of the Pack
====================

There are two other parts of a data pack: The ``pack.mcmeta`` file
and a slew of JSON files to confgure block and entity tags, loot
tables, custom dimensions, world generation, and o on.

``pack.mcmeta``
---------------

The ``pack.mcmeta`` file lives at the top of the data pack and has
some simple configuration, including the pack format version and
filters for other packs DataPack supports this, both in giving you
direct access to its dict that is serialized into the JSON in the
file, via the ``mcmeta`` property, and via particular methods to
set the dsecription and filters.

JSON Files
----------

DataPack organizes the JSON files as a top-level dict that contains
the relevant directories and their contained JSON files. Under this
dict, keys that end in '/' are saved as directories. These keys
have dict values whose keys are either subdirectories (they end in
'/' also) or files (they don't).  File keys have dict values that
are saved as JSON files.

For example, the dict tree:

::

    {
        'advancments/': {
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
methods, such as ``advacnements()``, ``recipies``, and ``tags()``.
You can create other dirctories using the pack's ``json_directory()``
method.

Minecraft Versions
------------------

Pynecraft was originally written for Minecraft version 1.19, but new things can happen to the
commands with each release. You can specify a version to the ``parameters`` object. For example,
to set the version to 1.19.3, you could say

::
    base.parameters.version = '1.19.3'

Where differences exist, they are checked when used. For example, the ``fillbiome`` command was
new in 1.19.3. So without setting the version to a value >= 1.19.3, invoking ``fillbiome()`` will
get an exception. Versions are specified using either ``packaging.version.Version``
objects or strings, which are converted to ``Version`` objects.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
