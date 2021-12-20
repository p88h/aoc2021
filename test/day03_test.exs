defmodule Day03Test do
  use ExUnit.Case
  doctest Aoc2021.Day03
  import Aoc2021.Day03

  def input do
    [ "00100","11110","10110","10111","10101","01111","00111","11100","10000","11001","00010","01010" ]
  end

  test "part 1" do
    assert part1(input()) == 198
  end

  test "part 2" do
    assert part2(input()) == 230
  end
end
