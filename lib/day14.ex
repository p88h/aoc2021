defmodule Aoc2021.Day14 do
  def produce({{a, b}, x}, map, ret) when is_map_key(map, {a, b}) do
    c = map[{a, b}]
    ret = Map.update(ret, {a, c}, x, &(&1 + x))
    Map.update(ret, {c, b}, x, &(&1 + x))
  end
  def produce({{a, b}, x}, _map, ret), do: Map.update(ret, {a, b}, x, &(&1 + x))

  def polystep(counts, map), do: Enum.reduce(counts, %{}, fn p, ret -> produce(p, map, ret) end)
  def polyloop(l, _map, 0), do: l
  def polyloop(l, map, limit), do: polyloop(polystep(l, map), map, limit - 1)

  def process([tmpl, _ | t], limit) do
    ta = [th | tr] = String.graphemes(tmpl)
    map = for l <- t, into: %{} do
      [p, c] = String.split(l, " -> ")
      [a, b] = String.graphemes(p)
      {{a, b}, c}
    end
    polyloop(Enum.zip(ta, tr) |> Enum.frequencies(), map, limit)
    |> Enum.reduce(%{th => 1}, fn {{_a, b}, x}, r -> Map.update(r, b, x, &(&1 + x)) end)
    |> Enum.sort_by(&elem(&1, 1)) |> Enum.map(&elem(&1, 1))
    |> (fn l -> List.last(l) - hd(l) end).()
  end

  def part1(args), do: process(args, 10)
  def part2(args), do: process(args, 40)
end
