defmodule Aoc2021.Day06 do
  def rep(m, 0, _), do: Enum.sum(Map.values(m))
  def rep(m, c, o), do: rep(%{m | rem(o + 7, 9) => m[rem(o + 7, 9)] + m[rem(o, 9)] }, c - 1, o + 1)

  def csv(line), do: String.split(line, ",") |> Enum.map(&String.to_integer/1)
  def init_map(), do: for x <- 0..8, into: %{}, do: {x, 0}
  def process(args), do: Enum.reduce(args, init_map(), &(%{&2 | &1 => &2[&1] + 1}))

  def part1(args), do: process(csv(hd(args))) |> rep(80, 0)
  def part2(args), do: process(csv(hd(args))) |> rep(256, 0)
end
