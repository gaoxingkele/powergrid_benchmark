from pathlib import Path
import sys, json, hashlib, ssl, smtplib
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

sys.path.insert(0, 'D:/aicoding/mylib/email_tools')
from xmu_send import load_cfg, _as_list

root = Path(__file__).resolve().parent.parent
base = root / 'linfan_team_v2'
receipt = root / 'internal/EMAIL_RECEIPT_LINFAN_V2.json'
if receipt.exists():
    raise SystemExit('Existing receipt; refusing duplicate send.')
assert (root / 'internal/QA_LINFAN_V2.md').is_file()
files = []
payloads = []
for suffix, mime in [('docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'), ('pdf', 'application/pdf')]:
    f = base / f'厦门大学林凡团队科研合作业绩与能力介绍_v2.{suffix}'
    data = f.read_bytes()
    assert len(data) > 10000
    if suffix == 'pdf':
        assert data == (root / 'internal/render_v2' / f.name).read_bytes()
    files.append({'name': f.name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    payloads.append((f.name, data, mime))
cfg = load_cfg()
to = ['iamafan@126.com']
cc = [a for a in _as_list(cfg.get('default_cc')) if a not in to]
msg = EmailMessage()
msg['From'] = cfg['default_from']
msg['To'] = ', '.join(to)
if cc:
    msg['Cc'] = ', '.join(cc)
msg['Subject'] = '厦门大学林凡团队科研合作业绩与能力介绍（升级版）'
msg['Date'] = formatdate(localtime=True)
msg['Message-ID'] = make_msgid(domain='xmu.edu.cn')
msg.set_content('您好！\n\n附件是升级后的《厦门大学林凡团队科研合作业绩与能力介绍》，Word和PDF各一份，共25页。\n\n本版已改为团队自我介绍，突出林凡团队面向电力与能源行业的科研合作业绩和能力，补充林凡履历、授权专利和高水平论文成果、14项主要项目完整清单，以及张志宏和周达相关研究积累。14项项目总金额合计2626.04万元，分担经费合计1573.24万元。\n\n报告同时保留国家专项与十五五方向对应、9个研究方向、数据资源条件、主要发表期刊与合作投稿期刊、期刊分区及影响因子和合作方式。个人、协同及联合工程成果分别列示；期刊指标注明年份和收录类别。\n\n已完成逐页版面检查，请查收。')
for name, data, mime in payloads:
    main, sub = mime.split('/', 1)
    msg.add_attachment(data, maintype=main, subtype=sub, filename=name)
with smtplib.SMTP_SSL(cfg['smtp']['host'], int(cfg['smtp']['port']), context=ssl.create_default_context(), timeout=60) as server:
    server.login(cfg['default_from'], cfg['smtp']['password'])
    refused = server.send_message(msg, from_addr=cfg['default_from'], to_addrs=to + cc)
result = {'status': 'smtp_accepted' if not refused else 'partial_refusal', 'to': to, 'cc': cc, 'message_id': msg['Message-ID'], 'sent_at_utc': datetime.now(timezone.utc).isoformat(), 'attachments': files, 'refused': list(refused), 'delivery_note': 'SMTP acceptance does not independently confirm recipient inbox delivery.'}
receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
