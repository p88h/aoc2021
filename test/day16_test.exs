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

defmodule Day16Test do
  use ExUnit.Case
  doctest Aoc2021.Day16
  import Aoc2021.Day16

  def input1, do: [ "D2FE28" ]
  def input2, do: [ "38006F45291200" ]
  def input3, do: [ "EE00D40C823060" ]
  def input4, do: [ "8A004A801A8002F478" ]
  def input5, do: [ "620080001611562C8802118E34" ]
  def input6, do: [ "C0015000016115A2E0802F182340" ]
  def input6, do: [ "A0016C880162017C3686B18A3D4780" ]

  test "part 1" do
    assert part1(input1()) == 6
    assert part1(input2()) == 1
    assert part1(input3()) == 14
    assert part1(input4()) == 16
    assert part1(input5()) == 12
    assert part1(input6()) == 23
    assert part1(input7()) == 31
  end

  test "part 2" do
    assert part2(input1()) == 6
    assert part2(input2()) == 1
    assert part2(input3()) == 14
    assert part2(input4()) == 16
    assert part2(input5()) == 12
    assert part2(input6()) == 23
    assert part2(input7()) == 31
  end
end
