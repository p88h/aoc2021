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

  def process1([dir, val], {x, d}) do
    v = String.to_integer(val)
    case dir do
      "forward" -> { x + v, d }
      "down" -> { x, d + v }
      "up" -> { x, d - v }
    end
  end

  def part1(args) do
    args |> Enum.map(&String.split/1)
         |> Enum.reduce({0, 0}, fn it, acc -> process1(it,acc) end)
         |> (fn { x , d } -> x * d end).()
  end

  def process2([dir, val], {x, d, a}) do
    v = String.to_integer(val)
    case dir do
      "forward" -> { x + v, d + a * v, a}
      "down" -> { x, d, a + v }
      "up" -> { x, d, a - v }
    end
  end

  def part2(args) do
    args |> Enum.map(&String.split/1)
         |> Enum.reduce({0, 0, 0}, fn it, acc -> process2(it,acc) end)
         |> (fn { x , d, _ } -> x * d end).()
  end
end
