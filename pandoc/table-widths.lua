local function latex_escape(text)
  return text
    :gsub('\\', '\\textbackslash{}')
    :gsub('([%%{}_$&#])', '\\%1')
    :gsub('%^', '\\textasciicircum{}')
    :gsub('~', '\\textasciitilde{}')
end

local function cell_text(cell)
  local lines = {}
  for _, block in ipairs(cell.contents) do
    lines[#lines + 1] = pandoc.utils.stringify(block)
  end
  return latex_escape(table.concat(lines, ' '))
end

local function row_cells(row)
  local cells = {}
  for i = 1, #row.cells do
    cells[#cells + 1] = cell_text(row.cells[i])
  end
  return table.concat(cells, ' & ') .. ' \\\\'
end

function Table(tbl)
  if FORMAT ~= 'latex' then
    return tbl
  end

  local count = #tbl.colspecs
  if count == 0 then
    return tbl
  end

  local spec
  if count == 2 then
    spec = '@{}>{\\raggedleft\\arraybackslash}p{0.16\\linewidth}>{\\raggedleft\\arraybackslash}X@{}'
  else
    local cols = {}
    for _ = 1, count do
      cols[#cols + 1] = '>{\\raggedleft\\arraybackslash}X'
    end
    spec = '@{}' .. table.concat(cols) .. '@{}'
  end

  local out = {
    '\\noindent\\begingroup',
    '\\fontsize{15.5pt}{24pt}\\selectfont',
    '\\begin{tabularx}{\\linewidth}{' .. spec .. '}',
    '\\toprule'
  }

  for _, row in ipairs(tbl.head.rows) do
    out[#out + 1] = row_cells(row)
  end
  out[#out + 1] = '\\midrule'

  for _, body in ipairs(tbl.bodies) do
    for _, row in ipairs(body.body) do
      out[#out + 1] = row_cells(row)
    end
  end

  out[#out + 1] = '\\bottomrule'
  out[#out + 1] = '\\end{tabularx}'
  out[#out + 1] = '\\endgroup'
  return pandoc.RawBlock('latex', table.concat(out, '\n'))
end
