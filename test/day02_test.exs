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

defmodule Day02Test do
  use ExUnit.Case
  doctest Aoc2021.Day02
  import Aoc2021.Day02

  def input do
    [ "forward 5",
      "down 5",
      "forward 8",
      "up 3",
      "down 8",
      "forward 2" ]
  end

  test "part 1" do
    assert part1(input()) == 150
  end

  test "part 2" do
    assert part2(input()) == 900
  end
end
