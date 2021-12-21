defmodule Aoc2021.Day05 do
  def parse(args) do
    args |> Enum.map(fn x -> String.replace(x, " -> ",",") end)
         |> Enum.map(fn x -> String.split(x, ",") |> Enum.map(&String.to_integer/1) end)
  end

  def next(a, a), do: a
  def next(a, b), do: if a < b, do: a + 1, else: a - 1

  def plot([a, b, a, b], acc), do: [ {a,b} | acc ]
  def plot([a, b, c, d], acc), do: plot([next(a, c), next(b, d), c, d ], [ {a,b} | acc ] )

  def solve(l), do: Enum.reduce(l, [], &plot/2) |> Enum.frequencies() |> Enum.count(&(elem(&1,1)>1))

  def part1(args), do: parse(args) |> Enum.filter(fn [a,b,c,d] -> a == c or b == d end) |> solve()
  def part2(args), do: parse(args) |> solve()
end
