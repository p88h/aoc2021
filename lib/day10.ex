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

defmodule Aoc2021.Day10 do
  def stack([c | t], s, m, z1, z2) when is_map_key(m, c), do: stack(t, [m[c] | s], m, z1, z2)
  def stack([], s, _, _, z2), do: {0, Enum.reduce(s, 0, fn x, a -> a * 5 + z2[x] end)}
  def stack([c | t], [c | r], m, z1, z2), do: stack(t, r, m, z1, z2)
  def stack([c | _], _, _, z1, _), do: {z1[c], 0}

  def process(args, ofs) do
    m = %{"(" => ")", "[" => "]", "{" => "}", "<" => ">"}
    z1 = %{")" => 3, "]" => 57, "}" => 1197, ">" => 25137}
    z2 = %{")" => 1, "]" => 2, "}" => 3, ">" => 4}
    Enum.map(args, &String.graphemes/1)
    |> Enum.map(&elem(stack(&1, [], m, z1, z2), ofs))
    |> Enum.reject(&(&1 == 0))
  end

  def part1(args), do: process(args, 0) |> Enum.sum()
  def middle(lst), do: Enum.sort(lst) |> Enum.at(div(length(lst), 2))
  def part2(args), do: process(args, 1) |> middle()
end
