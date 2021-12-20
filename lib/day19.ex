defmodule Aoc2021.Day19 do
  def parse(l), do: Enum.map(tl(l), fn x -> String.split(x, ",") |> Enum.map(&String.to_integer/1) end)
  def prep(args), do: Enum.chunk_by(args, &(&1=="")) |> Enum.reject(&(&1==[""])) |> Enum.map(&parse(&1))

  def rots(), do: [[-3, -2, -1], [-3, -1, 2], [-3, 1, -2], [-3, 2, 1],
                   [-2, -3, 1], [-2, -1, -3], [-2, 1, 3], [-2, 3, -1],
                   [-1, -3, -2], [-1, -2, 3], [-1, 2, -3], [-1, 3, 2],
                   [1, -3, 2], [1, -2, -3], [1, 2, 3], [1, 3, -2],
                   [2, -3, -1], [2, -1, 3], [2, 1, -3], [2, 3, 1],
                   [3, -2, 1], [3, -1, -2], [3, 1, 2], [3, 2, -1]]

  def delta([x1,y1,z1],[x2,y2,z2]), do: abs(x2-x1)+abs(y2-y1)+abs(z2-z1)
  def shift([x1,y1,z1],[x2,y2,z2]), do: [x2-x1,y2-y1,z2-z1]
  def shiftv(l, d), do: Enum.map(l, &shift(d, &1))

  def alignxyz( l, r ) do
    shifts = for a <- l, b <- r, do: shift(a,b)
    {best, freq} = Enum.frequencies(shifts) |> Enum.max_by(&(elem(&1,1)))
    if freq >= 12, do: best, else: nil
  end

  def pick(l, rot), do: Enum.at(l, abs(rot)-1)*div(rot, abs(rot))
  def rotate([], _), do: []
  def rotate([ h | t ], r=[r0,r1,r2]), do: [[pick(h,r0), pick(h,r1), pick(h,r2)] | rotate(t,r)]

  def alignrot(l, r), do: for rot <- rots(), into: %{}, do: {rot, alignxyz(l, rotate(r, rot))}

  def alignnext(_, [], good, bad, pos), do: { good, bad, pos }
  def alignnext(next, [ h | t ], good, bad, pos ) do
    rd = alignrot(next, h) |> Enum.find(&(not is_nil(elem(&1,1))))
    case rd do
      { rot, diff } -> alignnext(next, t, [ shiftv(rotate(h,rot),diff) | good], bad, [ diff | pos ])
      nil -> alignnext(next, t, good, [ h | bad ], pos)
    end
  end

  def alignall(done, aligned, []), do: Enum.concat(done,aligned)
  def alignall(done, [ next | t ], rest) do
    {new, rest, _} = alignnext(next, rest, [], [], [])
    alignall([ next | done ], Enum.concat(new, t), rest)
  end

  def part1(args) do
    scans = prep(args)
    beacons = Enum.concat(alignall([], [ hd(scans) ], tl(scans)))
    beacons |> Enum.frequencies() |> Map.keys() |> Enum.count()
  end

  def alignall2(pos, _, []), do: pos
  def alignall2(pos, [ next | t ], rest) do
    {new, rest, npos} = alignnext(next, rest, [], [], [])
    alignall2(Enum.concat(pos, npos), Enum.concat(new, t), rest)
  end

  def part2(args) do
    scans = prep(args)
    pos = alignall2([[0,0,0]], [ hd(scans) ], tl(scans))
    distances = for a <- pos, b <- pos, into: [], do: delta(a,b)
    Enum.max(distances)
  end
end
