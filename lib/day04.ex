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
