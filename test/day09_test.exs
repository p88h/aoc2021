defmodule Day09Test do
  use ExUnit.Case
  doctest Aoc2021.Day09
  import Aoc2021.Day09

  def input do
    [ "2199943210",
      "3987894921",
      "9856789892",
      "8767896789",
      "9899965678" ]
  end

  test "part 1" do
    assert part1(input()) == 15
  end

  test "part 2" do
    assert part2(input()) == 1134
  end
end
