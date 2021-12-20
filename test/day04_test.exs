# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

defmodule Day04Test do
  use ExUnit.Case
  doctest Aoc2021.Day04
  import Aoc2021.Day04

  def input do
    [ "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1",
      "",
      "22 13 17 11  0",
      "8  2 23  4 24",
      "21  9 14 16  7",
      "6 10  3 18  5",
      "1 12 20 15 19",
      "",
      "3 15  0  2 22",
      "9 18 13 17  5",
      "19  8  7 25 23",
      "20 11 10 24  4",
      "14 21 16 12  6",
      "",
      "14 21 17 24  4",
      "10 16 15  9 19",
      "18  8 23 26 20",
      "22 11 13  6  5",
      "2  0 12  3  7" ]
  end

  test "part 1" do
    assert part1(input()) == 4512
  end

  test "part 2" do
    assert part2(input()) == 1924
  end
end
