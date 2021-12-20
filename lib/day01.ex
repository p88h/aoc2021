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
