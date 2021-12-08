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

use Bitwise

defmodule Aoc2021.Day08 do

  def pattern(x), do: case x, do: (0->0b1110111; 1->0b0010010; 2->0b1011101; 3->0b1011011; 4->0b0111010;
                                   5->0b1101011; 6->0b1101111; 7->0b1010010; 8->0b1111111; 9->0b1111011 )
  def classes(s), do: case String.length(s), do: (2->[1]; 3->[7]; 4->[4]; 5->[2,3,5]; 6->[0,6,9]; 7->[8])
  def initmap(), do: for c <- String.graphemes("abcdefg"), into: %{}, do: { c, 0b1111111 }

  def single(1), do: true
  def single(0), do: false
  def single(bits) when (bits &&& 1) != 0, do: false
  def single(bits), do: single(bits >>> 1)

  def allsingle(vals), do: Enum.all?(vals, &single/1)
  def allbits(vals), do: Enum.reduce(vals, &(&1 ||| &2)) == 0b1111111
  def noempty(vals), do: not Enum.any?(vals, &(&1 == 0))
  def valid(vals), do: allbits(vals) and noempty(vals)

  def updatemap([ ], _, map), do: map
  def updatemap([ h | t ], bits, map), do: updatemap(t, bits, %{map | h => map[h] &&& bits })

  def resolve(map, done) do
    p = Enum.find(map, fn {_,v} -> (done &&& v) == 0 and single(v) end)
    if p != nil do
      {k, v} = p
      negv = bxor(0b1111111, v)
      updated = for {l,w} <- map, into: %{}, do: ( if k == l, do: {l,w}, else: {l, w &&& negv })
      resolve(updated, done ||| v)
    else
      map
    end
  end

  def descramble([], map, _, result), do: if allsingle(Map.values(map)), do: result
  def descramble([ h | t ], map, used, result) do
    solns = for n <- classes(h) do
      if (used &&& (1 <<< n)) == 0 do
        new_map = resolve(updatemap(String.graphemes(h), pattern(n), map), 0)
        if valid(Map.values(new_map)) do
          descramble(t, new_map, used ||| (1 <<< n), [ {h, n} | result ])
        end
      end
    end
    Enum.filter(solns, &(&1 != nil))
  end

  def sorted(s), do: List.to_string(Enum.sort(String.graphemes(s)))
  def unpack2(s), do: String.split(s) |> Enum.map(&sorted/1)
  def unpack1(s), do: String.split(s, " | ") |> Enum.map(&unpack2/1)

  def part1(args) do
    args |> Enum.map(&unpack1/1)
         |> Enum.map(fn [_, b] -> Enum.count(b, &( length(classes(&1))==1 )) end)
         |> Enum.sum()
  end

  def handle1([a,b]) do
    map = Enum.into(List.flatten(descramble(a, initmap(), 0, [])), %{})
    Enum.reduce(b, 0, fn s, acc -> acc*10 + map[s] end)
  end

  def part2(args) do
    args |> Enum.map(&unpack1/1) |> Enum.map(&handle1/1) |> Enum.sum()
  end
end
