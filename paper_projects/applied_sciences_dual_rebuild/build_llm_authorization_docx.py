from __future__ import annotations

import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "LLM_API_AUTHORIZATION_AND_ADJUDICATION_PLAN_2026-08-07.md"
OUTPUT = HERE / "LLM_API_AUTHORIZATION_AND_ADJUDICATION_PLAN_2026-08-07.docx"


def clean(text: str) -> str:
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    return text.replace("  ", " ").strip()


def run(text: str, *, bold: bool = False, italic: bool = False, code: bool = False) -> str:
    font = "Consolas" if code else "Calibri"
    east = "Microsoft YaHei"
    props = [f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:eastAsia="{east}"/>']
    if bold:
        props.append("<w:b/>")
    if italic:
        props.append("<w:i/>")
    if code:
        props.append('<w:sz w:val="18"/><w:szCs w:val="18"/>')
    preserve = ' xml:space="preserve"' if text[:1].isspace() or text[-1:].isspace() else ""
    return f"<w:r><w:rPr>{''.join(props)}</w:rPr><w:t{preserve}>{escape(text)}</w:t></w:r>"


def paragraph(text: str, style: str = "Normal", num_id: int | None = None, quote: bool = False,
              code: bool = False, page_break_before: bool = False) -> str:
    ppr = [f'<w:pStyle w:val="{style}"/>']
    if num_id is not None:
        ppr.append(f'<w:numPr><w:ilvl w:val="0"/><w:numId w:val="{num_id}"/></w:numPr>')
    if quote:
        ppr.append('<w:ind w:left="360"/><w:shd w:val="clear" w:color="auto" w:fill="F2F4F7"/>')
    if page_break_before:
        ppr.append("<w:pageBreakBefore/>")
    if code:
        ppr.append('<w:shd w:val="clear" w:color="auto" w:fill="F7F7F7"/><w:ind w:left="240" w:right="240"/>')
    return f"<w:p><w:pPr>{''.join(ppr)}</w:pPr>{run(text, code=code)}</w:p>"


def table(rows: list[list[str]]) -> str:
    cols = max(len(r) for r in rows)
    width = 9360
    base = width // cols
    widths = [base] * cols
    widths[-1] += width - sum(widths)
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    trs = []
    for ri, row in enumerate(rows):
        cells = []
        row = row + [""] * (cols - len(row))
        for ci, value in enumerate(row):
            fill = '<w:shd w:val="clear" w:color="auto" w:fill="E8EEF5"/>' if ri == 0 else ""
            tcpr = f'<w:tcW w:w="{widths[ci]}" w:type="dxa"/>{fill}<w:vAlign w:val="center"/>'
            p = f'<w:p><w:pPr><w:spacing w:before="0" w:after="40" w:line="260" w:lineRule="auto"/></w:pPr>{run(clean(value), bold=(ri == 0))}</w:p>'
            cells.append(f'<w:tc><w:tcPr>{tcpr}</w:tcPr>{p}</w:tc>')
        trpr = '<w:tblHeader/>' if ri == 0 else ""
        trs.append(f'<w:tr><w:trPr>{trpr}</w:trPr>{"".join(cells)}</w:tr>')
    borders = ''.join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="D9DEE5"/>' for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
    tblpr = (
        '<w:tblW w:w="9360" w:type="dxa"/><w:tblInd w:w="120" w:type="dxa"/>'
        '<w:tblLayout w:type="fixed"/>'
        f'<w:tblBorders>{borders}</w:tblBorders>'
        '<w:tblCellMar><w:top w:w="100" w:type="dxa"/><w:left w:w="120" w:type="dxa"/>'
        '<w:bottom w:w="100" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tblCellMar>'
    )
    return f'<w:tbl><w:tblPr>{tblpr}</w:tblPr><w:tblGrid>{grid}</w:tblGrid>{"".join(trs)}</w:tbl>'


def parse_markdown(md: str) -> tuple[list[str], int]:
    lines = md.splitlines()
    parts: list[str] = []
    i = 0
    in_code = False
    code_lines: list[str] = []
    para_lines: list[str] = []
    next_decimal_num_id = 2
    active_decimal_num_id: int | None = None

    def flush_para() -> None:
        if para_lines:
            parts.append(paragraph(clean(" ".join(x.strip() for x in para_lines))))
            para_lines.clear()

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush_para()
            if in_code:
                for cl in code_lines:
                    parts.append(paragraph(cl or " ", style="Code", code=True))
                code_lines.clear()
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue
        if not line.strip():
            flush_para()
            active_decimal_num_id = None
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-+", lines[i + 1]):
            flush_para()
            raw_rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                raw_rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            rows = [raw_rows[0]] + raw_rows[2:]
            parts.append(table(rows))
            continue
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            flush_para()
            level = len(m.group(1))
            text = clean(m.group(2))
            if level == 1:
                parts.append(paragraph(text, "DocTitle"))
            else:
                parts.append(paragraph(text, f"Heading{level - 1}"))
            i += 1
            continue
        if line.startswith(">"):
            flush_para()
            parts.append(paragraph(clean(line[1:].strip()), quote=True))
            i += 1
            continue
        if re.match(r"^\s*[-*]\s+", line):
            flush_para()
            parts.append(paragraph(clean(re.sub(r"^\s*[-*]\s+", "", line)), "ListParagraph", num_id=1))
            i += 1
            continue
        if re.match(r"^\s*\d+\.\s+", line):
            flush_para()
            if active_decimal_num_id is None:
                active_decimal_num_id = next_decimal_num_id
                next_decimal_num_id += 1
            parts.append(paragraph(clean(re.sub(r"^\s*\d+\.\s+", "", line)), "ListParagraph", num_id=active_decimal_num_id))
            i += 1
            continue
        active_decimal_num_id = None
        if line.strip() == "---":
            flush_para()
            parts.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="4" w:space="6" w:color="B8C2CC"/></w:pBdr></w:pPr></w:p>')
            i += 1
            continue
        para_lines.append(line)
        i += 1
    flush_para()
    return parts, next_decimal_num_id - 1


def styles_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Microsoft YaHei"/><w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="en-US" w:eastAsia="zh-CN"/></w:rPr></w:rPrDefault></w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:pPr><w:spacing w:before="0" w:after="120" w:line="264" w:lineRule="auto"/><w:widowControl/></w:pPr><w:rPr><w:color w:val="222222"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="DocTitle"><w:name w:val="Document Title"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:spacing w:before="240" w:after="160"/><w:keepNext/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:color w:val="0B2545"/><w:sz w:val="48"/><w:szCs w:val="48"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:spacing w:before="320" w:after="160"/><w:keepNext/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:color w:val="2E74B5"/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:spacing w:before="240" w:after="120"/><w:keepNext/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:color w:val="2E74B5"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:spacing w:before="160" w:after="80"/><w:keepNext/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:b/><w:color w:val="1F4D78"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="80"/><w:contextualSpacing/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr></w:style>
</w:styles>'''


def numbering_xml(max_num_id: int) -> str:
    instances = '<w:num w:numId="1"><w:abstractNumId w:val="1"/></w:num>'
    instances += "".join(f'<w:num w:numId="{i}"><w:abstractNumId w:val="2"/></w:num>' for i in range(2, max_num_id + 1))
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:abstractNum w:abstractNumId="1"><w:multiLevelType w:val="singleLevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:tabs><w:tab w:val="num" w:pos="360"/></w:tabs><w:ind w:left="720" w:hanging="360"/></w:pPr><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/></w:rPr></w:lvl></w:abstractNum>
  <w:abstractNum w:abstractNumId="2"><w:multiLevelType w:val="singleLevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/><w:lvlJc w:val="left"/><w:pPr><w:tabs><w:tab w:val="num" w:pos="360"/></w:tabs><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl></w:abstractNum>
''' + instances + '</w:numbering>'


def build() -> None:
    parsed, max_num_id = parse_markdown(SOURCE.read_text(encoding="utf-8"))
    body = "".join(parsed)
    sect = ('<w:sectPr><w:headerReference w:type="default" r:id="rId4"/><w:footerReference w:type="default" r:id="rId5"/>'
            '<w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>'
            '<w:cols w:space="708"/><w:docGrid w:linePitch="312"/></w:sectPr>')
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><w:body>{body}{sect}</w:body></w:document>'''
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/><Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/><Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>'''
    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>'''
    doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/><Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/><Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/></Relationships>'''
    header = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="4" w:space="4" w:color="D9DEE5"/></w:pBdr></w:pPr><w:r><w:rPr><w:color w:val="6B7280"/><w:sz w:val="18"/></w:rPr><w:t>CMC 双论文 · LLM API、标注裁决与实验授权方案</w:t></w:r></w:p></w:hdr>'''
    footer = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:pPr><w:jc w:val="right"/></w:pPr><w:r><w:rPr><w:color w:val="6B7280"/><w:sz w:val="18"/></w:rPr><w:t>第 </w:t></w:r><w:fldSimple w:instr=" PAGE "><w:r><w:rPr><w:color w:val="6B7280"/><w:sz w:val="18"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple><w:r><w:rPr><w:color w:val="6B7280"/><w:sz w:val="18"/></w:rPr><w:t> 页</w:t></w:r></w:p></w:ftr>'''
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    core = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>CMC 两篇论文：LLM API 申请、标注裁决与实验授权执行方案</dc:title><dc:creator>CMC authors</dc:creator><cp:lastModifiedBy>CMC authors</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified></cp:coreProperties>'''
    app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><Company></Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>'''
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("word/document.xml", document)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        z.writestr("word/styles.xml", styles_xml())
        z.writestr("word/numbering.xml", numbering_xml(max_num_id))
        z.writestr("word/header1.xml", header)
        z.writestr("word/footer1.xml", footer)
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
    print(OUTPUT)


if __name__ == "__main__":
    build()
