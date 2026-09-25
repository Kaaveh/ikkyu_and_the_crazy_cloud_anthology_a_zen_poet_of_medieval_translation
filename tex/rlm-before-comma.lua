-- A Persian comma or semicolon between two Latin runs -- "(Vimalakirti
-- Sūtra)، T 14" -- is a neutral between two left-to-right characters, so the
-- bidi algorithm makes it left-to-right and welds the two runs into one. Under
-- LuaLaTeX that also breaks the bracket pair: note 61 typeset as
-- "(T 14 ،Vimalakirti Sūtra)". An invisible RLM in front pins the comma
-- right-to-left, which is what it always is in this book. Spec 007.
local RLM = "\u{200F}"

function Str(el)
  local s = el.text:gsub("،", RLM .. "،"):gsub("؛", RLM .. "؛")
  if s ~= el.text then
    el.text = s
    return el
  end
end
