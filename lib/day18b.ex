defmodule Aoc2021.Day18B do
  def applyv([], _), do: []
  def applyv([ h | t ], fx) when h == "[" or h == "]" or h == ",", do: [ h | applyv(t, fx) ]
  def applyv([ h | t ], fx), do: fx.(h, t)

  def convf(h, t), do: [ String.to_integer(h) | applyv(t, &convf/2) ]
  def conv(s) when is_binary(s), do: conv(String.graphemes(s))
  def conv(l), do: applyv(l, &convf/2)

  def splitf(h, t) when h>=10, do: [ "[", trunc(h/2), ",", h-trunc(h/2), "]"  | t ]
  def splitf(h, t), do: [ h | applyv(t, &splitf/2) ]
  def split(l), do: applyv(l, &splitf/2)

  def incr(l, a), do: applyv(l, &([ &1+a | &2 ]))

  def explode([], _), do: {0, []}
  def explode([ "[", a, ",", b, "]" | t ], 4 ), do: {a, [0 | incr(t,b)]}
  def explode([ "[" | t ], d), do: ({a, t} = explode(t, d+1); {a, ["[" | t] })
  def explode([ "]" | t ], d), do: ({a, t} = explode(t, d-1); {a, ["]" | t] })
  def explode([ "," | t ], d), do: ({a, t} = explode(t, d); {a, ["," | t] })
  def explode([x | t], d), do: ({a, t} = explode(t, d); {0, [x+a | t] })

  def fixup(t) do
    #IO.inspect(Enum.join(t))
    {_, t1} = explode(t, 0)
    if t1 == t do
      t1 = split(t)
      if t1 == t, do: t, else: fixup(t1)
    else
      fixup(t1)
    end
  end

  def mag(["[" | t]), do: ({l, ["," | t]} = mag(t); {r, ["]" | t]} = mag(t); {3*l + 2*r, t})
  def mag([x | t]), do: { x, t }

  def add(b, a), do: fixup(Enum.concat([["["], a, [","], b, ["]"]]))
  def varsums(l), do: for a <- l, b <- l, a != b, do: elem(mag(add(a,b)),0)

  def part1(args), do: Enum.map(args, &conv/1) |> Enum.reduce(&add/2) |> mag() |> elem(0)

  def part2(args), do: Enum.map(args, &conv/1) |> varsums() |> Enum.max()
end
