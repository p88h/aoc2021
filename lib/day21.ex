defmodule Aoc2021.Day21 do
  def parse(line), do: String.split(line, ": ") |> Enum.at(1) |> String.to_integer()

  def iter([p1, p2], [s1, s2], ofs, cnt) do
    p1 = rem(p1+rem(ofs, 100)+rem(ofs+1,100)+rem(ofs+2,100)+2,10)+1
    ofs = rem(ofs + 3, 100)
    cnt = cnt + 3
    s1 = s1 + p1
    if s1 >= 1000, do: s2*cnt, else: iter([p2, p1], [s2, s1], ofs, cnt)
  end

  def part1(args), do: Enum.map(args, &parse/1) |> iter([0,0],0,0)

  def addstate({{_p1, _p2, s1, _s2}, c}, {ret, w1, w2}) when s1 >= 21, do: { ret, w1 + c, w2 }
  def addstate({{p1, p2, s1, s2}, c}, {ret, w1, w2}) do
    { Map.update(ret, {p2, p1, s2, s1}, c, &(&1+c)), w1, w2 }
  end

  def produce3({{p1, p2, s1, s2}, c}, {ret, w1, w2}) do
    quants = for {d,f} <- [{6, 7},{5, 6},{7, 6},{4, 3},{8, 3},{3, 1},{9, 1}] do
      np = rem(p1 + d - 1, 10) + 1
      {{np, p2, s1+np, s2}, c * f}
    end
    Enum.reduce(quants, {ret, w1, w2}, &addstate/2)
  end

  def iter2([p1, p2]), do: iter2({%{{p1,p2,0,0} => 1}, 0, 0})
  def iter2({multiverse, win1, win2}) when multiverse == %{}, do: max(win1, win2)
  def iter2({multiverse, win1, win2}), do: iter2(Enum.reduce(multiverse, {%{}, win2, win1}, &produce3/2 ))

  def part2(args), do: Enum.map(args, &parse/1) |> iter2()
end
