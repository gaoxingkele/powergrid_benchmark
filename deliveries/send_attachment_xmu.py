#!/usr/bin/env python3
"""Send one attachment through the configured XMU SMTP account."""

from __future__ import annotations

import argparse
import mimetypes
import smtplib
import ssl
import sys
from email.message import EmailMessage
from email.utils import formatdate
from pathlib import Path


EMAIL_TOOLS = Path(r"D:\aicoding\mylib\email_tools")
sys.path.insert(0, str(EMAIL_TOOLS))
from xmu_send import load_cfg  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", action="append", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body-file", type=Path, required=True)
    parser.add_argument("--attachment", type=Path, required=True)
    args = parser.parse_args()
    if not args.attachment.is_file() or not args.body_file.is_file():
        raise FileNotFoundError("body or attachment is missing")
    cfg = load_cfg()
    recipients = list(dict.fromkeys(args.to))
    default_cc = cfg.get("default_cc")
    cc_values = [default_cc] if isinstance(default_cc, str) else list(default_cc or [])
    for address in cc_values:
        if address and address not in recipients:
            recipients.append(address)
    message = EmailMessage()
    message["From"] = cfg["default_from"]
    message["To"] = ", ".join(args.to)
    cc = [address for address in recipients if address not in args.to]
    if cc:
        message["Cc"] = ", ".join(cc)
    message["Subject"] = args.subject
    message["Date"] = formatdate(localtime=True)
    message.set_content(args.body_file.read_text(encoding="utf-8"))
    mime, _ = mimetypes.guess_type(args.attachment.name)
    major, minor = (mime or "application/octet-stream").split("/", 1)
    message.add_attachment(args.attachment.read_bytes(), maintype=major, subtype=minor, filename=args.attachment.name)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(cfg["smtp"]["host"], int(cfg["smtp"]["port"]), context=context, timeout=90) as server:
        server.login(cfg["default_from"], cfg["smtp"]["password"])
        server.send_message(message, from_addr=cfg["default_from"], to_addrs=recipients)
    print(f"SENT_OK recipients={recipients} attachment={args.attachment.name} bytes={args.attachment.stat().st_size}")


if __name__ == "__main__":
    main()
