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

defmodule Aoc2021.Day02 do

  def process(args) do
    args |> Enum.map(&String.split/1)
         |> Enum.map(fn [dir, val] -> {String.to_atom(dir), String.to_integer(val)} end)
  end

  def move1({:forward, v}, {x, d}), do: { x + v, d }
  def move1({:down, v}, {x, d}), do: { x, d + v}
  def move1({:up, v}, {x, d}), do: { x, d - v}

  def part1(args) do
    process(args) |> Enum.reduce({0, 0}, &move1/2) |> (fn { x , d } -> x * d end).()
  end

  def move2({:forward, v}, {x, d, a}), do: { x + v, d + a * v, a }
  def move2({:down, v}, {x, d, a}), do: { x, d, a + v }
  def move2({:up, v}, {x, d, a}), do: { x, d, a - v }

  def part2(args) do
    process(args) |> Enum.reduce({0, 0, 0}, &move2/2) |> (fn { x , d, _ } -> x * d end).()
  end
end
