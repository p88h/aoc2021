defmodule Day02Test do
  use ExUnit.Case
  doctest Aoc2021.Day02
  import Aoc2021.Day02

  def input do
    [ "forward 5",
      "down 5",
      "forward 8",
      "up 3",
      "down 8",
      "forward 2" ]
  end

  test "part 1" do
    assert part1(input()) == 150
  end

  test "part 2" do
    assert part2(input()) == 900
  end
end
