defmodule Day01Test do
  use ExUnit.Case
  doctest Aoc2021.Day01
  import Aoc2021.Day01

  def input do
    [ "199", "200", "208", "210", "200", "207", "240", "269", "260", "263" ]
  end

  test "part 1" do
    assert part1(input()) == 7
  end

  test "part 2" do
    assert part2(input()) == 5
  end
end
