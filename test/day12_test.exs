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

defmodule Day00Test do
  use ExUnit.Case
  doctest Aoc2021.Day00
  import Aoc2021.Day00

  def input1, do: [ "start-A","start-b","A-c","A-b","b-d","A-end","b-end" ]
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
    assert part2(input1()) == 0
  end
end
