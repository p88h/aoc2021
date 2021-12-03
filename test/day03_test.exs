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
