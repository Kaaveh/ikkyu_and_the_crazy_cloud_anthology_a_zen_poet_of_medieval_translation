-- A verse line too long for the measure wraps, and flush with the next line
-- its continuation reads as a line of its own: poem 115's quatrain typeset as
-- six lines. Set every line of a hard-broken paragraph as a paragraph of its
-- own, with its continuation indented. Spec 007.
local function lines(inlines)
  local out, cur = {}, pandoc.Inlines{}
  for _, el in ipairs(inlines) do
    if el.t == "LineBreak" then
      out[#out + 1] = cur
      cur = pandoc.Inlines{}
    else
      cur:insert(el)
    end
  end
  out[#out + 1] = cur
  return out
end

local function hang(el)
  local ls = lines(el.content)
  if #ls < 2 then return nil end
  -- A prose line is not verse: the epigraph is a 325-character quote over two
  -- attribution lines. The longest verse line in fa/ is 112.
  for _, l in ipairs(ls) do
    if utf8.len(pandoc.utils.stringify(l)) > 200 then return nil end
  end
  -- Per line rather than \everypar: a quote is a list, and lists own \everypar.
  -- \parskip goes to zero only after the first line, so the stanza keeps the
  -- space above it that the paragraph had.
  local blocks = { pandoc.RawBlock("latex", "\\begingroup") }
  for i, l in ipairs(ls) do
    l:insert(1, pandoc.RawInline("latex", "\\hangindent=2em\\hangafter=1 "))
    blocks[#blocks + 1] = pandoc.Plain(l)
    blocks[#blocks + 1] = pandoc.RawBlock("latex",
      i == 1 and "\\par\\setlength{\\parskip}{0pt}" or "\\par")
  end
  blocks[#blocks + 1] = pandoc.RawBlock("latex", "\\endgroup")
  return blocks
end

-- Not into lists: a hard break inside a list item is an entry, not verse, and
-- a \par there is a LaTeX error.
local function walk(blocks)
  local out = pandoc.Blocks{}
  for _, b in ipairs(blocks) do
    if b.t == "Para" then
      out:extend(hang(b) or { b })
    else
      if b.t == "Div" or b.t == "BlockQuote" then b.content = walk(b.content) end
      out:insert(b)
    end
  end
  return out
end

function Pandoc(doc)
  if FORMAT:match("latex") then doc.blocks = walk(doc.blocks) end
  return doc
end
