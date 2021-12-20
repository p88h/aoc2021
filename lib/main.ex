defmodule Mix.Tasks.Main do
  def file_to_day(p), do: Path.basename(p) |> Path.rootname() |> String.slice(-2,2)
  def all_days(), do: Path.wildcard("input/day*.txt") |> Enum.map(&file_to_day/1)

  def parse_args([], cfg = %{days: []}), do: %{cfg | days: [ List.last(all_days()) ] }
  def parse_args([], cfg), do: cfg
  def parse_args(["bench" | t], cfg), do: parse_args(t, %{cfg | bench: true })
  def parse_args(["all" | t], cfg), do: parse_args(t, %{cfg | days: all_days() })
  def parse_args([ s | t ], cfg), do: parse_args(t, %{cfg | days: [ s | cfg[:days]] })

  use Mix.Task
  @shortdoc "Advent of Code Runner"
  @spec run(any) :: any
  def run(args) do
    config = parse_args(args, %{bench: false, days: []})

    runnables = for day <- config[:days], into: [] do
      module = String.to_existing_atom("Elixir.Aoc2021.Day#{day}")
      file = File.open!("input/day#{day}.txt", [:read, :utf8])
      input = IO.read(file, :all) |> String.split("\n")
      [ { "Day #{day} Part 1",  fn -> module.part1(input) end },
        { "Day #{day} Part 2",  fn -> module.part2(input) end } ]
    end |> List.flatten() |> Enum.into(%{})

    if config[:bench] do
      Benchee.run(runnables, warmup: 1, time: 3, parallel: 6 )
    else
      Enum.each(runnables, fn {name, fun} -> fun.() |> IO.inspect(label: name) end)
    end
  end
end
