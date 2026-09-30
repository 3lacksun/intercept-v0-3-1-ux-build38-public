#!/usr/bin/env python3
from pathlib import Path

REPO = Path("src/app/src/main/java/com/nexarenew/aiconsole/data/AppRepository.kt")
CHAT = Path("src/app/src/main/java/com/nexarenew/aiconsole/ui/screens/ChatScreen.kt")


def must_replace(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if old not in text:
        raise SystemExit("pattern not found in %s: %r" % (path, old[:120]))
    path.write_text(text.replace(old, new, 1))


def main() -> None:
    must_replace(
        REPO,
        "        private const val UI_CONTENT_CHARS = 6_000\n"
        "        private const val UI_REASONING_CHARS = 2_000\n",
        "        private const val UI_CONTENT_CHARS = 200_000\n"
        "        private const val UI_REASONING_CHARS = 24_000\n",
    )
    must_replace(
        REPO,
        "        return ids.asReversed().mapNotNull(::messageById)\n    }\n",
        "        val ordered = ids.asReversed()\n"
        "        val fullIds = ordered.takeLast(8).toSet()\n"
        "        return ordered.mapNotNull { id ->\n"
        "            val row = messageById(id) ?: return@mapNotNull null\n"
        "            if (id !in fullIds) return@mapNotNull row\n"
        "            val full = runCatching { messageContentFull(id) }.getOrDefault(\"\")\n"
        "            if (full.isBlank()) row else row.copy(content = full)\n"
        "        }\n"
        "    }\n",
    )
    must_replace(
        REPO,
        "        if (text.length >= max) text.take(max) + \"\\n\\n[Truncated in chat view. Use Download to export the full reply.]\" else text\n",
        "        if (text.length >= max) text else text\n",
    )
    must_replace(
        CHAT,
        "        if (message.status == MessageStatus.STREAMING || message.content.length > 8_000) {\n",
        "        if (message.status == MessageStatus.STREAMING || message.content.length > 4_000) {\n",
    )
    print("long-content overlay applied")


if __name__ == "__main__":
    main()
