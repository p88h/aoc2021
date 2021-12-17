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

defmodule Aoc2021.Day17 do
  def try_run(v, x, t), do: if t < x, do: try_run(v-1,x, t+v), else: { v, t }
  def yvrange(vx, x0, x1, _y0, y1, td) when td >= x0 and td <= x1 do
    xsmin = vx - trunc(:math.sqrt((td-x0)*2))
    for ys <- trunc(y1/xsmin + (xsmin-1)/2 - 1)..(-y1), into: [], do: {vx, ys}
  end
  def yvrange(vx, x0, x1, y0, y1, td) when td > x1 do
    { v1, t1 } = try_run(vx, x0, 0)
    { v2, _ } = try_run(v1, x1 + 1, t1)
    xsmin = vx - v1
    xsmax = vx - v2
    for ys <- trunc(y1/xsmin + (xsmin-1)/2 - 1)..trunc(y0/xsmax + (xsmax+1)/2), into: [], do: {vx, ys}
  end
  def yvrange(_vx, _x0, _x1, _y0, _y1, _td), do: []

  def shoot({_vx, _vy}, x0, x1, y0, y1, x, y, m) when x >= x0 and x <= x1 and y >= y1 and y <= y0, do: m
  def shoot({vx, _vy}, x0, x1, _y0, y1, x, y, _m) when (vx == 0 and x < x0) or x > x1 or y < y1, do: nil
  def shoot({vx, vy}, x0, x1, y0, y1, x, y, m) do
    shoot({max(0, vx-1), vy-1}, x0, x1, y0, y1, x + vx, y + vy, max(y,m))
  end

  def handle(args) do
    [ x0, x1, y1, y0 ] = Regex.run(~r/target area: x=(\d+)..(\d+), y=(-?\d+)..(-?\d+)/, hd(args)) |> tl()
                      |> Enum.map(&String.to_integer/1)
    xrange = for vx <- trunc(:math.sqrt(x0*2))..x1, into: [], do: vx
    Enum.map(xrange, &yvrange(&1, x0, x1, y0, y1, &1 * (&1 + 1) / 2)) |> List.flatten() |> Enum.map(&shoot(&1,x0,x1,y0,y1,0,0,0))
  end

  def part1(args), do: handle(args) |> Enum.reject(&is_nil/1) |> Enum.max()
  @spec part2(nonempty_maybe_improper_list) :: non_neg_integer
  def part2(args), do: handle(args) |> Enum.reject(&is_nil/1) |> Enum.count()
end
