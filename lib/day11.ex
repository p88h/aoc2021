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

defmodule Aoc2021.Day11 do

  def mapmap(l), do: for({v, k} <- Stream.with_index(l), into: %{}, do: {k, v})

  def load(args) do
    lol = Enum.map(args, fn l -> String.graphemes(l) |> Enum.map(&String.to_integer/1) end)
    { h, w } = { length(lol), length(hd(lol)) }
    idx = for i <- 0..(h - 1), j <- 0..(w - 1), into: [], do: {i,j}
    { h, w, idx, Enum.map(lol, &mapmap/1) |> mapmap() }
  end

  def inc(idx, m), do: Enum.reduce(idx, m, fn {i,j},mt -> put_in(mt[i][j],mt[i][j]+1) end)
  def zero(idx, m), do: Enum.reduce(idx, m, fn {i,j},mt -> put_in(mt[i][j],0) end)
  def scan(idx, m), do: Enum.filter(idx, fn {i,j} -> m[i][j] == 10 end)
  def neigh(i, j), do: [ {i-1,j-1},{i,j-1},{i+1,j-1},{i-1,j},{i+1,j},{i-1,j+1},{i,j+1},{i+1,j+1} ]
  def bound(l, h, w), do: Enum.filter(l, fn {i,j} -> i >= 0 and j >=0 and i < h and j < w end)
  def nb(i,j,h,w), do: bound(neigh(i,j), h, w)

  def flash([], map, _h, _w), do: map
  def flash([{i,j} | t], map, h, w) do
    next = nb(i,j,h,w) |> Enum.filter(fn {i, j} -> map[i][j] < 10 end)
    map = inc(next, map)
    f = scan(next, map)
    flash(f ++ t, map, h, w)
  end

  def step(_p, max, max, res), do: res
  def step({ h, w, idx, map }, cnt, max, res) do
    map = inc(idx, map)
    flashing = scan(idx, map)
    map = flash(flashing, map, h, w)
    flashed = scan(idx, map)
    map = zero(flashed, map)
    fc = length(flashed)
    if fc == h*w, do: cnt + 1, else: step({ h, w, idx, map }, cnt + 1, max, res + fc)
  end

  def part1(args), do: load(args) |> step(0, 100, 0)
  def part2(args), do: load(args) |> step(0, 1000, 0)
end
