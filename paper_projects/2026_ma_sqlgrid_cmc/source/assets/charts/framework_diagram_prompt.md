# Framework Diagram Prompt

**Paper**: Untitled Paper

## Image Generation Prompt

Use this as the image-generation prompt for the methodology framework diagram:

**Prompt:**
Create a clean IEEE Access-style methodology framework diagram for a paper titled “MA-SQLGrid: A Robust Multi-Agent Framework for Text-to-SQL in Power Grid Databases.” The figure should present a left-to-right pipeline with clear labeled modules, thin connector arrows, restrained scientific styling, and a white background. Use a professional systems-diagram look, not a marketing infographic. Keep typography compact, consistent, and readable at journal figure size.

Show the following pipeline stages as distinct blocks:
1. **Question Input**: user natural-language question `x`.
2. **Schema & Value Store**: database schema `S`, value inventory `V`, and power-grid maintenance database `D`.
3. **Schema Selector `g`**: compactly selects relevant tables, columns, relations, and limited value hints using lexical overlap, relation proximity, and domain salience.
4. **Domain Value Normalizer `n`**: maps question phrasing to canonical database literals, standardizes abbreviations, status labels, asset names, and temporal expressions.
5. **Answer Shape Predictor `h`**: infers answer form such as scalar, row set, grouped aggregate, boolean, or top-k list.
6. **Compact Context Builder**: combines selected schema, normalized values, and predicted shape into one prompt-ready context `c`.
7. **Fixed SQL Generator**: a single non-frontier model generates multiple candidate SQL queries `y1...yk`.
8. **Reference-Free Validator**: evaluates each candidate by execution success, answer-shape consistency, value alignment, and a light complexity penalty.
9. **Final Selection**: choose the highest-scoring executable SQL.
10. **Database Execution**: execute selected SQL against `D` to obtain the final denotation.

Visually separate the framework into two aligned lanes:
- **Construction lane** above or on the left: selector, normalizer, and shape predictor feeding the compact context builder.
- **Generation/validation lane** below or on the right: fixed generator, candidate SQL set, validator, final selection, and database execution.

Include small mathematical annotations in the diagram, rendered as part of the figure:
- `c = g(x,S,V) ⊕ n(x,V) ⊕ h(x)`
- `{y1,...,yk} ~ pθ(y | x,c)`
- `s(yi; x,c,D) = λ1 Exec + λ2 Shape + λ3 Value - λ4 Cost`

Use modest icons or symbols only if they are subtle and technical:
- table/grid icon for schema
- tag/value marker for canonical values
- a small shape icon for answer-form prediction
- code brackets for SQL generation
- checkmark or scoring bar for validation
- database cylinder for execution

Style requirements:
- IEEE-style, academic, and restrained
- crisp vector lines, no decorative gradients, no 3D effects
- no shadows, no glossy surfaces, no colorful blobs
- use a limited palette: dark navy, slate gray, muted teal, and one accent color such as gold or green
- boxes should have thin outlines and simple fills
- arrows should be straight or gently orthogonal, never curved and decorative
- label every block clearly
- emphasize that the system is **multi-role / multi-agent** but lightweight and compact
- include a small side note or inset showing “validated denotation” and “reference-free selection” as the key decision principle
- optionally include a tiny legend clarifying that the framework is designed for a frozen power-grid maintenance database with deterministic schema/value grounding

Composition:
- horizontal layout, balanced spacing, no overcrowding
- all text fully legible, no cropped labels
- suitable for a methods figure in an IEEE Access paper
- visually communicate that the framework reduces context size before generation and then reranks candidates via validation before final answer selection

Negative constraints:
- do not depict a generic chatbot
- do not show humans, faces, or screenshots
- do not use a colorful corporate infographic style
- do not include irrelevant analytics charts
- do not make it look like a product landing page
- do not include large paragraphs of text inside the figure

If you want, I can also turn this into a tighter “one-line prompt” version for Midjourney, DALL-E, or SDXL syntax.

## Usage Instructions

1. Copy the prompt above into an AI image generator (DALL-E 3, Midjourney, Ideogram, etc.)
2. Generate the image at high resolution (2048x1024 or similar landscape)
3. Save as `framework_diagram.png` in the same `charts/` folder
4. Insert into the paper's Method section using:
   - LaTeX: `\includegraphics[width=\textwidth]{charts/framework_diagram.png}`
   - Markdown: `![Framework Overview](charts/framework_diagram.png)`
