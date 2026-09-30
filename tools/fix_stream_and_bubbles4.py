#!/usr/bin/env python3
from pathlib import Path

CHAT = Path("src/app/src/main/java/com/nexarenew/aiconsole/ui/screens/ChatScreen.kt")


def must_replace(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if old not in text:
        raise SystemExit("pattern not found in %s: %r" % (path, old[:100]))
    path.write_text(text.replace(old, new, 1))


def main() -> None:
    must_replace(
        CHAT,
        "import androidx.compose.foundation.layout.ExperimentalLayoutApi\n",
        "import androidx.compose.foundation.clickable\n"
        "import androidx.compose.foundation.layout.ExperimentalLayoutApi\n",
    )
    must_replace(
        CHAT,
        "    var speakingMessageId by remember { mutableStateOf<String?>(null) }\n",
        "    var speakingMessageId by remember { mutableStateOf<String?>(null) }\n"
        "    var selectedActionMessageId by remember { mutableStateOf<String?>(null) }\n"
        "    var stickyFullText by remember { mutableStateOf<String?>(null) }\n",
    )
    must_replace(
        CHAT,
        "                            loadFullContent = {\n"
        "                                runCatching { repository.messageContentFull(message.id) }.getOrDefault(\"\")\n"
        "                                    .ifBlank { message.content.substringBefore(\"\\n\\n[Truncated in chat view.\") }\n"
        "                            },\n",
        "                            loadFullContent = {\n"
        "                                runCatching { repository.messageContentFull(message.id) }.getOrDefault(\"\")\n"
        "                                    .ifBlank { message.content.substringBefore(\"\\n\\n[Truncated in chat view.\") }\n"
        "                            },\n"
        "                            onSelect = { selectedActionMessageId = message.id },\n",
    )
    must_replace(
        CHAT,
        "    loadFullContent: () -> String = { message.content },\n) {",
        "    loadFullContent: () -> String = { message.content },\n"
        "    onSelect: () -> Unit = {},\n) {",
    )
    must_replace(
        CHAT,
        "            modifier = Modifier.fillMaxWidth(0.90f),\n",
        "            modifier = Modifier.fillMaxWidth(0.90f).clickable(onClick = onSelect),\n",
    )
    sticky = '''\n        val actionTarget = msgs.firstOrNull { it.id == selectedActionMessageId }\n            ?: msgs.lastOrNull { it.role.equals(\"assistant\", true) && it.content.isNotBlank() }\n        if (!imeVisible && actionTarget != null && ChatMessageActionPolicy.contentActionsAvailable(actionTarget.status, actionTarget.content)) {\n            Surface(\n                color = MaterialTheme.colorScheme.secondaryContainer,\n                contentColor = MaterialTheme.colorScheme.onSecondaryContainer,\n                shape = RoundedCornerShape(16.dp),\n                modifier = Modifier.fillMaxWidth().padding(top = 6.dp, bottom = 4.dp).testTag(\"chat-sticky-actions\"),\n            ) {\n                Column(Modifier.padding(horizontal = 10.dp, vertical = 8.dp)) {\n                    Text(\n                        if (actionTarget.role.equals(\"assistant\", true)) \"Reply actions\" else \"Message actions\",\n                        style = MaterialTheme.typography.labelMedium,\n                    )\n                    Row(\n                        modifier = Modifier.fillMaxWidth().padding(top = 6.dp),\n                        horizontalArrangement = Arrangement.spacedBy(6.dp),\n                    ) {\n                        Button(\n                            onClick = {\n                                if (sttState == VoiceState.LISTENING || sttState == VoiceState.TRANSCRIBING) inlineVoice.pauseInput()\n                                val spoken = runCatching { repository.messageContentFull(actionTarget.id) }.getOrDefault(\"\")\n                                    .ifBlank { actionTarget.content.substringBefore(\"\\n\\n[Truncated in chat view.\") }\n                                speaker.toggle(actionTarget.id, spoken)\n                                Toast.makeText(context, \"Speak\", Toast.LENGTH_SHORT).show()\n                            },\n                            modifier = Modifier.weight(1f).heightIn(min = 48.dp).testTag(\"sticky-speak\"),\n                        ) { Text(if (speakingMessageId == actionTarget.id) \"Stop\" else \"Speak\") }\n                        Button(\n                            onClick = {\n                                val copied = runCatching { repository.messageContentFull(actionTarget.id) }.getOrDefault(\"\")\n                                    .ifBlank { actionTarget.content.substringBefore(\"\\n\\n[Truncated in chat view.\") }\n                                runCatching {\n                                    val mgr = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager\n                                    mgr.setPrimaryClip(android.content.ClipData.newPlainText(\"message\", copied))\n                                }\n                                Toast.makeText(context, \"Copied ${copied.length} characters\", Toast.LENGTH_SHORT).show()\n                            },\n                            modifier = Modifier.weight(1f).heightIn(min = 48.dp).testTag(\"sticky-copy\"),\n                        ) { Text(\"Copy\") }\n                    }\n                    Row(\n                        modifier = Modifier.fillMaxWidth().padding(top = 6.dp),\n                        horizontalArrangement = Arrangement.spacedBy(6.dp),\n                    ) {\n                        Button(\n                            onClick = {\n                                stickyFullText = runCatching { repository.messageContentFull(actionTarget.id) }.getOrDefault(\"\")\n                                    .ifBlank { actionTarget.content.substringBefore(\"\\n\\n[Truncated in chat view.\") }\n                            },\n                            modifier = Modifier.weight(1f).heightIn(min = 48.dp).testTag(\"sticky-full\"),\n                        ) { Text(\"Full\") }\n                        Button(\n                            onClick = {\n                                val exported = runCatching { repository.messageContentFull(actionTarget.id) }.getOrDefault(\"\")\n                                    .ifBlank { actionTarget.content.substringBefore(\"\\n\\n[Truncated in chat view.\") }\n                                val filename = ChatExportPolicy.txtFilename(actionTarget.role, actionTarget.createdAt)\n                                pendingTextExport = filename to exported\n                                textExportLauncher.launch(filename)\n                            },\n                            modifier = Modifier.weight(1f).heightIn(min = 48.dp).testTag(\"sticky-download\"),\n                        ) { Text(\"Download\") }\n                    }\n                }\n            }\n        }\n        stickyFullText?.let { body ->\n            AlertDialog(\n                onDismissRequest = { stickyFullText = null },\n                title = { Text(\"Full reply (${body.length} characters)\") },\n                text = {\n                    Column(Modifier.fillMaxWidth().heightIn(max = 420.dp).verticalScroll(rememberScrollState())) {\n                        Text(body, style = MaterialTheme.typography.bodyMedium)\n                    }\n                },\n                confirmButton = {\n                    TextButton(onClick = {\n                        runCatching {\n                            val mgr = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager\n                            mgr.setPrimaryClip(android.content.ClipData.newPlainText(\"message\", body))\n                        }\n                        Toast.makeText(context, \"Copied ${body.length} characters\", Toast.LENGTH_SHORT).show()\n                    }) { Text(\"Copy\") }\n                },\n                dismissButton = { TextButton(onClick = { stickyFullText = null }) { Text(\"Close\") } },\n            )\n        }\n'''
    must_replace(
        CHAT,
        "        if (!imeVisible && !autoFollow && msgs.isNotEmpty()) {",
        sticky + "\n        if (!imeVisible && !autoFollow && msgs.isNotEmpty()) {",
    )
    print("stream-and-bubble overlay 4 applied")


if __name__ == "__main__":
    main()
