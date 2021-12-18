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

defmodule Aoc2021.Day18 do
  def parse(s) when is_bitstring(s), do: parse(String.graphemes(s)) |> elem(0)
  def parse(["[" | t]) do
    {left, ["," | t]} = parse(t)
    {right, ["]" | t]} = parse(t)
    {[left, right], t}
  end
  def parse([x | t]), do: {String.to_integer(x), t}

  def inc([l, r], v, 0), do: [inc(l, v, 0), r]
  def inc([l, r], v, 1), do: [l, inc(r, v, 1)]
  def inc(x, v, _), do: x + v

  def split([l, r]) do
    {l, s} = split(l)
    if not s do
      {r, s} = split(r)
      {[l, r], s}
    else
      {[l, r], s}
    end
  end
  def split(x), do: if x < 10, do: {x, false}, else: {[trunc(x / 2), x - trunc(x / 2)], true}

  def explode([l, r], 4), do: {true, 0, l, r}
  def explode([l, r], d) do
    {e, l, a, b} = explode(l, d + 1)
    if not e do
      {e, r, a, b} = explode(r, d + 1)
      if e and a > 0 do
        {e, [inc(l, a, 1), r], -1, b}
      else
        {e, [l, r], a, b}
      end
    else
      if b > 0 do
        {e, [l, inc(r, b, 0)], a, -1}
      else
        {e, [l, r], a, b}
      end
    end
  end
  def explode(x, _), do: {false, x, -1, -1}

  def fixup(t) do
    {e, t, _a, _b} = explode(t, 0)
    if not e do
      {t, s} = split(t)
      if s, do: fixup(t), else: t
    else
      fixup(t)
    end
  end

  def mag([l, r]), do: 3*mag(l)+2*mag(r)
  def mag(x), do: x

  def add(b, a), do: fixup([a, b])
  def varsums(l), do: for a <- l, b <- l, a != b, do: mag(add(a,b))

  def part1(args), do: Enum.map(args, &parse/1) |> Enum.reduce(&add/2) |> mag()

  def part2(args), do: Enum.map(args, &parse/1) |> varsums() |> Enum.max()
end
