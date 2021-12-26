defmodule Aoc2021.Day25 do
  def load(args) do
    lol = Enum.map(args, fn l -> String.graphemes(l) end)
    map = Stream.with_index(lol)
      |> Enum.map(fn {x,i} -> Stream.with_index(x) |> Enum.map(&({{i,elem(&1,1)},elem(&1,0)})) end)
      |> List.flatten() |> Map.new()
    {map, length(lol), length(hd(lol)) }
  end

  def move(map, h, w, dx, dy, ch) do
    for y <- 0..h-1, x <- 0..w-1, into: %{} do
      nch = if map[{y,x}] == "." do
        py = rem(y + h - dy, h)
        px = rem(x + w - dx, w)
        if map[{py,px}] == ch, do: ch, else: "."
      else
        if map[{y,x}] == ch do
          ny = rem(y + dy, h)
          nx = rem(x + dx, w)
          if map[{ny,nx}] == ".", do: ".", else: ch
        else
          map[{y,x}]
        end
      end
      {{y,x}, nch}
    end
  end

  def moveit({map, h, w}, cnt) do
    amap = move(map, h, w, 1, 0, ">")
    bmap = move(amap, h, w, 0, 1, "v")
    if bmap == map, do: cnt, else: moveit({bmap, h, w}, cnt + 1)
  end

  def part1(args), do: load(args) |> moveit(1)
  def part2(_args), do: "🌟"
end
