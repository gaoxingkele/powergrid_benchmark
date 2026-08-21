"""Send the hash-checked MA-SQLGrid PDF with an RFC-compliant UTF-8 body."""

from __future__ import annotations

import argparse
import hashlib
import os
import smtplib
from email import policy
from email.message import EmailMessage
from pathlib import Path


SMTP_HOST = "smtp.xmu.edu.cn"
SMTP_PORT = 465
SENDER = "iamafan@xmu.edu.cn"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--body", required=True, type=Path)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--to", required=True)
    args = parser.parse_args()

    attachment = args.pdf.resolve(strict=True)
    body_file = args.body.resolve(strict=True)
    actual_hash = sha256(attachment)
    if actual_hash != args.sha256.upper():
        raise RuntimeError(f"Attachment hash mismatch: {actual_hash}")

    password = os.environ.get("XMU_SMTP_PASSWORD")
    if not password:
        raise RuntimeError("XMU_SMTP_PASSWORD is not set")

    message = EmailMessage(policy=policy.SMTP)
    message["From"] = SENDER
    message["To"] = args.to
    message["Subject"] = args.subject
    message["Content-Language"] = "zh-CN"
    message.set_content(
        body_file.read_text(encoding="utf-8"),
        subtype="plain",
        charset="utf-8",
        cte="base64",
    )
    message.add_attachment(
        attachment.read_bytes(),
        maintype="application",
        subtype="pdf",
        filename=attachment.name,
    )

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=180) as server:
        server.ehlo()
        server.login(SENDER, password)
        refused = server.send_message(message)
    if refused:
        raise RuntimeError(f"Recipients refused: {sorted(refused)}")
    print(f"SENT {attachment.name} to {args.to}; sha256={actual_hash}")


if __name__ == "__main__":
    main()
