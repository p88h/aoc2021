defmodule Aoc2021.Day01 do
  def tail1([a, b | tail ], acc) do
    tmp = if a < b do acc+1 else acc end
    tail1([ b | tail ], tmp)
  end

  def tail1(_ , acc) do
    acc
  end

  def part1(args) do
    args |> Enum.map(&String.to_integer/1)
         |> tail1(0)
  end

  def tail2([a, b, c, d | tail ], acc) do
    tmp = if a < d do acc+1 else acc end
    tail2([ b, c, d | tail ], tmp)
  end

  def tail2(_ , acc) do
    acc
  end

  def part2(args) do
    args |> Enum.map(&String.to_integer/1)
         |> tail2(0)
  end
end
