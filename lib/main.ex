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
  def run(args) do
    day = if length(args) > 0 do
      # Use provided day number (needs to be 0-prefixed just like modules and files are)
      hd(args)
    else
      # Figure out the last day based on input files
      tl(Path.wildcard("input/day*.txt")) |> Path.basename() |> Path.rootname() |> String.slice(-2,2)
    end

    module = String.to_existing_atom("Elixir.Aoc2021.Day#{day}")
    file = File.open!("input/day#{day}.txt", [:read, :utf8])
    input = IO.read(file, :all) |> String.split("\n")

    Benchee.run(
      %{
        "Day #{day} Part 1" => fn -> module.part1(input) end,
        "Day #{day} Part 2" => fn -> module.part2(input) end
      },
      warmup: 1,
      time: 3
    )

    module.part1(input) |> IO.inspect(label: "Day #{day} Part 1 result:")
    module.part2(input) |> IO.inspect(label: "Day #{day} Part 2 result:")
  end
end
