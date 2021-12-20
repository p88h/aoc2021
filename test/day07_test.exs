defmodule Day07Test do
  use ExUnit.Case
  doctest Aoc2021.Day07
  import Aoc2021.Day07

  def input do
    [ "16,1,2,0,4,2,7,1,2,14" ]
  end

  test "part 1" do
    assert part1(input()) == 37
  end

  test "part 2" do
    assert part2(input()) == 168
  end
end
