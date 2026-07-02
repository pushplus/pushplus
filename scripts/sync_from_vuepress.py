#!/usr/bin/env python3
"""Sync markdown docs from VuePress (perk-pushplus-doc) to pushplus GitHub articles."""

import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

VUEPRESS = Path("/Users/chensiyuan/project/pushplus/perk-pushplus-doc/docs")
PUSHPLUS = Path("/Users/chensiyuan/project/pushplus/pushplus")
IMAGES = PUSHPLUS / "images"
VUEPRESS_PUBLIC = VUEPRESS / ".vuepress" / "public" / "img"

# Files handled separately
SKIP_FILES = set()
README_PATH = "README.md"

IMAGE_URL_RE = re.compile(
    r"(?:src|href)=['\"]((?:(?:https?:)?//image\.pushplus\.plus/[^'\"]+)|/img/[^'\"]+)['\"]",
    re.I,
)
FANCYBOX_BLOCK_RE = re.compile(
    r"<a\s+data-fancybox[^>]*>\s*<img[^>]*>\s*</a>",
    re.I | re.S,
)
IMG_TAG_RE = re.compile(r"<img\b[^>]*?/?>", re.I | re.S)
FRONTMATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.S)


def image_prefix(rel_path: str) -> str:
    depth = rel_path.count("/")
    return "./images/" if depth == 0 else "../" * depth + "images/"


def cdn_path_from_url(url: str) -> str:
    url = url.strip()
    if url.startswith("/img/"):
        return url.lstrip("/")
    parsed = urlparse(url if "://" in url else "https:" + url)
    path = parsed.path.lstrip("/")
    for prefix in ("doc/img/", "image/", "images/", "pc/image/"):
        if path.startswith(prefix):
            return path[len(prefix) :] if prefix != "pc/image/" else f"pc/{path[len(prefix):]}"
    return path


def local_image_name(cdn_path: str) -> str:
    """Map CDN path to flat local filename under pushplus/images/."""
    parts = [p for p in cdn_path.split("/") if p]
    basename = parts[-1]
    if (IMAGES / basename).exists():
        return basename
    if len(parts) == 1:
        return basename
    prefixed = f"{parts[-2]}-{basename}"
    if (IMAGES / prefixed).exists():
        return prefixed
    return prefixed


def cdn_fetch_url(url: str) -> str:
    url = url.strip()
    if url.startswith("//"):
        return "https:" + url
    if url.startswith("/img/"):
        return "https://www.pushplus.plus" + url
    return url


def cdn_public_url(url: str) -> str:
    fetch = cdn_fetch_url(url)
    if fetch.startswith("https://image.pushplus.plus/"):
        return fetch
    parsed = urlparse(fetch)
    path = parsed.path.lstrip("/")
    return f"https://image.pushplus.plus/{path}"


def resolve_image(url: str, cache: dict[str, str]) -> str:
    if url in cache:
        return cache[url]
    cdn_path = cdn_path_from_url(url)
    name = local_image_name(cdn_path)
    cache[url] = name
    return name


