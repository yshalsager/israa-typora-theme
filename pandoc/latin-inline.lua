local function latex_escape(text)
  return text
    :gsub('\\', '\\textbackslash{}')
    :gsub('([%%{}_$&#])', '\\%1')
    :gsub('%^', '\\textasciicircum{}')
    :gsub('~', '\\textasciitilde{}')
end

local function Link(el)
  if FORMAT:match('latex') and pandoc.utils.stringify(el.content) == el.target then
    local url = pandoc.write(pandoc.Pandoc({pandoc.Plain({el})}), 'latex')
    return pandoc.RawInline('latex', '\\textenglish{\\fontsize{12pt}{19.2pt}\\selectfont ' .. url .. '}')
  end
end

local function Str(el)
  if FORMAT:match('latex') and el.text:match('[A-Za-z]') then
    return pandoc.RawInline('latex', '\\textenglish{' .. latex_escape(el.text) .. '}')
  end
end

-- Preserve Pandoc's URL escaping and line breaks before replacing Latin strings.
return {{Link = Link}, {Str = Str}}
