defmodule Day12Test do
  use ExUnit.Case
  doctest Aoc2021.Day12
  import Aoc2021.Day12

  def input1 do
    [ "start-A",
      "start-b",
      "A-c",
      "A-b",
      "b-d",
      "A-end",
      "b-end" ]
  end
  def input2 do
  [ "dc-end",
    "HN-start",
    "start-kj",
    "dc-start",
    "dc-HN",
    "LN-dc",
    "HN-end",
    "kj-sa",
    "kj-HN",
    "kj-dc" ]
  end
  def input3 do
    [ "fs-end",
      "he-DX",
      "fs-he",
      "start-DX",
      "pj-DX",
      "end-zg",
      "zg-sl",
      "zg-pj",
      "pj-he",
      "RW-he",
      "fs-DX",
      "pj-RW",
      "zg-RW",
      "start-pj",
      "he-WI",
      "zg-he",
      "pj-fs",
      "start-RW" ]
  end

  test "part 1" do
    assert part1(input1()) == 10
    assert part1(input2()) == 19
    assert part1(input3()) == 226
  end

  test "part 2" do
    assert part2(input1()) == 36
    assert part2(input2()) == 103
    assert part2(input3()) == 3509
  end
end
