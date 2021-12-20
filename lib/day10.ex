defmodule Aoc2021.Day10 do
  def stack([c | t], s, m, z1, z2) when is_map_key(m, c), do: stack(t, [m[c] | s], m, z1, z2)
  def stack([], s, _, _, z2), do: {0, Enum.reduce(s, 0, fn x, a -> a * 5 + z2[x] end)}
  def stack([c | t], [c | r], m, z1, z2), do: stack(t, r, m, z1, z2)
  def stack([c | _], _, _, z1, _), do: {z1[c], 0}

  def process(args, ofs) do
    m = %{"(" => ")", "[" => "]", "{" => "}", "<" => ">"}
    z1 = %{")" => 3, "]" => 57, "}" => 1197, ">" => 25137}
    z2 = %{")" => 1, "]" => 2, "}" => 3, ">" => 4}
    Enum.map(args, &String.graphemes/1)
    |> Enum.map(&elem(stack(&1, [], m, z1, z2), ofs))
    |> Enum.reject(&(&1 == 0))
  end

  def part1(args), do: process(args, 0) |> Enum.sum()
  def middle(lst), do: Enum.sort(lst) |> Enum.at(div(length(lst), 2))
  def part2(args), do: process(args, 1) |> middle()
end
