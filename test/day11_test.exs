defmodule Day11Test do
  use ExUnit.Case
  doctest Aoc2021.Day11
  import Aoc2021.Day11

  def input do
    [ "5483143223",
      "2745854711",
      "5264556173",
      "6141336146",
      "6357385478",
      "4167524645",
      "2176841721",
      "6882881134",
      "4846848554",
      "5283751526" ]
  end

  test "part 1" do
    assert part1(input()) == 1656
  end

  test "part 2" do
    assert part2(input()) == 195
  end
end
