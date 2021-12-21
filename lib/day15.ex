defmodule Aoc2021.Day15 do
  def load(args, r) do
    lol = Enum.map(args, fn l -> String.graphemes(l) |> Enum.map(&String.to_integer/1) end)
    map = Stream.with_index(lol)
      |> Enum.map(fn {x,i} -> Stream.with_index(x) |> Enum.map(&({{i,elem(&1,1)},elem(&1,0)})) end)
      |> List.flatten() |> Map.new()
    {map, length(lol)*r-1, length(hd(lol))*r-1, length(lol), length(hd(lol)) }
  end

  def update({pq, cost}, {map, ly, lx, my, mx}, dist, p={y,x}) when y>=0 and y<=ly and x>=0 and x<=lx and not is_map_key(cost, p) do
    newd = dist + rem(map[{rem(y,my),rem(x,mx)}]+div(y,my)+div(x,mx)-1,9)+1
    { Map.update(pq, newd, [p], &([p|&1])), Map.put(cost, p, newd) }
  end
  def update({pq, cost}, _map, _dist, _pos), do: { pq, cost }

  def explore({_map, ly, lx, _, _}, _cost, _pq, dist, [ {ly,lx} | _ ] ), do: dist
  def explore(mp, cost, pq, dist, [] ), do: explore(mp, cost, pq, dist + 1, Map.get(pq, dist+1, []))
  def explore(mp, cost, pq, dist, [ {y,x} | t ] ) do
    if not is_map_key(cost, {y,x}) or cost[{y,x}] >= dist do
      ms = Enum.map([ {-1,0},{1,0},{0,-1},{0,1} ], fn {a,b} -> {y+a,x+b} end)
      {pq, cost} = Enum.reduce(ms, {pq, cost}, &update(&2, mp, dist, &1))
      explore(mp, cost, pq, dist, t)
    else
      explore(mp, cost, pq, dist, t)
    end
  end

  def part1(args), do: load(args, 1) |> explore(%{}, %{}, 0, [{0,0}])
  def part2(args), do: load(args, 5) |> explore(%{}, %{}, 0, [{0,0}])
end
