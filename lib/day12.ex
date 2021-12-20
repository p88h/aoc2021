defmodule Aoc2021.Day12 do
  def cost(<<f, _::binary>>), do: if f >= 65 and f <= 90, do: 0, else: 1
  def process(args) do
    args |> Enum.map(fn x -> String.split(x, "-") end)
         |> Enum.map(fn [a, b] -> [{a,b}, {b,a}] end)
         |> List.flatten() |> Enum.sort()
         |> Enum.reduce(%{}, fn {a,b}, m -> Map.put(m, a, [ b | Map.get(m, a, []) ]) end)
  end

  def explore(map, node, visited, max, path) do
    visited = Map.put(visited, node, Map.get(visited, node, 0) + cost(node))
    max = if visited[node] == 2 and node != "start", do: 1, else: max
    path = [ node | path ]
    if node == "end" do
      1
    else
      next = Enum.filter(map[node], fn x -> Map.get(visited, x, 0) < max end)
      Enum.map(next, &explore(map, &1, visited, max, path)) |> Enum.sum()
    end
  end

  def part1(args), do: process(args) |> explore("start", %{}, 1, [])
  def part2(args), do: process(args) |> explore("start", %{"start" => 1}, 2, [])
end
