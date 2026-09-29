# -*- coding: utf-8 -*-
"""三家单位电力系统发展水平与科研能力调查 — Brave + Tavily"""
import json, time, sys, os
import requests

BRAVE_KEY = "BSAM1t_qxF5z3cjrPtTAYIx166Ei-lf"
TAVILY_KEY = "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"

QUERIES = [
    # 湖北
    ("hubei", "国网湖北电科院 科技项目 人工智能 大模型"),
    ("hubei", "国网湖北省电力有限公司电力科学研究院 重点实验室 科研成果"),
    ("hubei", "湖北电网 新能源装机 发展 2025"),
    ("hubei", "湖北电科院 数字孪生 智能运检 科技进步奖"),
    # 周口
    ("zhoukou", "国网周口供电公司 科技项目 创新"),
    ("zhoukou", "周口电网 分布式光伏 装机 农村电网"),
    ("zhoukou", "国网河南电力 周口 智能配电网 建设"),
    # 冀北
    ("jibei", "国网冀北电力 智能配电网中心 科研"),
    ("jibei", "冀北电力 张家口 可再生能源示范区 分布式光伏"),
    ("jibei", "国网冀北电力 科技项目 人工智能 数字化"),
    ("jibei", "冀北电科院 智能配电网 秦皇岛 承德"),
]

def brave_search(q, count=8):
    r = requests.get("https://api.search.brave.com/res/v1/web/search",
        headers={"X-Subscription-Token": BRAVE_KEY, "Accept": "application/json"},
        params={"q": q, "count": count, "country": "CN", "search_lang": "zh-hans"}, timeout=30)
    r.raise_for_status()
    out = []
    for item in r.json().get("web", {}).get("results", []):
        out.append({"title": item.get("title"), "url": item.get("url"), "desc": item.get("description")})
    return out

def tavily_search(q, max_results=8):
    r = requests.post("https://api.tavily.com/search",
        json={"api_key": TAVILY_KEY, "query": q, "max_results": max_results,
              "search_depth": "advanced", "include_answer": True},
        timeout=60)
    r.raise_for_status()
    d = r.json()
    return {"answer": d.get("answer"),
            "results": [{"title": x.get("title"), "url": x.get("url"), "content": (x.get("content") or "")[:600]} for x in d.get("results", [])]}

report = {}
for unit, q in QUERIES:
    entry = {"query": q}
    try:
        entry["tavily"] = tavily_search(q)
    except Exception as e:
        entry["tavily_error"] = str(e)
    try:
        entry["brave"] = brave_search(q)
    except Exception as e:
        entry["brave_error"] = str(e)
    report.setdefault(unit, []).append(entry)
    print(f"[done] {unit}: {q}", flush=True)
    time.sleep(1.2)

with open(r"D:\BaiduSyncdisk\2026-08\国网项目策划\调查原始结果.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=1)
print("ALL DONE")
