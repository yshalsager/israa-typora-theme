function Table(tbl)
  if FORMAT ~= 'latex' or #tbl.colspecs == 0 then
    return tbl
  end

  -- Keep the native table AST: Pandoc handles headers, notes and cell resources.
  local count = #tbl.colspecs
  local columns = tbl.colspecs
  for i, column in ipairs(columns) do
    if column[2] == 0 then
      columns[i] = {column[1], count == 2 and (i == 1 and 0.16 or 0.84) or 1 / count}
    end
  end
  tbl.colspecs = columns
  for _, row in ipairs(tbl.head.rows) do
    for _, cell in ipairs(row.cells) do
      local block = cell.contents[1]
      if block and (block.t == 'Plain' or block.t == 'Para') then
        block.content:insert(1, pandoc.RawInline('latex', '\\cellcolor{israaTableHead}\\bfseries '))
      end
    end
  end
  return tbl
end
