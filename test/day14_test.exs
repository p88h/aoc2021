defmodule Day14Test do
  use ExUnit.Case
  doctest Aoc2021.Day14
  import Aoc2021.Day14

  def input do
    [ "NNCB",
      "",
      "CH -> B",
      "HH -> N",
      "CB -> H",
      "NH -> C",
      "HB -> C",
      "HC -> B",
      "HN -> C",
      "NN -> C",
      "BH -> H",
      "NC -> B",
      "NB -> B",
      "BN -> B",
      "BB -> N",
      "BC -> B",
      "CC -> N",
      "CN -> C" ]
  end

  test "part 1" do
    assert part1(input()) == 1588
  end

  test "part 2" do
    assert part2(input()) == 2188189693529
  end
end
