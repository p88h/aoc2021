defmodule Day13Test do
  use ExUnit.Case
  doctest Aoc2021.Day13
  import Aoc2021.Day13

  def input do
    [ "6,10",
      "0,14",
      "9,10",
      "0,3",
      "10,4",
      "4,11",
      "6,0",
      "6,12",
      "4,1",
      "0,13",
      "10,12",
      "3,4",
      "3,0",
      "8,4",
      "1,10",
      "2,14",
      "8,10",
      "9,0",
      "",
      "fold along y=7",
      "fold along x=5" ]
  end

  test "part 1" do
    assert part1(input()) == 17
  end

  test "part 2" do
    assert part2(input()) == "▯"
  end
end
