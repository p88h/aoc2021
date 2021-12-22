defmodule Aoc2021.Day22 do
  def parse(line) do
    [_, b | r] = Regex.run(~r/(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)/, line)
    [ x0, x1, y0, y1, z0, z1 ] = Enum.map(r, &String.to_integer/1)
    {b == "on", [x0, x1 + 1, y0, y1 + 1, z0, z1 + 1]}
  end

  def crop([a0, a1 | at], [b0, b1 | bt]) when a1 <= b0 or a0 >= b1, do: [0, 0 | crop(at, bt)]
  def crop([a0, a1 | at], [b0, b1 | bt]), do: [max(a0, b0), min(a1, b1) | crop(at, bt)]
  def crop(_, _), do: []

  def empty([x0, x1, y0, y1, z0, z1]), do: x1 <= x0 or y1 <= y0 or z1 <= z0

  def volume([x0, x1, y0, y1, z0, z1]), do: (x1 - x0) * (y1 - y0) * (z1 - z0)
  def volume({dims, lst}), do: volume(dims) - Enum.sum(Enum.map(lst, &volume/1))

  def subtract(box = {dims, lst}, other) do
    cropped = crop(other, dims)
    if empty(cropped), do: box, else: {dims, [{cropped, []} | Enum.map(lst, &subtract(&1, cropped))]}
  end

  def handle(args, bounds \\ nil) do
    Enum.reduce(Enum.map(args, &parse/1), [], fn {bit, dims}, boxes ->
      dims = if is_nil(bounds), do: dims, else: crop(dims, bounds)
      boxes = Enum.map(boxes, &subtract(&1, dims))
      if bit, do: [{dims, []} | boxes], else: boxes
    end) |> Enum.map(&volume/1) |> Enum.sum()
  end

  def part1(args), do: handle(args, [-50, 51, -50, 51, -50, 51])
  def part2(args), do: handle(args)
end
