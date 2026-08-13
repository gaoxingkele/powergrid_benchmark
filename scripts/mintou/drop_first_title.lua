local first_h1_removed = false

function Header(element)
  if not first_h1_removed and element.level == 1 then
    first_h1_removed = true
    return {}
  end
end
