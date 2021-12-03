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

defmodule Aoc2021.Day03 do

  def str_to_nums(s), do: String.graphemes(s) |> Enum.map(fn x -> if x == "0" do -1 else 1 end end)
  def sum_lists(a,b), do: Enum.zip(a,b) |> Enum.map(fn {a,b} -> a + b end)

  def gamma_epsilon(l) do
    bits = Enum.map(l, fn x -> if x > 0 do 1 else 0 end end)
    gamma = Enum.reduce(bits, 0, fn x, acc -> acc * 2 + x end)
    epsilon = Enum.reduce(bits, 0, fn x, acc -> acc * 2 + 1 - x end)
    gamma * epsilon
  end

  def part1(args) do
    args |> Enum.map(&str_to_nums/1)
         |> Enum.reduce(&sum_lists/2)
         |> gamma_epsilon()
  end

  def filter(single = [ _ ], _ ), do: single
  def filter(llp, mode) do
    sum_first = Enum.reduce(llp, 0, fn x, acc -> acc + hd(x) end)
    Enum.filter(llp, fn x -> ((sum_first >= 0) == mode) == (hd(x) >= 0) end)
  end

  def filter_rec( [[]],  _, acc ), do: acc
  def filter_rec( llp = [ _ | _ ],  mode, acc ) do
    more = filter(llp, mode)
    bit = if hd(hd(more)) >= 0 do 1 else 0 end
    filter_rec(Enum.map(more, &tl/1), mode, acc * 2 + bit)
  end

  def part2(args) do
    prep = Enum.map(args, &str_to_nums/1)
    oxy = filter_rec(prep, true, 0)
    co2 = filter_rec(prep, false, 0)
    oxy * co2
  end
end
