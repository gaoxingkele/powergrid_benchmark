from pathlib import Path
import sys, json, hashlib, ssl, smtplib
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

sys.path.insert(0, 'D:/aicoding/mylib/email_tools')
from xmu_send import load_cfg, _as_list

base=Path(__file__).resolve().parent.parent
receipt=base/'internal/EMAIL_RECEIPT.json'
if receipt.exists():
    raise SystemExit('Existing send receipt; refusing duplicate send.')
qa=json.loads((base/'internal/QA_RECORD.json').read_text(encoding='utf-8'))
assert qa['visual_review']=='passed'
cfg=load_cfg()
to=['iamafan@126.com']
cc=[a for a in _as_list(cfg.get('default_cc')) if a not in to]
msg=EmailMessage()
msg['From']=cfg['default_from']
msg['To']=', '.join(to)
if cc: msg['Cc']=', '.join(cc)
msg['Subject']='电力人工智能与新型电力系统科研能力说明（Word及PDF）'
msg['Date']=formatdate(localtime=True)
msg['Message-ID']=make_msgid(domain='xmu.edu.cn')
msg.set_content('您好！\n\n附件为电力人工智能与新型电力系统科研能力说明，2026年9月20日版，Word与PDF内容一致，共21页。\n\n内容包括：团队项目与联合成果、2025/2026年度国家专项及十五五政策对应、9个研究方向、65条本地研究资源目录、13本候选期刊的收录/JCR分区/影响因子和来源，以及合作方式与交付内容。\n\n期刊指标注明年度；JCR不与中科院分区混用，Information单独标为ESCI。数据、代码/入口及合成材料分开说明，联合成果不归为课题组独享。所附材料不包含数据原件或受访问限制的指南全文。\n\n请查收。')
files=[]
for suffix,mime in [('docx','application/vnd.openxmlformats-officedocument.wordprocessingml.document'),('pdf','application/pdf')]:
    f=base/f'电力人工智能科研能力说明_20260920.{suffix}'
    data=f.read_bytes()
    digest=hashlib.sha256(data).hexdigest()
    assert digest==qa['attachments'][suffix]['sha256']
    typ,sub=mime.split('/',1)
    msg.add_attachment(data,maintype=typ,subtype=sub,filename=f.name)
    files.append({'name':f.name,'bytes':len(data),'sha256':digest})
with smtplib.SMTP_SSL(cfg['smtp']['host'],int(cfg['smtp']['port']),context=ssl.create_default_context(),timeout=90) as server:
    server.login(cfg['default_from'],cfg['smtp']['password'])
    refused=server.send_message(msg,from_addr=cfg['default_from'],to_addrs=to+cc)
result={'status':'smtp_accepted' if not refused else 'partial_refusal','to':to,'cc':cc,'message_id':msg['Message-ID'],'sent_at_utc':datetime.now(timezone.utc).isoformat(),'attachments':files,'refused':list(refused),'delivery_note':'SMTP acceptance does not independently confirm recipient inbox delivery.'}
receipt.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
