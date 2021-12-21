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

  def addstate({{_p, s}, c}, {ret, [ w | t ]}) when s >= 21, do: { ret, [ w + c | t ] }
  def addstate({{p, s}, c}, {ret, wins}), do: { Map.update(ret, {p, s}, c, &(&1+c)), wins }

  def produce3({{p, s}, c}, {ret, wins}) do
    quants = for {d,f} <- [{6, 7},{5, 6},{7, 6},{4, 3},{8, 3},{3, 1},{9, 1}] do
      np = rem(p + d - 1, 10) + 1
      {{np, s+np}, c * f}
    end
    Enum.reduce(quants, {ret, wins}, &addstate/2)
  end

  def iter2({multiverse, wins}) when multiverse == %{}, do: Enum.reverse(wins)
  def iter2({multiverse, wins}), do: iter2(Enum.reduce(multiverse, {%{}, [ 0 | wins]}, &produce3/2 ))

  def compute([], [], _, _, r1, r2), do: max(r1, r2)
  def compute([w1 | t1], [w2 | t2], s1, s2, r1, r2) do
    s1 = s1 * 27 - w1
    r1 = r1 + w1 * s2
    s2 = s2 * 27 - w2
    r2 = r2 + w2 * s1
    compute(t1, t2, s1, s2, r1, r2)
  end

  def iter3([p1, p2]), do: compute(iter2({%{{p1,0}=> 1}, []}),iter2({%{{p2,0}=> 1}, []}), 1, 1, 0, 0)

  def part2(args), do: Enum.map(args, &parse/1) |> iter3()
end
