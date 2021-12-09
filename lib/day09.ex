# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

defmodule Aoc2021.Day09 do
  def indexed_map(l), do: for {v,k} <- Stream.with_index(l), into: %{}, do: {k,v}

  def load(args) do
    lol = Enum.map(args, fn l -> String.graphemes(l) |> Enum.map(&String.to_integer/1) end)
    {length(lol), length(hd(lol)), Enum.map(lol, &indexed_map/1) |> indexed_map() }
  end

  def part1(args) do
    {h, w, mat} = load(args)
    for i <- 0..h-1, j <- 0..w-1 do
      if (i == 0 or mat[i-1][j] > mat[i][j]) and
         (i == h-1 or mat[i+1][j] > mat[i][j]) and
         (j == 0 or mat[i][j-1] > mat[i][j]) and
         (j == w-1 or mat[i][j+1] > mat[i][j]) do
          {i,j,mat[i][j]}
        end
    end |> Enum.filter(&(&1 != nil)) |> Enum.map(fn {_,_,v} -> v+1 end ) |> Enum.sum()
  end

  def find(map, a) do
    if map[a] != a do
      {parent, map} = find(map, map[a])
      {parent, %{map | a => parent }}
    else
      { map[a], map }
    end
  end

  def union(map, a, b) do
    {a, map} = find(map, a)
    {b, map} = find(map, b)
    if a == b, do: map, else: %{map | a => b}
  end

  @spec top3prod(nonempty_maybe_improper_list) :: number
  def top3prod([ _ , {_, a}, { _, b }, { _, c} | _]), do: a*b*c

  def part2(args) do
    {h, w, mat} = load(args)
    map = for i <- 0..h-1, j <- 0..w-1, into: %{}, do: {{i,j}, {i,j}}
    map = Enum.reduce(Map.keys(map), map, fn {i,j}, m ->
      m = if mat[i][j] < 9 and j > 0 and mat[i][j-1] < 9, do: union(m,{i,j}, {i,j-1}), else: m
      if mat[i][j] < 9 and i > 0 and mat[i-1][j] < 9, do: union(m,{i,j}, {i,j-1}), else: m
    end)
    map = Enum.reduce(Map.keys(map), map, fn {i,j}, m -> elem(find(m,{i, j}),1) end)
    for i <- 0..h-1, j <- 0..w-1 do
      if mat[i][j] < 9, do: map[i*w+j], else: -1
    end |> Enum.frequencies() |> Enum.sort_by(&(-elem(&1,1))) |> top3prod()
  end
end
