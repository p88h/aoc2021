p88h Advent of Code 2021
========================

This is a repository containing solutions for the 2021 Advent of Code
(https://adventofcode.com/).

This years language of choice is Elixir, and the proper solutions are all in the `lib/` 
directory, one per day + some common dispatch code in main.ex. 

If you would like to run this your self, you can do it like so, from the top-level 
directory of the project:

```
$ mix main
Day 16 Part 1: 879
Day 16 Part 2: 539051801941
```

The following additional options are supported

* `mix main 01` (or any other day name, but need leading zeroes for first 9) will run that particular day
* `mix main all` will run all of the modules
* `mix main bench` will run under Benchee and report performance (this is what goes into BENCHMARKS.md)
* `mix main bench all` or `mix main bench 14` also works
* `mix test` will run the unit tests (=validate all parts on their respective sample inputs)

Visualisations
==============

In addition to the Elixir code, the `vis/` directory contains visualisations of all challenges. 
All of those are written in Python, most likely require Python 3, and are built on top of 
[Pygame](https://pygame.org/). 

The simplest way to view them is on [YouTube](https://www.youtube.com/playlist?list=PLgRrl8I0Q168jJYjfbzak3l-9xkLU6bCE)


If, however, you would like to run them, you will need to first get all the dependencies:

```
$ pip install pygame numpy ffmpeg-python
```

* `pygame` is needed for all the display functions. 
* `ffmpeg` is only needed when making  recordings, and optional otherwise.
* `numpy` is only needed in one of the visualisations, and is not critical 
(commenting out relevant lines will work perfectly fine, you just won't get polynomial approximations).

Visualisations run on the same inputs as the main challenges. All of the visualisations support 
same basic controls: press ESCAPE to quit, and press SPACE to pause. 
In addition to that, in Day 12 you can drag the caves around using the mouse.

The visualisation scripts support some common commandline arguments:
* `-r` | `--rec` : creates a recording of the screen output, the output will be saved into an mp4 file 
in the current directory, named after the script name (`vis/day01.py` will produce `day01.mp4`)
* `-f` | `--fps` `<FPS>` : sets both the display and recording speed to the specified value. 
Note that even if the script cannot handle the specified FPS, recorded video will play at that rate,
rather than what you see during the run. 
The default FPS vary per script, and setting that should not be necessary.

Copyright disclaimer
====================

Licensed under the Apache License, Version 2.0 (the "License");
you may not use these files except in compliance with the License.
You may obtain a copy of the License at

   https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
