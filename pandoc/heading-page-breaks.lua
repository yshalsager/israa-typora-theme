local function has_class(element, expected)
  for _, class in ipairs(element.classes) do
    if class == expected then
      return true
    end
  end
  return false
end

local first_heading = true

function Header(element)
  if not FORMAT:match('latex') or element.level ~= 1 then
    return nil
  end

  local break_before = not first_heading
    and not has_class(element, 'no-page-break')
    and not has_class(element, 'nopagebreak')
  first_heading = false

  if break_before then
    return {pandoc.RawBlock('latex', '\\clearpage'), element}
  end
end
