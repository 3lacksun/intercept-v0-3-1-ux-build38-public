#!/usr/bin/env python3
from pathlib import Path

ROOT = Path("src")
REPO = ROOT / "app/src/main/java/com/nexarenew/aiconsole/data/AppRepository.kt"
CHAT = ROOT / "app/src/main/java/com/nexarenew/aiconsole/ui/screens/ChatScreen.kt"


def must_replace(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if old not in text:
        raise SystemExit("pattern not found in %s: %r" % (path, old[:90]))
    path.write_text(text.replace(old, new, 1))


def main() -> None:
    helper = """
    fun messageContentFull(id: String): String {
        val total = db.readableDatabase.rawQuery(
            "SELECT ifnull(length(content),0) FROM messages WHERE id=?",
            arrayOf(id),
        ).use { c -> if (!c.moveToFirst()) 0 else c.getInt(0) }
        if (total <= 0) return ""
        val chunkSize = 40_000
        if (total <= chunkSize) {
            return db.readableDatabase.rawQuery(
                "SELECT ifnull(content,'') FROM messages WHERE id=?",
                arrayOf(id),
            ).use { c -> if (!c.moveToFirst()) "" else c.getString(0).orEmpty() }
        }
        val out = StringBuilder(total)
        var offset = 1
        while (offset <= total) {
            val piece = db.readableDatabase.rawQuery(
                "SELECT substr(content,?,?) FROM messages WHERE id=?",
                arrayOf(offset.toString(), chunkSize.toString(), id),
            ).use { c -> if (!c.moveToFirst()) "" else c.getString(0).orEmpty() }
            if (piece.isEmpty()) break
            out.append(piece)
            offset += piece.length
        }
        return out.toString()
    }
"""
    must_replace(
        REPO,
        "        readMessageRowFallback(id)\n    }\n",
        "        readMessageRowFallback(id)\n    }\n" + helper,
    )

    must_replace(
        CHAT,
        "                            vm = vm,\n                            message = message,\n",
        "                            vm = vm,\n                            message = message,\n"
        "                            loadFullContent = {\n"
        "                                runCatching { repository.messageContentFull(message.id) }.getOrDefault(\"\")\n"
        "                                    .ifBlank { message.content.substringBefore(\"\\n\\n[Truncated in chat view.\") }\n"
        "                            },\n",
    )
    must_replace(
        CHAT,
        "                                speaker.toggle(message.id, message.content)\n",
        "                                val spoken = runCatching { repository.messageContentFull(message.id) }.getOrDefault(\"\")\n"
        "                                    .ifBlank { message.content.substringBefore(\"\\n\\n[Truncated in chat view.\") }\n"
        "                                speaker.toggle(message.id, spoken)\n"
        "                                Toast.makeText(context, \"Speak\", Toast.LENGTH_SHORT).show()\n",
    )
    must_replace(
        CHAT,
        "                                pendingTextExport = filename to content\n",
        "                                val exported = runCatching { repository.messageContentFull(message.id) }.getOrDefault(\"\")\n"
        "                                    .ifBlank { content.substringBefore(\"\\n\\n[Truncated in chat view.\") }\n"
        "                                pendingTextExport = filename to exported\n",
    )
    must_replace(
        CHAT,
        "    onRetry: (() -> Unit)? = null,\n) {",
        "    onRetry: (() -> Unit)? = null,\n    loadFullContent: () -> String = { message.content },\n) {",
    )
    must_replace(
        CHAT,
        "    var moreActionsExpanded by remember { mutableStateOf(false) }\n",
        "    var moreActionsExpanded by remember { mutableStateOf(false) }\n"
        "    var fullViewText by remember { mutableStateOf<String?>(null) }\n",
    )
    must_replace(
        CHAT,
        "                                clipboard.setText(AnnotatedString(message.content))\n"
        "                                runCatching {\n"
        "                                    val mgr = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager\n"
        "                                    mgr.setPrimaryClip(android.content.ClipData.newPlainText(\"message\", message.content))\n"
        "                                }\n"
        "                                actionStatus = \"Copied\"\n"
        "                                Toast.makeText(context, \"Copied\", Toast.LENGTH_SHORT).show()\n",
        "                                val copied = loadFullContent()\n"
        "                                clipboard.setText(AnnotatedString(copied))\n"
        "                                runCatching {\n"
        "                                    val mgr = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager\n"
        "                                    mgr.setPrimaryClip(android.content.ClipData.newPlainText(\"message\", copied))\n"
        "                                }\n"
        "                                actionStatus = \"Copied ${copied.length} characters\"\n"
        "                                Toast.makeText(context, \"Copied ${copied.length} characters\", Toast.LENGTH_SHORT).show()\n",
    )
    must_replace(
        CHAT,
        "                            Box {\n"
        "                                BubbleActionButton(\n"
        "                                    label = \"More\", icon = Icons.Default.MoreHoriz,\n"
        "                                    modifier = Modifier.testTag(\"bubble-more-${message.id}\"),\n"
        "                                ) { moreActionsExpanded = true }\n",
        "                            BubbleActionButton(\n"
        "                                label = \"Full\", icon = Icons.Default.UnfoldMore,\n"
        "                                modifier = Modifier.testTag(\"bubble-full-${message.id}\"),\n"
        "                            ) { fullViewText = loadFullContent(); actionStatus = \"Showing full reply\" }\n"
        "                            BubbleActionButton(\n"
        "                                label = \"More\", icon = Icons.Default.MoreHoriz,\n"
        "                                modifier = Modifier.testTag(\"bubble-more-${message.id}\"),\n"
        "                            ) { moreActionsExpanded = true }\n"
        "                            if (false) Box {\n"
        "                                BubbleActionButton(\n"
        "                                    label = \"More\", icon = Icons.Default.MoreHoriz,\n"
        "                                    modifier = Modifier.testTag(\"bubble-more-hidden-${message.id}\"),\n"
        "                                ) { moreActionsExpanded = true }\n",
    )
    must_replace(
        CHAT,
        "                val resolvedActionStatus = if (isSpeaking) \"Reading response aloud\" else actionStatus\n",
        "                if (moreActionsExpanded) {\n"
        "                    AlertDialog(\n"
        "                        onDismissRequest = { moreActionsExpanded = false },\n"
        "                        title = { Text(\"Message actions\") },\n"
        "                        text = { Text(\"These actions use the full stored reply, not the shortened chat preview.\") },\n"
        "                        confirmButton = {\n"
        "                            Column {\n"
        "                                TextButton(onClick = {\n"
        "                                    moreActionsExpanded = false\n"
        "                                    actionStatus = \"Download prepared\"\n"
        "                                    onDownloadText(txtFilename, loadFullContent())\n"
        "                                }, modifier = Modifier.testTag(\"bubble-action-sheet-download\")) { Text(\"Download .txt\") }\n"
        "                                TextButton(onClick = {\n"
        "                                    moreActionsExpanded = false\n"
        "                                    actionStatus = \"Preparing Documents save\"\n"
        "                                    onSaveToDocuments(message)\n"
        "                                }) { Text(\"Save to Documents\") }\n"
        "                                TextButton(onClick = { moreActionsExpanded = false }) { Text(\"Close\") }\n"
        "                            }\n"
        "                        },\n"
        "                    )\n"
        "                }\n"
        "                fullViewText?.let { body ->\n"
        "                    AlertDialog(\n"
        "                        onDismissRequest = { fullViewText = null },\n"
        "                        title = { Text(\"Full reply (${body.length} characters)\") },\n"
        "                        text = {\n"
        "                            Column(Modifier.fillMaxWidth().heightIn(max = 420.dp).verticalScroll(rememberScrollState())) {\n"
        "                                Text(body, style = MaterialTheme.typography.bodyMedium)\n"
        "                            }\n"
        "                        },\n"
        "                        confirmButton = {\n"
        "                            TextButton(onClick = {\n"
        "                                runCatching {\n"
        "                                    val mgr = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager\n"
        "                                    mgr.setPrimaryClip(android.content.ClipData.newPlainText(\"message\", body))\n"
        "                                }\n"
        "                                Toast.makeText(context, \"Copied ${body.length} characters\", Toast.LENGTH_SHORT).show()\n"
        "                            }) { Text(\"Copy\") }\n"
        "                        },\n"
        "                        dismissButton = { TextButton(onClick = { fullViewText = null }) { Text(\"Close\") } },\n"
        "                    )\n"
        "                }\n"
        "                val resolvedActionStatus = if (isSpeaking) \"Reading response aloud\" else actionStatus\n",
    )
    must_replace(
        CHAT,
        "        onClick = onClick,\n        enabled = true,\n        modifier = modifier.heightIn(min = 48.dp),\n",
        "        onClick = { runCatching { onClick() } },\n        enabled = true,\n        modifier = modifier.heightIn(min = 48.dp).defaultMinSize(minWidth = 72.dp),\n",
    )
    print("stream-and-bubble overlay 3 applied")


if __name__ == "__main__":
    main()
