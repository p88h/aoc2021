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

defmodule Aoc2021.Day04 do
  def mark({bits, played, map}, card) when is_map_key(map, card) do
    {(bits ||| (1 <<< map[card])), [ card | played ], map }
  end
  def mark(hand, _), do: hand

  def won({bits, _, _}) do
    [ 31, 992, 31744, 1015808, 32505856, 1082401, 2164802, 4329604, 8659208, 17318416 ]
    |> Enum.any?(fn p -> (bits &&& p) == p end)
  end

  def score({ _, played, map }, card), do: (Enum.sum(Map.keys(map)) - Enum.sum(played)) * card

  def play([], _, acc), do: List.flatten(acc)
  def play(hands1, [ card | tail ], acc) do
    { winning, losing } = Enum.map(hands1, fn hand -> mark(hand, card) end ) |> Enum.split_with(&won/1)
    play(losing, tail, [ Enum.map(winning, fn x -> score(x, card) end) | acc ])
  end

  def process([ first , _ | rest ]) do
    nums = String.split(first, ",") |> Enum.map(&String.to_integer/1)
    hands = Enum.chunk_every(rest, 5, 6, :discard) |> Enum.map(fn x -> Enum.map(x, fn y -> String.split(y)
         |> Enum.map(&String.to_integer/1) end) |> List.flatten() |> Enum.with_index() |> Map.new()
         |> (fn map -> {0, [], map} end).() end)
    [ hands, nums, [] ]
  end

  def part1(args), do: List.last(apply(Aoc2021.Day04, :play, process(args)))

  def part2(args), do: hd(apply(Aoc2021.Day04, :play, process(args)))
end
