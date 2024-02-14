
Introduction to pynecraft
=========================

``pynecraft`` is a Python package that lets you create
a data pack and its functions using python, so you can take
advantage of python's tools. It generates the files required
for a data pack from your python code.

Writing data packs requires handling a lot of details, from
putting things in the right folders in the correct format, to
how those things are expressed in the first place. All errors
are discovered during reload, or possibly at run time, rather
than when you're editing the files in the first place.

In contrast, Python (and other actual programming languages) have
syntax checkers, errors for misspelled function and field names,
IDEs that do auto-completion and checks for improper data types.
And of course you have basic programming language tools, like loops
and functions with parameters that generate similar output for
varying input.

``pynecraft`` lets you use all that in creating your
data pack. It represents the data pack as an object that
understands much of the layout of the data pack, and provides
ways to generate commands inside functions from within Python,
as well as JSON files all around the data pack. This means you
have all the power of a real programming language to generate
your commands, including syntax and other error checks, python
functions that generate minecraft commands that can be used in
minecraft functions. And pynecraft also knows where to store
what files in a data pack, and how to generate some boilerplate,
like the ``pack.mcmeta``.

As a simple example, the following is a "hello_world" data pack::

    pack = DataPack('hello_world')
    pack.function_set.add(Function('hello').add(say('Hello, World!')))
    pack.save(minecraft_world)

We create a DataPack object, and add a Function to it. That function
has, as its sole command, the result of calling ``say``, which is
a pynecraft function that returns a minecraft ``say`` command with
the provided string. We add it to the function ``hello_world:hello``
inside the ``hello_world`` data pack. Any number of commands can
be added at once, or any other time before the ``save()``, which
writes out the data pack files to a specified directory.

If 'minecraft_world' is a minecraft world save, the ``save()``
method will create::

    minecraft_world
    |-- datapacks
	|-- hello_world
	    |-- README                 # A generated warning not to edit this by hand
	    |-- pack.mcmeta
	    |-- data
		|-- functions
		    |-- hello.mcfunction
			"say Hello, World!"


Pynecraft also has simple calls for obscure or complex minecraft
mechanisms. For example, there is a Score class that holds the
definition of a score (name and objective). You can use it as a
parameter to commands like ``scoreboard``, but more importantly,
it has methods to generate commands simply, such as ``score.add(15)``
to generate ``scoreboard players add <i>player objective</i> 15``.

Other examples of simplifications include:

* ``Item.of(<i>block</i>)``, which returns the NBT required to store
  an item including its state and data as (say) an item you would
  summon into the world to be picked up by a player

* The ``Sign`` class that generates all the messy NBT to set sign
  texts and commands, so::

      Sign((None, 'hi', 'there'), (tell(p(), 'Hello!'),)).place((0, 100, 0), WEST)

  …which gives a list of three lines of text for the sign and one ``tell`` command, generates the lovely::

      setblock 0 100 0 oak_sign[rotation=4]{front_text: {messages: ['{"text": "",
        "clickEvent": {"action": "run_command", "value": "/tell @p Hello!"}}',
        '{"text": "hi"}', '{"text": "there"}', '{"text": ""}']}}

  …a command that places an oak sign facing west at 0 100 0 with
  three lines of text which, when touched by the player, tells them
  "Hello!" (in case you couldn't decode all that NBT). (Actually
  it generates two commands, the first of which sets that block to
  ``air``, to work around the fact that setting a sign at a place
  sometimes will not overwrite an existing sign, which is another
  thing you'd probably prefer not to worry about, and pynecraft
  takes care of for you.)

Pynecraft is distributed under the standard MIT license.

Why?
----

Python has tools: editors, debugger, formatters, etc. It also
checks syntax at compile time and has run-time type checking. These
are really useful for eliminating errors from your commands quickly
and easily.

It is a full language, so you can use it to generate your commands.
You can have a check for every mob that starts with 'a', or every
value of a score from one to ten. You can write a python function
that generates complicated commands based on a few parameters.

There are macro languages that could help with this, but the
quoting issues alone can be daunting, and they won't do the syntax
and run-time validation of commands.

I wrote pynecraft because I was working on my `RestWorld resource
pack test world <https://claritypack.com/restworld>`_.  It makes
extensive use of functions. After using a macro system to generate
things for a while, it was clear that this was ugly and difficult.
Pynecraft made a big difference. The "saying what I mean to say"
stage of development nearly entirely vanished.  I still had bugs
and made mistakes, out they were almost never typos or command
syntax problems. And with some of the simplification tools, I also
stopped making mistakes about how relatively complicated things
were done.

I hope it will help you, too!

(Currently pynecraft only supports Java Edition commands. A Bedrock
version is certainly possible as a companion project; if someone
wants to undertake it, please let me know.)

Resources
=========
Here are some useful resources:

* `The python docs <https://pynecraft.readthedocs.io/en/latest/#>`_.
* `The discord <https://discord.gg/ksmuc4qqvy>`_.
* `The GitHub repository <https://github.com/kcrca/pynecraft>`_
* `Bugs and feature tickets <https://github.com/kcrca/pynecraft/issues>`_
* `The "warning" example
  <https://github.com/kcrca/pynecraft/blob/main/example/warning.py>`_,
  a basic example included with the source.
* `The megavillage project
  <https://github.com/kcrca/megavillage/tree/main/megavillage>`_,
  a simple project of mine (YouTube videos coming soon!)
* `The RestWorld project
  <https://github.com/kcrca/restworld/tree/main/restworld>`_, a
  very complex use that is the original target, whose `very own
  website is here <https://claritypack.com/restworld>`_.
