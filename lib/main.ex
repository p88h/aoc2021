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

defmodule Mix.Tasks.Main do
  use Mix.Task
  @shortdoc "Advent of Code Runner"
  @spec run(any) :: any
  def run(_args) do
    day = "01" # TODO: parametrize this ?
    module = String.to_existing_atom("Elixir.Aoc2021.Day#{day}")
    file = File.open!("input/day#{day}.txt", [:read, :utf8])
    input = IO.read(file, :all ) |> String.split("\n")
    input |> module.part1() |> IO.inspect(label: "Part 1:")
    input |> module.part2() |> IO.inspect(label: "Part 2:")
  end
end
