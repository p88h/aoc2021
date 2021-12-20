defmodule Aoc2021.Day15 do
  def load(args, r) do
    lol = Enum.map(args, fn l -> String.graphemes(l) |> Enum.map(&String.to_integer/1) end)
    map = Stream.with_index(lol)
      |> Enum.map(fn {x,i} -> Stream.with_index(x) |> Enum.map(&({{i,elem(&1,1)},elem(&1,0)})) end)
      |> List.flatten() |> Map.new()
    {map, length(lol)*r-1, length(hd(lol))*r-1, length(lol), length(hd(lol)) }
  end

  def update(pq, {map, ly, lx, my, mx}, cost, dist, p={y,x}) when y>=0 and y<=ly and x>=0 and x<=lx do
    oldd = if is_map_key(cost, p), do: cost[p], else: 999999999
    newd = dist + rem(map[{rem(y,my),rem(x,mx)}]+div(y,my)+div(x,mx)-1,9)+1
    if newd < oldd, do: PriorityQueue.put(pq, {newd, p}), else: pq
  end
  def update(pq, _map, _cost, _dist, _pos), do: pq

  def explore({_map, ly, lx, _, _}, _cost, _pq, { dist, {ly,lx} }), do: dist
  def explore(mp, cost, pq, { dist, {y,x} }) do
    pq = PriorityQueue.delete_min!(pq)
    if not is_map_key(cost, {y,x}) or cost[{y,x}] > dist do
      cost = Map.put(cost, {y,x}, dist)
      ms = Enum.map([ {-1,0},{1,0},{0,-1},{0,1} ], fn {a,b} -> {y+a,x+b} end)
      pq = Enum.reduce(ms, pq, &update(&2, mp, cost, dist, &1))
      explore(mp, cost, pq, PriorityQueue.min!(pq))
    else
      explore(mp, cost, pq, PriorityQueue.min!(pq))
    end
  end

  def startq(), do: PriorityQueue.new() |> PriorityQueue.put({0,{0,0}})
  def part1(args), do: load(args, 1) |> explore(%{}, startq(), {0,{0,0}})
  def part2(args), do: load(args, 5) |> explore(%{}, startq(), {0,{0,0}})
end
