defmodule Aoc2021.Day23 do
  def home(a), do: %{"A"=>0,"B"=>1,"C"=>2,"D"=>3}[a]
  def cost(a), do: %{"A"=>1,"B"=>10,"C"=>100,"D"=>1000}[a]
  def swap(s, a, b), do: String.slice(s,0,a) <> String.at(s,b) <> String.slice(s,a+1,b-a-1) <> String.at(s,a) <> String.slice(s, b+1, 23-b)

  def find_top(s, ofs, lvl, kind) do
    if String.at(s, ofs + lvl) == kind and lvl > 0, do: find_top(s,ofs,lvl-1,kind), else: lvl
  end

  def move_in_cost(s, pos, dst, mc, ct) when pos < dst + 1 do
    ct = if pos == 0, do: ct + mc, else: ct + 2*mc
    if String.at(s,pos+1) == ".", do: move_in_cost(s, pos + 1, dst, mc, ct), else: -1
  end
  def move_in_cost(s, pos, dst, mc, ct) when pos > dst + 2 do
    ct = if pos == 6, do: ct + mc, else: ct + 2*mc
    if String.at(s,pos-1) == ".", do: move_in_cost(s, pos - 1, dst, mc, ct + mc), else: -1
  end
  def move_in_cost(_s, _pos, _dst, _mc, ct), do: ct

  def move_home(s, 7, cost), do: {s, cost}
  def move_home(s, pos, cost) do
    chr = String.at(s, pos)
    if chr == "."  do
      move_home(s, pos + 1, cost)
    else
      ofs = 7+home(chr)*4
      lvl = find_top(s, ofs, 3, chr)
      ctm = move_in_cost(s, pos, home(chr), cost(chr), (2+lvl)*cost(chr))
      if String.at(s, ofs+lvl) != "." or ctm < 0 do
        move_home(s, pos + 1, cost)
      else
        move_home(swap(s, pos, ofs+lvl), 0, cost + ctm)
      end
    end
  end

  def look_down(s, ofs, lvl) do
    if String.at(s, ofs + lvl) == "." and lvl < 3, do: look_down(s,ofs,lvl+1), else: lvl
  end
  def move_right(s, pos, dst, mc, ct) do
    ct = if dst == 6, do: ct + mc, else: ct + 2*mc
    if dst > 6 or String.at(s, dst) == ".", do: [], else: [ { swap(s, dst, pos), ct } | move_right(s, pos, dst + 1, mc, ct) ]
  end
  def move_left(s, pos, dst, mc, ct) do
    ct = if dst == 0, do: ct + mc, else: ct + 2*mc
    if dst < 0 or String.at(s, dst) == ".", do: [], else: [ { swap(s, dst, pos), ct } | move_left(s, pos, dst - 1, mc, ct) ]
  end
  def move_out(s) do
    for row <- 0..3 do
      ofs = 7+row*4
      lvl = look_down(s, ofs, 0)
      chr = String.at(s, ofs+lvl)
      if chr != "." and (row != home(chr) or find_top(s, ofs, 3, chr) > lvl) do
        Enum.concat(move_left(s, ofs+lvl, row+1, cost(chr), cost(chr)*lvl), move_right(s, ofs+lvl, row+2, cost(chr), cost(chr)*lvl))
      else
        []
      end
    end |> List.flatten()
  end


  def part1(args) do
    nil
  end

  def part2(args) do
    nil
  end
end
