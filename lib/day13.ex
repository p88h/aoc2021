# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

use Bitwise

defmodule Aoc2021.Day13 do
  def process1(s) do
    [ a, b ] = String.split(s, ",")
    { String.to_integer(a), String.to_integer(b) }
  end
  def process2(s) do
    [ l, r ] = String.split(s, "=")
    xy = List.last(String.split(l, " "))
    { String.to_atom(xy), String.to_integer(r) }
  end

  def foldxy({x, y}, []), do: {x, y}  # swap after folding
  def foldxy({x, y}, [ {:x, f} | t ]), do: foldxy({f-abs(x-f), y}, t)
  def foldxy({x, y}, [ {:y, f} | t ]), do: foldxy({x, f-abs(y-f)}, t)

  def process(args, limit) do
    [ ps, _, fs ] = Enum.chunk_by(args, &(&1 == ""))
    folds = Enum.take(Enum.map( fs, &process2/1), limit)
    Enum.map(ps, &process1/1) |> Enum.map(&foldxy(&1, folds)) |> Enum.frequencies() |> Map.keys()
  end

  def part1(args), do: process(args, 1) |> length()

  def match([]), do: ""
  def match([0b111110,0b001001,0b001001,0b111110 | t]), do: "A" <> match(t)
  def match([0b111111,0b100101,0b100101,0b011010 | t]), do: "B" <> match(t)
  def match([0b011110,0b100001,0b100001,0b010010 | t]), do: "C" <> match(t)
  def match([0b111111,0b100101,0b100101,0b100001 | t]), do: "E" <> match(t)
  def match([0b111111,0b000101,0b000101,0b000001 | t]), do: "F" <> match(t)
  def match([0b011110,0b100001,0b101001,0b111010 | t]), do: "G" <> match(t)
  def match([0b111111,0b000100,0b000100,0b111111 | t]), do: "H" <> match(t)
  def match([0b010000,0b100000,0b100001,0b011111 | t]), do: "J" <> match(t)
  def match([0b111111,0b000100,0b011010,0b100001 | t]), do: "K" <> match(t)
  def match([0b111111,0b100000,0b100000,0b100000 | t]), do: "L" <> match(t)
  def match([0b011110,0b100001,0b100001,0b011110 | t]), do: "O" <> match(t)
  def match([0b111111,0b001001,0b001001,0b000110 | t]), do: "P" <> match(t)
  def match([0b011110,0b100001,0b100011,0b011111 | t]), do: "Q" <> match(t)
  def match([0b111111,0b001001,0b011001,0b100110 | t]), do: "R" <> match(t)
  def match([0b010010,0b100101,0b101001,0b010010 | t]), do: "S" <> match(t)
  def match([0b011111,0b100000,0b100000,0b011111 | t]), do: "U" <> match(t)
  def match([0b110001,0b101001,0b100101,0b100011 | t]), do: "Z" <> match(t)
  def match([0b11111,0b10001,0b10001,0b10001,0b11111 | t]), do: "▯" <> match(t)

  def paint([ ]), do: 0
  def paint([ {_, y} | t ]), do:  (1 <<< y) + paint(t)

  def part2(args) do
    process(args, 999)  |> Enum.sort() |> Enum.chunk_by(&elem(&1,0)) |> Enum.map(&paint/1)|> match()
  end
end
