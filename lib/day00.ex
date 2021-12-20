defmodule Aoc2021.Day00 do
  def part1(args) do
    args |> Enum.reduce(0, fn _, acc -> acc + 1 end)
  end

  def part2(args) do
    args |> Enum.reduce(0, fn x, acc -> acc + String.to_integer(x) end)
  end
end
