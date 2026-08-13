-- Keep the manuscript's explicit, evidence-qualified caption paragraph and
-- suppress Pandoc's second caption derived from image alt text.
--
-- The Markdown sources intentionally place a bold "Figure N." paragraph
-- immediately after every standalone image.  Pandoc otherwise promotes the
-- image to a Figure block and emits an additional \caption{...}.  Returning
-- only the Figure content preserves the image and removes that duplicate.

function Figure(el)
  return el.content
end
