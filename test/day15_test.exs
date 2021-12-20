defmodule Day15Test do
  use ExUnit.Case
  doctest Aoc2021.Day15
  import Aoc2021.Day15

  def input do
    [ "1163751742",
      "1381373672",
      "2136511328",
      "3694931569",
      "7463417111",
      "1319128137",
      "1359912421",
      "3125421639",
      "1293138521",
      "2311944581" ]
  end

  test "part 1" do
    assert part1(input()) == 40
  end

  test "part 2" do
    assert part2(input()) == 315
  end
end
