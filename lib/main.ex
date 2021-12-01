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
