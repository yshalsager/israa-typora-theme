local function has_class(element, expected)
  for _, class in ipairs(element.classes) do
    if class == expected then
      return true
    end
  end
  return false
end

function Header(element)
  if not FORMAT:match('latex') then
    return nil
  end

  if element.level <= 2 and (has_class(element, 'no-page-break') or has_class(element, 'nopagebreak')) then
    return {
      pandoc.RawBlock('latex', '\\israanextheadingnobreak{}'),
      element,
    }
  end

  return nil
end
