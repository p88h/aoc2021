defmodule Aoc2021.Day19 do
  def parse(l), do: Enum.map(tl(l), fn x -> String.split(x, ",") |> Enum.map(&String.to_integer/1) end)
  def prep(args), do: Enum.chunk_by(args, &(&1=="")) |> Enum.reject(&(&1==[""])) |> Enum.map(&parse(&1))

  def delta([x1,y1,z1],[x2,y2,z2]), do: abs(x2-x1)+abs(y2-y1)+abs(z2-z1)
  def shift([x1,y1,z1],[x2,y2,z2]), do: [x2-x1,y2-y1,z2-z1]
  def shiftv(l, d), do: Enum.map(l, &shift(d, &1))

  def pick(l, rot), do: Enum.at(l, abs(rot)-1)*div(rot, abs(rot))
  def rotate([], _), do: []
  def rotate([ h | t ], r=[r0,r1,r2]), do: [[pick(h,r0), pick(h,r1), pick(h,r2)] | rotate(t,r)]

  def try_align(_l, _r, 4, [], ba, ea), do: { Enum.reverse(ea), Enum.reverse(ba) }
  def try_align(l, r, d, el, ba, ea) do
    p = Enum.map(l, &pick(&1, d))
    for e <- el, s <- [-1,1] do
      t = Enum.map(r, &pick(&1, e*s))
      w = for a <- p, b <- t, do: b-a
      {best, freq} = Enum.frequencies(w) |> Enum.max_by(&(elem(&1,1)))
      if freq >= 12 do
        try_align(l,r,d+1, Enum.reject(el, &(&1==e)), [ best | ba ], [e*s | ea])
      end
    end
  end

  def align_next(_, [], good, bad, pos), do: { good, bad, pos }
  def align_next(next, [ h | t ], good, bad, pos ) do
    rd = try_align(next, h, 1, [1,2,3], [],[]) |> List.flatten() |> Enum.find(&(not is_nil(&1)))
    case rd do
      { rot, diff } -> align_next(next, t, [ shiftv(rotate(h,rot),diff) | good], bad, [ diff | pos ])
      nil -> align_next(next, t, good, [ h | bad ], pos)
    end
  end

  def align_all(done, aligned, []), do: Enum.concat(done,aligned)
  def align_all(done, [ next | t ], rest) do
    {new, rest, _} = align_next(next, rest, [], [], [])
    align_all([ next | done ], Enum.concat(new, t), rest)
  end

  def part1(args) do
    scans = prep(args)
    beacons = Enum.concat(align_all([], [ hd(scans) ], tl(scans)))
    beacons |> Enum.frequencies() |> Map.keys() |> Enum.count()
  end

  def align_all2(pos, _, []), do: pos
  def align_all2(pos, [ next | t ], rest) do
    {new, rest, npos} = align_next(next, rest, [], [], [])
    align_all2(Enum.concat(pos, npos), Enum.concat(new, t), rest)
  end

  def part2(args) do
    scans = prep(args)
    pos = align_all2([[0,0,0]], [ hd(scans) ], tl(scans))
    distances = for a <- pos, b <- pos, into: [], do: delta(a,b)
    Enum.max(distances)
  end
end
