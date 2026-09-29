import sys
import json
import ssl
import smtplib
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import make_msgid, formatdate

sys.path.insert(0, r'D:\aicoding\mylib\email_tools')
from xmu_send import load_cfg

base = Path(__file__).resolve().parent
receipt = base / 'EMAIL_RECEIPT_LINFAN_V3.json'
if receipt.exists():
    raise SystemExit('Receipt already exists; no duplicate send.')
folder = base.parent / 'linfan_team_v3'
stem = '厦门大学林凡团队科研合作业绩与能力介绍_v3'
files = [folder / (stem + ext) for ext in ('.docx', '.pdf')]
for f in files:
    if not f.is_file() or f.stat().st_size == 0:
        raise SystemExit('Attachment missing or empty')
cfg = load_cfg()
recipient = 'iamafan@126.com'
msg = EmailMessage()
msg['From'] = cfg['default_from']
msg['To'] = recipient
cc = cfg.get('default_cc', [])
cc = [cc] if isinstance(cc, str) else cc
cc = [a for a in cc if a and a != recipient]
if cc:
    msg['Cc'] = ', '.join(cc)
msg['Subject'] = '科研合作业绩与能力介绍 V3（完整项目、论文及分类数据资源）'
msg['Date'] = formatdate(localtime=True)
msg['Message-ID'] = make_msgid()
msg.set_content('您好！\n\n附件为最新版 V3 的 Word 和 PDF，共36页。\n\n本版已调整为自然的团队自我介绍，减少姓名重复，并完整列出14项主要项目、补充科研经历、27篇论文和17条专利；65条公共资源按8类整理，另列自主开发研究材料。已完成逐页版式检查。\n\n论文分组沿用履历中的历史分区口径，不代表当前年度分区。\n\n请查收。')
records = []
for f in files:
    data = f.read_bytes()
    subtype = 'pdf' if f.suffix == '.pdf' else 'vnd.openxmlformats-officedocument.wordprocessingml.document'
    msg.add_attachment(data, maintype='application', subtype=subtype, filename=f.name)
    records.append({'name': f.name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
with smtplib.SMTP_SSL(cfg['smtp']['host'], int(cfg['smtp']['port']), context=ssl.create_default_context(), timeout=45) as server:
    server.login(cfg['default_from'], cfg['smtp']['password'])
    refused = server.send_message(msg, to_addrs=list(dict.fromkeys([recipient] + cc)))
result = {'status': 'SMTP_ACCEPTED' if not refused else 'PARTIAL_REFUSAL', 'to': recipient, 'message_id': msg['Message-ID'], 'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'attachments': records, 'refused_recipients': list(refused)}
receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
