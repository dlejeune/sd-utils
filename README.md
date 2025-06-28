# Scouts Digital Utilities 🛠️

This repo is a quick command-line wrapper around some hacky python code I wrote to parse scouts digital data into more human- (or computer-) friendly formats. I make no guarantees any of this works beyond my machine (classic).

## Installation

I use uv for installation. Life is too short to do anything otherwise:

```
put install instruction here

```

Otherwise you can download the repo and install all the dependencies but if you know how to do that then I guess you can figure out the rest. 

### Dependencies

The bane of everyone's existence. One of the tools (the todo-list generator) requires a functional version of XeLaTeX. This is not the simplest thing to get working but there exist a few tutorials out there. TODO: Put links here

## Usage

When you install with uv, you get the command line tool `sd-utils`. Running `sd-utils --help` should provide an overview of the tool. 

In a nutshell, there are two sub-commands: `make-adv-chart` and `make-todo-list`. These produce nicely-formatted advancement charts and todo lists respectively. They both consume the advancement chart export from scouts digital. In theory, you can provide it with the "minimal" export, but I sugest just doing a full export.
