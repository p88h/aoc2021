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

defmodule Aoc2021.Day01 do
  def part1(args) do
    list = Enum.map(args, &String.to_integer/1)
    [ _ | tail ] = list
    Enum.zip(tail, list) |> Enum.reduce(0, fn {a,b},c -> if a>b do c+1 else c end end)
  end

  def part2(args) do
    args |> Enum.map(&String.to_integer/1)
         |> Enum.chunk_every(4,1,:discard)
         |> Enum.reduce(0, fn [a,_,_,b],c -> if b>a do c+1 else c end end)
  end
end
