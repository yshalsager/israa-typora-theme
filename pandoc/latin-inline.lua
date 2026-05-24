local function latex_escape(text)
  return text
    :gsub('\\', '\\textbackslash{}')
    :gsub('([%%{}_$&#])', '\\%1')
    :gsub('%^', '\\textasciicircum{}')
    :gsub('~', '\\textasciitilde{}')
end

function Str(el)
  if FORMAT:match('latex') and el.text:match('[A-Za-z]') then
    return pandoc.RawInline('latex', '\\textenglish{' .. latex_escape(el.text) .. '}')
  end
end