def ensure_image(url: str, cache: dict[str, str], downloaded: list, copied: list, failed: list) -> tuple[str, bool]:
    """Return (reference_path, is_external)."""
    name = resolve_image(url, cache)
    dest = IMAGES / name
    if dest.exists():
        return name, False

    # Try vuepress public folder
    basename = Path(cdn_path_from_url(url)).name
    vue_src = VUEPRESS_PUBLIC / basename
    if vue_src.exists():
        shutil.copy2(vue_src, dest)
        copied.append((str(vue_src), name))
        return name, False

    fetch_url = cdn_fetch_url(url)
    try:
        result = subprocess.run(
            [
                "curl",
                "-fsSL",
                "-H",
                "Referer: https://www.pushplus.plus/",
                "-o",
                str(dest),
                fetch_url,
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0 and dest.exists() and dest.stat().st_size > 0:
            downloaded.append((fetch_url, name))
            return name, False
    except Exception as exc:
        print(f"WARN: download failed {fetch_url}: {exc}", file=sys.stderr)

    dest.unlink(missing_ok=True)
    failed.append((fetch_url, name))
    return cdn_public_url(url), True


def img_tag_to_md(match: re.Match, rel_path: str, cache: dict[str, str], downloaded: list, copied: list, failed: list) -> str:
    tag = match.group(0)
    src_m = re.search(r"src=['\"]([^'\"]+)['\"]", tag, re.I)
    if not src_m:
        return tag
    src = src_m.group(1)
    alt_m = re.search(r"alt=['\"]([^'\"]*)['\"]", tag, re.I)
    alt = alt_m.group(1) if alt_m else ""

    if "idqqimg.com" in src:
        prefix = image_prefix(rel_path)
        return f"![{alt or 'QQ群'}]({prefix}group.png)"

    if "pushplus" in src or src.startswith("/img/"):
        ref, external = ensure_image(src, cache, downloaded, copied, failed)
        if external:
            return f"![{alt}]({ref})"
        prefix = image_prefix(rel_path)
        return f"![{alt}]({prefix}{ref})"

    return tag


def convert_fancybox_block(block: str, rel_path: str, cache: dict[str, str], downloaded: list, copied: list, failed: list) -> str:
    img_m = re.search(r"<img\b[^>]*>", block, re.I | re.S)
    if not img_m:
        return block
    return img_tag_to_md(img_m, rel_path, cache, downloaded, copied, failed)


def convert_links(text: str) -> str:
    def link_repl(m: re.Match) -> str:
        link = m.group(1)
        if link.endswith(".html"):
            link = link[:-5] + ".md"
        return f"]({link})"

    return re.sub(r"\]\(([^)]+)\)", link_repl, text)


def convert_content(text: str, rel_path: str, cache: dict[str, str], downloaded: list, copied: list, failed: list) -> str:
    text = FRONTMATTER_RE.sub("", text)

    def fancybox_repl(m: re.Match) -> str:
        return convert_fancybox_block(m.group(0), rel_path, cache, downloaded, copied, failed)

    text = FANCYBOX_BLOCK_RE.sub(fancybox_repl, text)

    def img_repl(m: re.Match) -> str:
        return img_tag_to_md(m, rel_path, cache, downloaded, copied, failed)

    text = IMG_TAG_RE.sub(img_repl, text)
    text = convert_links(text)
    return text.rstrip() + "\n"


def build_readme(vue_text: str, existing: str, cache: dict[str, str], downloaded: list, copied: list, failed: list) -> str:
    vue_body = convert_content(vue_text, README_PATH, cache, downloaded, copied, failed)

    # Preserve doc directory from existing README if present
    doc_dir_marker = "## 文档目录"
    if doc_dir_marker in existing:
        doc_dir = existing[existing.index(doc_dir_marker) :]
        # Strip old intro, keep converted intro from vuepress until doc dir
        intro_lines = []
        for line in vue_body.splitlines():
            if line.startswith(doc_dir_marker):
                break
            intro_lines.append(line)
        intro = "\n".join(intro_lines).rstrip()

        # Expand doc directory with new pages from sidebar
        extra_links = """
- [积分群组](/function/paidTopic.md) - 积分群组功能
- [图片服务](/function/image.md) - 图片上传与管理
- [SDK说明](/guide/sdk.md) - 官方 SDK 使用说明
- [pushplus MCP Server](/guide/mcp.md) - MCP Server 配置
- [语音渠道配置](/channel/voice.md) - 语音渠道
- [桌面应用程序使用教程](/extend/desktop.md) - 桌面客户端
- [APP渠道使用说明](/channel/app.md) - App 渠道
- [微信ClawBot渠道使用说明](/channel/clawbot.md) - ClawBot 渠道
- [自定义webhook配置](/extend/diy.md) - 自定义 webhook
- [服务协议](/introduce/service.md) - 服务协议
- [用户隐私协议](/introduce/privacy.md) - 隐私协议
- [APP上没有通知弹框](/help/app.md) - App 通知问题
- [常用工具](/tool/index.md) - 在线调试工具
"""
        if "积分群组" not in doc_dir:
            doc_dir = doc_dir.replace(
                "- [好友消息](/function/friend.md)",
                "- [好友消息](/function/friend.md) - 好友功能介绍\n- [积分群组](/function/paidTopic.md) - 积分群组功能\n- [图片服务](/function/image.md) - 图片上传与管理",
            )
        if "SDK说明" not in doc_dir:
            doc_dir = doc_dir.replace(
                "- [Demo代码](/guide/demo.md)",
                "- [Demo代码](/guide/demo.md) - 各种语言的代码示例\n- [SDK说明](/guide/sdk.md) - 官方 SDK 使用说明\n- [pushplus MCP Server](/guide/mcp.md) - MCP Server 配置",
            )
        if "语音渠道配置" not in doc_dir:
            doc_dir = doc_dir.replace(
                "- [浏览器插件使用教程](/extend/extension.md)",
                "- [浏览器插件使用教程](/extend/extension.md) - 浏览器插件\n- [桌面应用程序使用教程](/extend/desktop.md) - 桌面客户端\n- [APP渠道使用说明](/channel/app.md) - App 渠道\n- [微信ClawBot渠道使用说明](/channel/clawbot.md) - ClawBot 渠道\n- [语音渠道配置](/channel/voice.md) - 语音渠道",
            )
        if "自定义webhook" not in doc_dir:
            doc_dir = doc_dir.replace(
                "- [调用IFTTT的webhook](/extend/ifttt.md)",
                "- [调用IFTTT的webhook](/extend/ifttt.md) - IFTTT集成\n- [自定义webhook配置](/extend/diy.md) - 自定义 webhook",
            )
        if "服务协议" not in doc_dir:
            doc_dir = doc_dir.replace(
                "- [联系我们](/introduce/contact.md)",
                "- [联系我们](/introduce/contact.md) - 联系方式\n- [服务协议](/introduce/service.md) - 服务协议\n- [用户隐私协议](/introduce/privacy.md) - 隐私协议",
            )
        if "APP上没有通知弹框" not in doc_dir:
            doc_dir = doc_dir.replace(
                "- [Get请求导致的问题](/help/get.md)",
                "- [APP上没有通知弹框](/help/app.md) - App 通知问题\n- [Get请求导致的问题](/help/get.md)",
            )
        if "常用工具" not in doc_dir:
            doc_dir = doc_dir + "\n\n### 常用工具\n- [常用工具](/tool/index.md) - 在线调试工具\n"

        return intro + "\n\n" + doc_dir

    return vue_body


def main():
    cache: dict[str, str] = {}
    downloaded: list[tuple[str, str]] = []
    copied: list[tuple[str, str]] = []
    failed: list[tuple[str, str]] = []
    updated: list[str] = []
    created: list[str] = []
    unchanged: list[str] = []

    vue_files = sorted(
        p.relative_to(VUEPRESS)
        for p in VUEPRESS.rglob("*.md")
        if ".vuepress" not in str(p) and str(p.relative_to(VUEPRESS)) not in SKIP_FILES
    )

    for rel in vue_files:
        rel_str = str(rel)
        src = VUEPRESS / rel
        dst = PUSHPLUS / rel
        vue_text = src.read_text(encoding="utf-8")

        if rel_str == README_PATH:
            existing = (PUSHPLUS / README_PATH).read_text(encoding="utf-8") if (PUSHPLUS / README_PATH).exists() else ""
            new_text = build_readme(vue_text, existing, cache, downloaded, copied, failed)
        elif rel_str == "guide/README.md":
            continue  # vuepress-only stub, skip
        elif rel_str == "tool/index.md":
            new_text = convert_content(vue_text, "tool/index.md", cache, downloaded, copied, failed)
        else:
            new_text = convert_content(vue_text, rel_str, cache, downloaded, copied, failed)

        dst.parent.mkdir(parents=True, exist_ok=True)
        old_text = dst.read_text(encoding="utf-8") if dst.exists() else None
        if old_text == new_text:
            unchanged.append(rel_str)
        else:
            dst.write_text(new_text, encoding="utf-8")
            (created if old_text is None else updated).append(rel_str)

    print("UPDATED:", len(updated))
    for f in updated:
        print(f"  U {f}")
    print("CREATED:", len(created))
    for f in created:
        print(f"  + {f}")
    print("UNCHANGED:", len(unchanged))
    print("IMAGES COPIED:", len(copied))
    print("IMAGES DOWNLOADED:", len(downloaded))
    if failed:
        print("IMAGES EXTERNAL FALLBACK:", len(failed))
        for url, name in failed[:20]:
            print(f"  ~ {name} <- {url}")
        if len(failed) > 20:
            print(f"  ... and {len(failed) - 20} more")


if __name__ == "__main__":
    main()
