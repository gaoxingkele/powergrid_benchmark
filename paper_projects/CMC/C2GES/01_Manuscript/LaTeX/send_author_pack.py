"""Send the C2GES Information author pack via XMU SMTP (multiple attachments)."""
from __future__ import annotations

import mimetypes
import smtplib
import ssl
import sys
from email.message import EmailMessage
from email.utils import formatdate
from pathlib import Path

sys.path.insert(0, r"D:\aicoding\mylib\email_tools")
from xmu_send import load_cfg  # noqa: E402

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent


def attach(message: EmailMessage, path: Path) -> None:
    mime, _ = mimetypes.guess_type(path.name)
    major, minor = (mime or "application/octet-stream").split("/", 1)
    message.add_attachment(
        path.read_bytes(),
        maintype=major,
        subtype=minor,
        filename=path.name,
    )


def main() -> None:
    cfg = load_cfg()
    to_list = ["confident_topshen@163.com", "iamafan@126.com"]
    cc_list = []
    default_cc = cfg.get("default_cc")
    for addr in ([default_cc] if isinstance(default_cc, str) else list(default_cc or [])):
        if addr and addr not in to_list and addr not in cc_list:
            cc_list.append(addr)
    recipients = list(dict.fromkeys(to_list + cc_list))

    files = [
        PROJECT / "C2GES_Information_20260920_submission.zip",
        HERE / "paper_information.pdf",
        HERE / "paper_information.docx",
        HERE / "INFORMATION_COVER_LETTER.md",
        PROJECT / "C2GES_Information_20260920_supplementary.zip",
        HERE / "FORMAT_CHECK.md",
    ]
    missing = [str(p) for p in files if not p.is_file()]
    if missing:
        raise FileNotFoundError(missing)

    message = EmailMessage()
    message["From"] = cfg["default_from"]
    message["To"] = ", ".join(to_list)
    if cc_list:
        message["Cc"] = ", ".join(cc_list)
    message["Subject"] = (
        "C2GES 投 Information：2026-09-20 作者包（PDF/Word/LaTeX）及核心结论"
    )
    message["Date"] = formatdate(localtime=True)
    message.set_content((HERE / "EMAIL_BODY.txt").read_text(encoding="utf-8"))
    for path in files:
        attach(message, path)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        cfg["smtp"]["host"], int(cfg["smtp"]["port"]), context=context, timeout=180
    ) as server:
        server.login(cfg["default_from"], cfg["smtp"]["password"])
        server.send_message(message, from_addr=cfg["default_from"], to_addrs=recipients)
    sizes = {p.name: p.stat().st_size for p in files}
    print(f"SENT_OK to={to_list} cc={cc_list} files={sizes}")


if __name__ == "__main__":
    main()
