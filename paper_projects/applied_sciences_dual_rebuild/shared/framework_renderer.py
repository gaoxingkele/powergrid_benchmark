#!/usr/bin/env python3
"""Deterministic renderer for protocol-only, editable journal diagrams."""

from __future__ import annotations

import hashlib
import json
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle


FIXED_DATE = datetime(2026, 8, 5, tzinfo=timezone.utc)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def endpoint(source: dict[str, Any], target: dict[str, Any], outgoing: bool) -> tuple[float, float]:
    sx, sy = source["x"], source["y"]
    tx, ty = target["x"], target["y"]
    dx, dy = tx - sx, ty - sy
    if not outgoing:
        dx, dy = -dx, -dy
    if dx == 0 and dy == 0:
        return sx, sy
    if source.get("shape") == "diamond":
        scale = 1 / (abs(dx) / (source["w"] / 2) + abs(dy) / (source["h"] / 2))
    else:
        candidates = []
        if dx:
            candidates.append((source["w"] / 2) / abs(dx))
        if dy:
            candidates.append((source["h"] / 2) / abs(dy))
        scale = min(candidates)
    sign = 1 if outgoing else -1
    return sx + sign * dx * scale, sy + sign * dy * scale


def draw_node(ax, node: dict[str, Any], font_size: float) -> None:
    x, y, w, h = node["x"], node["y"], node["w"], node["h"]
    common = dict(facecolor=node["fill"], edgecolor="#1A1A1A", linewidth=1.35,
                  linestyle=node.get("linestyle", "solid"), hatch=node.get("hatch", ""), zorder=3)
    if node.get("shape") == "diamond":
        patch = Polygon([(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)], **common)
    elif node.get("shape") == "square":
        patch = Rectangle((x - w / 2, y - h / 2), w, h, **common)
    else:
        rounding = 0.08 if node.get("shape", "round") == "round" else 0.015
        pad = node.get("box_pad", 0.018)
        patch = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                               boxstyle=f"round,pad={pad},rounding_size={rounding}", **common)
    ax.add_patch(patch)
    ax.text(x, y, node["label"], ha="center", va="center", fontsize=node.get("font_size", font_size),
            color="#111111", weight=node.get("weight", "normal"), linespacing=1.22, zorder=4)


def draw_edge(ax, edge: dict[str, Any], nodes: dict[str, dict[str, Any]], font_size: float) -> None:
    source, target = nodes[edge["source"]], nodes[edge["target"]]
    start = endpoint(source, target, True)
    end = endpoint(target, source, False)
    style = edge.get("style", "solid")
    arrow = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=12, linewidth=1.25,
                            linestyle=style, color=edge.get("color", "#333333"),
                            connectionstyle=f"arc3,rad={edge.get('rad', 0)}", zorder=2)
    ax.add_patch(arrow)
    if edge.get("label"):
        mx, my = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
        mx += edge.get("label_dx", 0); my += edge.get("label_dy", 0)
        ax.text(mx, my, edge["label"], fontsize=font_size - 1, ha="center", va="center",
                color="#222222", bbox=dict(boxstyle="round,pad=0.12", facecolor="white",
                                             edgecolor="none", alpha=0.92), zorder=5)


def render_figure(figure: dict[str, Any], output_dir: Path, config_hash: str, script_path: Path) -> list[dict[str, Any]]:
    mpl.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": figure.get("font_size", 10.5),
        "svg.fonttype": "none", "svg.hashsalt": "applsci-framework-v1",
        "pdf.fonttype": 42, "ps.fonttype": 42, "axes.linewidth": 0.8,
    })
    width, height = figure.get("figsize", [12, 7.2])
    fig, ax = plt.subplots(figsize=(width, height))
    fig.patch.set_facecolor("white"); ax.set_facecolor("white")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    for group in figure.get("groups", []):
        patch = FancyBboxPatch((group["x"], group["y"]), group["w"], group["h"],
                               boxstyle="round,pad=0.012,rounding_size=0.02",
                               facecolor=group.get("fill", "#F7F7F7"), edgecolor="#666666",
                               linestyle=group.get("linestyle", "dashed"), linewidth=1.0, zorder=0)
        ax.add_patch(patch)
        ax.text(group["x"] + 0.012, group["y"] + group["h"] - 0.02, group["label"],
                ha="left", va="top", fontsize=figure.get("font_size", 10.5), weight="bold", color="#333333")
    nodes = {node["id"]: node for node in figure["nodes"]}
    for edge in figure["edges"]:
        draw_edge(ax, edge, nodes, figure.get("font_size", 10.5))
    for node in figure["nodes"]:
        draw_node(ax, node, figure.get("font_size", 10.5))
    for note in figure.get("notes", []):
        ax.text(note["x"], note["y"], note["text"], ha=note.get("ha", "left"), va="center",
                fontsize=figure.get("font_size", 10.5) - 1, style=note.get("style", "normal"),
                color="#333333", linespacing=1.2)
    plt.subplots_adjust(left=0.015, right=0.985, bottom=0.025, top=0.975)
    stem = figure["id"]
    outputs = []
    for extension in ("svg", "pdf", "png"):
        path = output_dir / f"{stem}.{extension}"
        metadata = ({"Date": "2026-08-05", "Creator": "framework_renderer.py"} if extension == "svg" else
                    {"CreationDate": FIXED_DATE, "ModDate": FIXED_DATE, "Creator": "framework_renderer.py"}
                    if extension == "pdf" else {"Software": "framework_renderer.py", "dpi": "450"})
        fig.savefig(path, format=extension, dpi=450, bbox_inches="tight", pad_inches=0.06, metadata=metadata)
        outputs.append({"path": path.name, "format": extension, "bytes": path.stat().st_size,
                        "sha256": sha256(path), "dpi": 450 if extension == "png" else None,
                        "editable_vector": extension in {"svg", "pdf"}})
    plt.close(fig)
    return outputs


def render_config(config_path: Path, output_dir: Path, script_path: Path) -> dict[str, Any]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("data_status") != "protocol_only_no_unfrozen_results":
        raise ValueError("Framework config must explicitly declare protocol-only/no-unfrozen-results status")
    output_dir.mkdir(parents=True, exist_ok=True)
    config_hash = sha256(config_path)
    outputs = []
    for figure in config["figures"]:
        outputs.extend(render_figure(figure, output_dir, config_hash, script_path))
    caption_lines = ["# Caption drafts", "",
                     "> Protocol/method diagrams only. No unfrozen experimental result is represented.", ""]
    for figure in config["figures"]:
        caption_lines.extend([f"## {figure['id']}", "", figure["caption"], "",
                              "Source evidence: " + "; ".join(figure["source_evidence"]), ""])
    captions = output_dir / "captions.md"
    captions.write_text("\n".join(caption_lines), encoding="utf-8")
    manifest = {
        "schema_version": "framework-artifact-manifest-1.0", "data_status": config["data_status"],
        "config": {"path": config_path.name, "sha256": config_hash},
        "renderer": {"path": script_path.name, "shared_source": str(Path(__file__).resolve()),
                     "sha256": sha256(script_path), "shared_sha256": sha256(Path(__file__).resolve())},
        "captions": {"path": captions.name, "sha256": sha256(captions)}, "outputs": outputs,
        "quality": {"png_dpi": 450, "svg_text_editable": True, "pdf_vector": True,
                    "palette": "Okabe-Ito", "redundant_encoding": "shape+hatch+line style"}
    }
    manifest_path = output_dir / "artifact_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest
