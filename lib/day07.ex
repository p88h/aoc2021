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

defmodule Aoc2021.Day07 do
  def lnorm(a, b), do: abs(a-b)
  def enorm(a, b), do: div(abs(a-b)*(abs(a-b)+1),2)
  def dist(pp, c, norm), do: Enum.map(pp, &(norm.(&1, c))) |> Enum.sum()

  def gradient(pp, c, norm) do
    cond do
      dist(pp, c - 1, norm) < dist(pp, c, norm) -> gradient(pp, c - 1, norm)
      dist(pp, c + 1, norm) < dist(pp, c, norm) -> gradient(pp, c + 1, norm)
      true -> dist(pp, c, norm)
    end
  end

  def median(pp), do: Enum.at(pp, div(length(pp), 2))
  def mean(pp), do: div(Enum.sum(pp), length(pp))
  def run(args, norm, centroid) do
    pp = String.split(hd(args), ",") |> Enum.map(&String.to_integer/1) |> Enum.sort()
    gradient(pp, centroid.(pp), norm)
  end

  def part1(args), do: run(args, &lnorm/2, &median/1)
  def part2(args), do: run(args, &enorm/2, &mean/1)
end
