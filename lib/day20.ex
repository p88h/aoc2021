defmodule Aoc2021.Day20 do
  def area(), do: [{-1,-1},{-1,0},{-1,1},{0,-1},{0,0},{0,1},{1,-1},{1,0},{1,1}]
  def iter(mat, _, _, step, _, step), do: Map.values(mat) |> Enum.map(&Map.values/1) |> List.flatten()
  def iter(mat, bits, size, step, dflt, maxstep) do
    mat = for y <- -step..size+step, into: %{} do
      { y, for x <- -step..size+step, into: %{} do
        fval = Enum.reduce(area(), 0, fn {dy,dx}, a -> 2*a + (mat[y+dy][x+dx] || dflt) end)
        {x, bits[fval] }
      end }
    end
    dflt = if dflt == 0, do: bits[0], else: bits[511]
    iter(mat, bits, size, step + 1, dflt, maxstep)
  end

  def hash_bits(s), do: Enum.map(String.graphemes(s), &(if &1 == "#", do: 1, else: 0))
  def indexed_map(l), do: for({v, k} <- Stream.with_index(l), into: %{}, do: {k, v})
  def run([rules, "" | lines], maxstep) do
    bits = hash_bits(rules) |> indexed_map()
    mat = Enum.map(lines, &hash_bits/1) |> Enum.map(&indexed_map/1) |> indexed_map()
    iter(mat, bits, length(lines), 1, 0, maxstep + 1)
  end

  def part1(args), do: run(args, 2) |> Enum.sum()
  def part2(args), do: run(args, 50) |> Enum.sum()
end
