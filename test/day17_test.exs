defmodule Day17Test do
  use ExUnit.Case
  doctest Aoc2021.Day17
  import Aoc2021.Day17

  def input do
    [ "target area: x=20..30, y=-10..-5" ]
  end

  test "part 1" do
    assert part1(input()) == 45
  end

  test "part 2" do
    assert part2(input()) == 112
  end
end
