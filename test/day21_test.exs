defmodule Day21Test do
  use ExUnit.Case
  doctest Aoc2021.Day21
  import Aoc2021.Day21

  def input do
    [ "Player 1 starting position: 4",
      "Player 2 starting position: 8" ]
  end

  test "part 1" do
    assert part1(input()) == 739785
  end

  test "part 2" do
    assert part2(input()) == 444356092776315
  end
end
