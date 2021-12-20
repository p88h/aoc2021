defmodule Aoc2021.Day09 do
  def indexed_map(l), do: for({v, k} <- Stream.with_index(l), into: %{}, do: {k, v})

  def load(args) do
    lol = Enum.map(args, fn l -> String.graphemes(l) |> Enum.map(&String.to_integer/1) end)
    {length(lol), length(hd(lol)), Enum.map(lol, &indexed_map/1) |> indexed_map()}
  end

  def part1(args) do
    {h, w, mat} = load(args)
    for i <- 0..(h - 1), j <- 0..(w - 1) do
      if (i == 0 or mat[i - 1][j] > mat[i][j]) and
         (i == h - 1 or mat[i + 1][j] > mat[i][j]) and
         (j == 0 or mat[i][j - 1] > mat[i][j]) and
         (j == w - 1 or mat[i][j + 1] > mat[i][j]) do
        mat[i][j] + 1
      end
    end|> Enum.reject(&is_nil/1) |> Enum.sum()
  end

  def find(map, a) do
    if map[a] != a do
      {parent, map} = find(map, map[a])
      {parent, %{map | a => parent}}
    else
      {map[a], map}
    end
  end

  def union(map, a, b) do
    {a, map} = find(map, a)
    {b, map} = find(map, b)
    if a == b, do: map, else: %{map | a => b}
  end

  def part2(args) do
    {h, w, mat} = load(args)
    map = for i <- 0..(h - 1), j <- 0..(w - 1), into: %{}, do: {{i, j}, {i, j}}
    map = Enum.reduce(Map.keys(map), map, fn {i, j}, m ->
      m = if mat[i][j] < 9 and j > 0 and mat[i][j - 1] < 9, do: union(m, {i, j}, {i, j - 1}), else: m
      if mat[i][j] < 9 and i > 0 and mat[i - 1][j] < 9, do: union(m, {i, j}, {i - 1, j}), else: m
    end)
    map = Enum.reduce(Map.keys(map), map, fn t, m -> elem(find(m, t), 1) end)
    roots = for i <- 0..(h - 1), j <- 0..(w - 1), do: if (mat[i][j] < 9), do: map[{i, j}]
    Enum.reject(roots, &is_nil/1) |> Enum.frequencies() |> Enum.sort_by(&(-elem(&1, 1)))
      |> Enum.map(&elem(&1, 1)) |> Enum.chunk_every(3) |> hd() |> Enum.product()
  end
end
