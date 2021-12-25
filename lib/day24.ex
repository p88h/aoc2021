defmodule Aoc2021.Day24 do
  def expr(val, inp \\ [], left \\ nil), do: { val, inp, left }
  def ezero(), do: {0, [], nil}

  def emin({val, inp, nil}), do: length(inp)+val
  def emin({val, inp, left}), do: emin(left)+length(inp)+val
  def emax({val, inp, nil}), do: 9*length(inp)+val
  def emax({val, inp, left}), do: emax(left)+9*length(inp)+val
  def equal({val, [], nil}, imm), do: val == imm
  def equal(reg, imm), do: emin(reg) == imm and emax(reg) == imm

  def ediv(reg, 1), do: reg
  def ediv(reg, { val, [], nil }), do: ediv(reg, val)
  def ediv({_, _, left}, _val) when not is_nil(left), do: left
  def ediv({_, _, _}, _val), do: ezero()

  def emul(_reg, 0), do: ezero()
  def emul(reg, 1), do: reg
  def emul(reg = {0, [], nil}, _), do: reg
  def emul(reg, { val, [], nil }), do: emul(reg, val)
  def emul(reg, _val), do: {0, [], reg}

  def emod({val, inp, _}, _val), do: {val, inp, nil}

  def eadd(reg, 0), do: reg
  def eadd({val1, inp1, left1}, { val2, inp2, nil }), do: {val1+val2, Enum.concat(inp1, inp2), left1}
  def eadd({val1, inp1, nil}, { val2, inp2, left2 }), do: {val1+val2, Enum.concat(inp1, inp2), left2}
  def eadd({val1, inp1, left1}, { val2, inp2, left2 }), do: {val1+val2, Enum.concat(inp1, inp2), eadd(left1, left2)}
  def eadd({val, inp, left}, imm), do: { val+imm, inp, left }

  def str1(val, []), do: Integer.to_string(val)
  def str1(val, [ h | t ]), do: Integer.to_string(h) <> "+" <> str1(val, t)
  def estr({val, inp, nil}), do: str1(val, inp)
  def estr({val, inp, left}), do: "(" <> estr(left) <> "*X)+" <> str1(val,inp)

  def inpf({idx, ent, reg, con}, dst) do
    {idx+1, ent, Map.put(reg, dst, expr(0, [idx])), con}
  end

  def funf({idx, ent, reg, con}, fun, dst, op) when is_integer(op) do
    {idx, ent, Map.put(reg, dst, fun.(reg[dst], op)), con}
  end
  def funf({idx, ent, reg, con}, fun, dst, op) do
    {idx, ent, Map.put(reg, dst, fun.(reg[dst], reg[op])), con}
  end

  def addf(state, dst, op), do: funf(state, &eadd/2, dst, op)
  def mulf(state, dst, op), do: funf(state, &emul/2, dst, op)
  def divf(state, dst, op), do: funf(state, &ediv/2, dst, op)
  def modf(state, dst, op), do: funf(state, &emod/2, dst, op)

  def eqlf({idx, ent, reg, con}, dst, op) when is_integer(op) do
    val = if equal(reg[dst], op), do: expr(1), else: expr(0)
    {idx, ent, Map.put(reg, dst, val), con}
  end
  def eqlf({idx, ent, reg, con}, dst, op) do
    bit = rem(ent, 2)
    ent = div(ent, 2)
    pre = emax(reg[op]) < emin(reg[dst]) or emax(reg[dst]) < emin(reg[op])
    con = if bit == 1 do
      clause = if not pre, do: {reg[op], "==", reg[dst]}
      [ clause | con ]
    else
      if pre, do: con, else: [ {reg[op], "!=", reg[dst]} | con ]
    end
    reg = Map.put(reg, dst, expr(bit))
    {idx, ent, reg, con }
  end

  def resolve(s) when s=="x" or s=="y" or s=="z" or s =="w", do: s
  def resolve(s), do: String.to_integer(s)

  def parse(args) do
    for l <- args do
      case String.split(l) do
        ["inp", dst] -> { l, fn x -> inpf(x, dst) end }
        ["add", dst, op] -> { l, fn x -> addf(x,dst,resolve(op)) end }
        ["mul", dst, op] -> { l, fn x -> mulf(x,dst,resolve(op)) end }
        ["div", dst, op] -> { l, fn x -> divf(x,dst,resolve(op)) end }
        ["mod", dst, op] -> { l, fn x -> modf(x,dst,resolve(op)) end }
        ["eql", dst, op] -> { l, fn x -> eqlf(x,dst,resolve(op)) end }
      end
    end
  end

  def run(prog, start), do: Enum.reduce(prog, start, fn { _l, fun }, x -> fun.(x) end)

  def minimize([]), do: 0
  def minimize([ { {0, [l], nil}, "==", {d, [r], nil }} | t ]) do
    lv = if d > 0, do: 1 + d, else: 1
    rv = if d < 0, do: 1 - d, else: 1
    lv * trunc(:math.pow(10,14-l)) + rv * trunc(:math.pow(10,14-r)) + minimize(t)
  end
  def minimize({_, _, _, con}), do: minimize(con)

  def maximize([]), do: 0
  def maximize([ { {0, [l], nil}, "==", {d, [r], nil }} | t ]) do
    lv = if d > 0, do: 9, else: 9 + d
    rv = if d < 0, do: 9, else: 9 - d
    lv * trunc(:math.pow(10,14-l)) + rv * trunc(:math.pow(10,14-r)) + maximize(t)
  end
  def maximize({_, _, _, con}), do: maximize(con)

  def start(), do: %{ "x"=> expr(0), "y"=>expr(0), "z"=>expr(0), "w"=>expr(0) }

  def part1(args) do
    parse(args) |> run({ 1, 15528, start(), []}) |> maximize()
  end

  def part2(args) do
    parse(args) |> run({ 1, 15528, start(), []}) |> minimize()
  end
end
