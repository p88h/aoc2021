defmodule Aoc2021.Day20 do
  def conv1d([], p, d), do: [rem(p * 2 + rem(d,2), 8), rem(p * 4 + rem(d,4), 8)]
  def conv1d([a | t], p, d), do: ( f = rem(p * 2 + a, 8); [f | conv1d(t, f, d)] )

  def add2lf([], []), do: []
  def add2lf([a1 | t1], [a2 | t2]), do: [rem(a1, 64) * 8 + a2 | add2lf(t1, t2)]

  def shiftl(p, d, m), do: Enum.map(p, &rem(&1 * m + rem(d,m), 512))
  def conv2d([], p, d), do: [ shiftl(p, d, 8), shiftl(p, d, 64) ]
  def conv2d([l | t], p, d), do: ( k = add2lf(p, conv1d(l, d, d)); [k | conv2d(t, k, d)] )

  def iter(mat, _, _, _, step, step), do: mat
  def iter(mat, bits, size, dflt, step, maxstep) do
    mconv = conv2d(mat, List.duplicate(512 - dflt, size + step * 2), 512 - dflt)
    mat = Enum.map(mconv, fn l -> Enum.map(l, &bits[&1]) end)
    dflt = if dflt == 0, do: bits[0], else: bits[511]
    iter(mat, bits, size, dflt, step + 1, maxstep)
  end

  def hash_bits(s), do: Enum.map(String.graphemes(s), &if(&1 == "#", do: 1, else: 0))
  def indexed_map(l), do: for({v, k} <- Stream.with_index(l), into: %{}, do: {k, v})

  def run([rules, "" | lines], maxstep) do
    bits = hash_bits(rules) |> indexed_map()
    mat = Enum.map(lines, &hash_bits/1)
    iter(mat, bits, length(lines), 0, 1, maxstep + 1)
  end

  def part1(args), do: run(args, 2) |> List.flatten() |> Enum.sum()
  def part2(args), do: run(args, 50) |> List.flatten() |> Enum.sum()
end
