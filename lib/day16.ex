defmodule Aoc2021.Day16 do
  def h2b(<<>>), do: <<>>
  def h2b(<<a, b, r::binary>>) do
    :binary.encode_unsigned(elem(Integer.parse(<<a, b>>, 16), 0)) <> h2b(r)
  end

  def literal(<<0::1, x::size(4), r::bitstring>>, acc, v), do: {r, acc * 16 + x, v}
  def literal(<<1::1, x::size(4), r::bitstring>>, acc, v), do: literal(r, acc * 16 + x, v)

  def pkts(<<>>, l, s, c), do: {c, l, s}

  def pkts(<<b::bitstring>>, l, s, c),
    do: packet(b) |> (fn {r, a, v} -> pkts(r, [a | l], s + v, c) end).()

  def pktl(b, l, 0, s), do: {b, l, s}
  def pktl(b, l, n, s), do: packet(b) |> (fn {r, a, v} -> pktl(r, [a | l], n - 1, s + v) end).()

  def eval({r, l, v}, 0), do: {r, Enum.sum(l), v}
  def eval({r, l, v}, 1), do: {r, Enum.product(l), v}
  def eval({r, l, v}, 2), do: {r, Enum.min(l), v}
  def eval({r, l, v}, 3), do: {r, Enum.max(l), v}
  def eval({r, [b, a], v}, 5), do: {r, if(a > b, do: 1, else: 0), v}
  def eval({r, [b, a], v}, 6), do: {r, if(a < b, do: 1, else: 0), v}
  def eval({r, [b, a], v}, 7), do: {r, if(a == b, do: 1, else: 0), v}

  def packet(<<v::size(3), t::size(3), r::bitstring>>) when t == 4, do: literal(r, 0, v)
  def packet(<<v::size(3), t::size(3), 1::1, len::size(11), r::bitstring>>) do
    eval(pktl(r, [], len, v), t)
  end
  def packet(<<v::size(3), t::size(3), 0::1, len::size(15), sp::size(len), rr::bitstring>>) do
    eval(pkts(<<sp::size(len)>>, [], v, rr), t)
  end

  def part1(args), do: h2b(hd(args)) |> packet |> elem(2)
  def part2(args), do: h2b(hd(args)) |> packet |> elem(1)
end
