#!/usr/bin/env python3
from pathlib import Path

REPO = Path("src/app/src/main/java/com/nexarenew/aiconsole/data/AppRepository.kt")
CHAT = Path("src/app/src/main/java/com/nexarenew/aiconsole/ui/screens/ChatScreen.kt")
CONT = Path("src/app/src/main/java/com/nexarenew/aiconsole/domain/StreamCompletionPolicy.kt")
MODELS = Path("src/app/src/main/java/com/nexarenew/aiconsole/model/Models.kt")


def must_replace(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if old not in text:
        raise SystemExit("pattern not found in %s: %r" % (path, old[:160]))
    path.write_text(text.replace(old, new, 1))


def main() -> None:
    must_replace(
        REPO,
        "        return ids.asReversed().mapNotNull(::messageById)\n    }\n",
        "        val ordered = ids.asReversed()\n"
        "        return ordered.mapNotNull { id ->\n"
        "            val row = messageById(id) ?: return@mapNotNull null\n"
        "            val full = runCatching { messageContentFull(id) }.getOrDefault(\"\")\n"
        "            if (full.isBlank()) row else row.copy(content = full)\n"
        "        }\n"
        "    }\n",
    )
    must_replace(
        REPO,
        "        if (text.length >= max) text.take(max) + \"\\n\\n[Truncated in chat view. Use Download to export the full reply.]\" else text\n",
        "        text\n",
    )
    must_replace(
        REPO,
        "        private const val UI_CONTENT_CHARS = 6_000\n"
        "        private const val UI_REASONING_CHARS = 2_000\n",
        "        private const val UI_CONTENT_CHARS = 120_000\n"
        "        private const val UI_REASONING_CHARS = 24_000\n",
    )
    must_replace(
        CONT,
        "    const val MAX_CONTINUATIONS = 8\n",
        "    const val MAX_CONTINUATIONS = 24\n",
    )
    if MODELS.exists():
        text = MODELS.read_text()
        text = text.replace("val maxTokens: Int = 4096,", "val maxTokens: Int = 32768,", 3)
        MODELS.write_text(text)

    must_replace(
        CHAT,
        "    var selectedActionMessageId by remember { mutableStateOf<String?>(null) }\n"
        "    var stickyFullText by remember { mutableStateOf<String?>(null) }\n",
        "    var selectedActionMessageId by remember { mutableStateOf<String?>(null) }\n"
        "    var stickyFullText by remember { mutableStateOf<String?>(null) }\n"
        "    var actionSheetOpen by remember { mutableStateOf(false) }\n",
    )
    must_replace(
        CHAT,
        "                            onSelect = { selectedActionMessageId = message.id },\n",
        "                            onSelect = {\n"
        "                                selectedActionMessageId = message.id\n"
        "                                actionSheetOpen = true\n"
        "                            },\n",
    )
    must_replace(
        CHAT,
        "        if (!imeVisible && actionTarget != null && ChatMessageActionPolicy.contentActionsAvailable(actionTarget.status, actionTarget.content)) {",
        "        if (actionTarget != null && ChatMessageActionPolicy.contentActionsAvailable(actionTarget.status, actionTarget.content)) {",
    )
    must_replace(
        CHAT,
        "        stickyFullText?.let { body ->\n",
        "        if (actionSheetOpen && actionTarget != null) {\n"
        "            AlertDialog(\n"
        "                onDismissRequest = { actionSheetOpen = false },\n"
        "                title = { Text(\"Message actions\") },\n"
        "                text = {\n"
        "                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {\n"
        "                        Text(\n"
        "                            \"${actionTarget.role} · ${actionTarget.content.length} characters in view\",\n"
        "                            style = MaterialTheme.typography.bodySmall,\n"
        "                        )\n"
        "                        Button(\n"
        "                            onClick = {\n"
        "                                if (sttState == VoiceState.LISTENING || sttState == VoiceState.TRANSCRIBING) inlineVoice.pauseInput()\n"
        "                                val spoken = runCatching { repository.messageContentFull(actionTarget.id) }.getOrDefault(\"\")\n"
        "                                    .ifBlank { actionTarget.content }\n"
        "                                speaker.toggle(actionTarget.id, spoken)\n"
        "                                Toast.makeText(context, if (speakingMessageId == actionTarget.id) \"Stopped\" else \"Speak \" + spoken.length + \" characters\", Toast.LENGTH_SHORT).show()\n"
        "                            },\n"
        "                            modifier = Modifier.fillMaxWidth().heightIn(min = 52.dp).testTag(\"sheet-speak\"),\n"
        "                        ) { Text(if (speakingMessageId == actionTarget.id) \"Stop reading\" else \"Speak\") }\n"
        "                        Button(\n"
        "                            onClick = {\n"
        "                                val copied = runCatching { repository.messageContentFull(actionTarget.id) }.getOrDefault(\"\")\n"
        "                                    .ifBlank { actionTarget.content }\n"
        "                                runCatching {\n"
        "                                    val mgr = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager\n"
        "                                    mgr.setPrimaryClip(android.content.ClipData.newPlainText(\"message\", copied))\n"
        "                                }\n"
        "                                Toast.makeText(context, \"Copied \" + copied.length + \" characters\", Toast.LENGTH_SHORT).show()\n"
        "                            },\n"
        "                            modifier = Modifier.fillMaxWidth().heightIn(min = 52.dp).testTag(\"sheet-copy\"),\n"
        "                        ) { Text(\"Copy full reply\") }\n"
        "                        Button(\n"
        "                            onClick = {\n"
        "                                stickyFullText = runCatching { repository.messageContentFull(actionTarget.id) }.getOrDefault(\"\")\n"
        "                                    .ifBlank { actionTarget.content }\n"
        "                                actionSheetOpen = false\n"
        "                            },\n"
        "                            modifier = Modifier.fillMaxWidth().heightIn(min = 52.dp).testTag(\"sheet-full\"),\n"
        "                        ) { Text(\"View full text\") }\n"
        "                        Button(\n"
        "                            onClick = {\n"
        "                                val exported = runCatching { repository.messageContentFull(actionTarget.id) }.getOrDefault(\"\")\n"
        "                                    .ifBlank { actionTarget.content }\n"
        "                                val filename = ChatExportPolicy.txtFilename(actionTarget.role, actionTarget.createdAt)\n"
        "                                pendingTextExport = filename to exported\n"
        "                                textExportLauncher.launch(filename)\n"
        "                                actionSheetOpen = false\n"
        "                            },\n"
        "                            modifier = Modifier.fillMaxWidth().heightIn(min = 52.dp).testTag(\"sheet-download\"),\n"
        "                        ) { Text(\"Download .txt\") }\n"
        "                    }\n"
        "                },\n"
        "                confirmButton = { TextButton(onClick = { actionSheetOpen = false }) { Text(\"Close\") } },\n"
        "            )\n"
        "        }\n"
        "        stickyFullText?.let { body ->\n",
    )
    must_replace(
        CHAT,
        "        if (message.status == MessageStatus.STREAMING || message.content.length > 8_000) {\n",
        "        if (true) {\n",
    )
    print("stream-and-bubble overlay 5 applied")


if __name__ == \"__main__\":
    main()
