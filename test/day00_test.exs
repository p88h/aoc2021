defmodule Day00Test do
  use ExUnit.Case
  doctest Aoc2021.Day00
  import Aoc2021.Day00

  def input do
    [ "1", "2", "3", "4", "5", "6", "7", "8", "9", "10" ]
  end

  test "part 1" do
    assert part1(input()) == 10
  end

  test "part 2" do
    assert part2(input()) == 55
  end
end
