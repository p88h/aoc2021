defmodule Aoc2021.Day23 do
  def home(a), do: %{"A"=>0,"B"=>1,"C"=>2,"D"=>3}[a]
  def cost(a), do: %{"A"=>1,"B"=>10,"C"=>100,"D"=>1000}[a]
  def swap(s, a, b), do: String.slice(s,0,a) <> String.at(s,b) <> String.slice(s,a+1,b-a-1) <> String.at(s,a) <> String.slice(s, b+1, 23-b)

  def find_top(s, ofs, lvl, kf) do
    if kf.(String.at(s, ofs + lvl)) and lvl > 0, do: find_top(s,ofs,lvl-1,kf), else: lvl
  end

  def move_in_cost(s, pos, dst, mc, ct) when pos < dst + 1 do
    ct = if pos == 0, do: ct + mc, else: ct + 2*mc
    if String.at(s,pos+1) == ".", do: move_in_cost(s, pos + 1, dst, mc, ct), else: -1
  end
  def move_in_cost(s, pos, dst, mc, ct) when pos > dst + 2 do
    ct = if pos == 6, do: ct + mc, else: ct + 2*mc
    if String.at(s,pos-1) == ".", do: move_in_cost(s, pos - 1, dst, mc, ct), else: -1
  end
  def move_in_cost(_s, _pos, _dst, _mc, ct), do: ct

  def move_home(s, 7, dist, _size), do: {s, dist}
  def move_home(s, pos, dist, size) do
    chr = String.at(s, pos)
    if chr == "."  do
      move_home(s, pos + 1, dist, size)
    else
      ofs = 7+home(chr)*size
      lvl = find_top(s, ofs, size-1, &(&1==chr))
      ctm = move_in_cost(s, pos, home(chr), cost(chr), (2+lvl)*cost(chr))
      if String.at(s, ofs+lvl) != "." or ctm < 0 do
        move_home(s, pos + 1, dist, size)
      else
        move_home(swap(s, pos, ofs+lvl), 0, dist + ctm, size)
      end
    end
  end

  def move_right(s, pos, dst, mc, ct) do
    ct = if dst == 6, do: ct + mc, else: ct + 2*mc
    if dst > 6 or String.at(s, dst) != "." do
      []
    else
      [ { swap(s, dst, pos), ct } | move_right(s, pos, dst + 1, mc, ct) ]
    end
  end

  def move_left(s, pos, dst, mc, ct) do
    ct = if dst == 0, do: ct + mc, else: ct + 2*mc
    if dst < 0 or String.at(s, dst) != "." do
      []
    else
      [ { swap(s, dst, pos), ct } | move_left(s, pos, dst - 1, mc, ct) ]
    end
  end

  def move_out(s, size, dist) do
    ret = for row <- 0..3 do
      ofs = 7+row*size
      lvl = find_top(s, ofs, size-1, &(&1 != "."))
      lvl = if lvl < size-1 and String.at(s, ofs+lvl) == ".", do: lvl + 1, else: lvl
      chr = String.at(s, ofs+lvl)
      if chr != "." and (row != home(chr) or find_top(s, ofs, size-1, &(&1==chr)) >= lvl) do
        Enum.concat(move_left(s, ofs+lvl, row+1, cost(chr), dist + cost(chr)*lvl),
                    move_right(s, ofs+lvl, row+2, cost(chr), dist + cost(chr)*lvl))
      else
        []
      end
    end
    ret |> List.flatten() |> Enum.map(&move_home(elem(&1,0), 0, elem(&1,1), size))
  end

  def extract([], _pos), do: []
  def extract([a | t], pos), do: [ String.at(a, pos) | extract(t,pos) ]
  def parse([_l1, l2, l3, l4, l5, l6, _l7], size) do
    a = String.at(l2,1)
    z = [ String.at(l2,11) ]
    s = for c <- 1..5, into: [], do: String.at(l2,c*2)
    ls = Enum.concat([a, s], z)
    il = if size == 2, do: [l3, l6], else: [l3, l4, l5, l6]
    lr = for r <- 0..3, into: [], do: extract(il, 3+r*2)
    Enum.join(ls) <> Enum.join(List.flatten(lr))
  end

  def update({pq, mind}, {state, dist}) do
    if not is_map_key(mind, state) or mind[state] > dist do
      { Map.update(pq, dist, [state], &([state|&1])), Map.put(mind, state, dist) }
    else
      { pq, mind }
    end
  end

  def explore(_mind, _pq, 50000, _final, _size, _ ), do: -1
  def explore(_mind, _pq, dist, final, _size, [ final | _ ] ), do: dist
  def explore(mind, pq, dist, final, size, [] ), do: explore(mind, pq, dist + 1, final, size, Map.get(pq, dist+1, []))
  def explore(mind, pq, dist, final, size, [ state | t ] ) do
    if not is_map_key(mind, state) or mind[state] >= dist do
      moves = move_out(state, size, dist)
      {pq, mind} = Enum.reduce(moves, {pq, mind}, &update(&2, &1))
      explore(mind, pq, dist, final, size, t)
    else
      explore(mind, pq, dist, final, size, t)
    end
  end

  def part1(args), do: explore(%{}, %{}, 0, ".......AABBCCDD", 2, [ parse(args, 2) ])
  def part2(args), do: explore(%{}, %{}, 0, ".......AAAABBBBCCCCDDDD", 4, [ parse(args, 4) ])
end
