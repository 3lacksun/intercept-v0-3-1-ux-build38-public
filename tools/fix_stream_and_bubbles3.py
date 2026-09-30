#!/usr/bin/env python3
from pathlib import Path

ROOT = Path("src")
BANNER = "[Truncated in chat view. Use Download to export the full reply.]"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if old not in text:
        raise SystemExit(f"pattern not found in {path}: {old[:80]!r}")
    path.write_text(text.replace(old, new, 1))


def main() -> None:
    replace_once(
        ROOT / "app/src/main/java/com/nexarenew/aiconsole/data/AppRepository.kt",
        """    fun messageById(id: String): Message? = try {
        readMessageRowCapped(id)
    } catch (failure: Throwable) {
        if (!isCursorWindowFailure(failure)) throw failure
        readMessageRowFallback(id)
    }
""",
        """    fun messageById(id: String): Message? = try {
        readMessageRowCapped(id)
    } catch (failure: Throwable) {
        if (!isCursorWindowFailure(failure)) throw failure
        readMessageRowFallback(id)
    }

    fun messageContentFull(id: String): String {
        val total = db.readableDatabase.rawQuery(
            \"SELECT ifnull(length(content),0) FROM messages WHERE id=?\",
            arrayOf(id),
        ).use { c -> if (!c.moveToFirst()) 0 else c.getInt(0) }
        if (total <= 0) return \"\"
        val chunkSize = 40_000
        if (total <= chunkSize) {
            return db.readableDatabase.rawQuery(
                \"SELECT ifnull(content,'') FROM messages WHERE id=?\",
                arrayOf(id),
            ).use { c -> if (!c.moveToFirst()) \"\" else c.getString(0).orEmpty() }
        }
        val out = StringBuilder(total)
        var offset = 1
        while (offset <= total) {
            val piece = db.readableDatabase.rawQuery(
                \"SELECT substr(content,?,?) FROM messages WHERE id=?\",
                arrayOf(offset.toString(), chunkSize.toString(), id),
            ).use { c -> if (!c.moveToFirst()) \"\" else c.getString(0).orEmpty() }
            if (piece.isEmpty()) break
            out.append(piece)
            offset += piece.length
        }
        return out.toString()
    }
""",
    )

    chat = ROOT / "app/src/main/java/com/nexarenew/aiconsole/ui/screens/ChatScreen.kt"
    replace_once(
        chat,
        """                        MessageBubble(
                            vm = vm,
                            message = message,
""",
        """                        MessageBubble(
                            vm = vm,
                            message = message,
                            loadFullContent = {
                                runCatching { repository.messageContentFull(message.id) }.getOrDefault(\"\")
                                    .ifBlank {
                                        message.content.replace(
                                            \"\\n\\n[Truncated in chat view. Use Download to export the full reply.]\",
                                            \"\",
                                        )
                                    }
                            },
""",
    )
    replace_once(
        chat,
        """                            onToggleSpeech = {
                                if (sttState == VoiceState.LISTENING || sttState == VoiceState.TRANSCRIBING) inlineVoice.pauseInput()
                                speaker.toggle(message.id, message.content)
                            },
                            onDownloadText = { filename, content ->
                                pendingTextExport = filename to content
                                textExportLauncher.launch(filename)
                            },
""",
        """                            onToggleSpeech = {
                                if (sttState == VoiceState.LISTENING || sttState == VoiceState.TRANSCRIBING) inlineVoice.pauseInput()
                                val spoken = runCatching { repository.messageContentFull(message.id) }.getOrDefault(\"\")
                                    .ifBlank { message.content.replace(\"\\n\\n[Truncated in chat view. Use Download to export the full reply.]\", \"\") }
                                speaker.toggle(message.id, spoken)
                                Toast.makeText(context, \"Speak\", Toast.LENGTH_SHORT).show()
                            },
                            onDownloadText = { filename, content ->
                                val exported = runCatching { repository.messageContentFull(message.id) }.getOrDefault(\"\")
                                    .ifBlank { content.replace(\"\\n\\n[Truncated in chat view. Use Download to export the full reply.]\", \"\") }
                                pendingTextExport = filename to exported
                                textExportLauncher.launch(filename)
                            },
""",
    )
    replace_once(
        chat,
        """    onRetry: (() -> Unit)? = null,
) {
""",
        """    onRetry: (() -> Unit)? = null,
    loadFullContent: () -> String = { message.content },
) {
""",
    )
    replace_once(
        chat,
        """    var moreActionsExpanded by remember { mutableStateOf(false) }
""",
        """    var moreActionsExpanded by remember { mutableStateOf(false) }
    var fullViewText by remember { mutableStateOf<String?>(null) }
""",
    )
    replace_once(
        chat,
        """                            ) {
                                clipboard.setText(AnnotatedString(message.content))
                                runCatching {
                                    val mgr = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
                                    mgr.setPrimaryClip(android.content.ClipData.newPlainText(\"message\", message.content))
                                }
                                actionStatus = \"Copied\"
                                Toast.makeText(context, \"Copied\", Toast.LENGTH_SHORT).show()
                            }
                            Box {
                                BubbleActionButton(
                                    label = \"More\", icon = Icons.Default.MoreHoriz,
                                    modifier = Modifier.testTag(\"bubble-more-${message.id}\"),
                                ) { moreActionsExpanded = true }
                                DropdownMenu(expanded = moreActionsExpanded, onDismissRequest = { moreActionsExpanded = false }) {
                                    DropdownMenuItem(
                                        text = { Text(\"Download .txt\") },
                                        leadingIcon = { Icon(Icons.Default.Download, null) },
                                        onClick = { moreActionsExpanded = false; actionStatus = \"Download prepared\"; onDownloadText(txtFilename, message.content) },
                                    )
                                    DropdownMenuItem(
                                        text = { Text(\"Save to Documents\") },
                                        leadingIcon = { Icon(Icons.Default.Description, null) },
                                        onClick = { moreActionsExpanded = false; actionStatus = \"Preparing Documents save\…\"; onSaveToDocuments(message) },
                                    )
                                    if (onRetry != null && retryEnabled) {
                                        DropdownMenuItem(
                                            text = { Text(if (message.status == MessageStatus.FAILED || message.status == MessageStatus.CANCELLED) \"Retry\" else \"Regenerate\") },
                                            leadingIcon = { Icon(Icons.Default.Refresh, null) },
                                            onClick = { moreActionsExpanded = false; actionStatus = \"Starting generation\…\"; onRetry() },
                                        )
                                    }
                                }
                            }
""",
        """                            ) {
                                val copied = loadFullContent()
                                clipboard.setText(AnnotatedString(copied))
                                runCatching {
                                    val mgr = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
                                    mgr.setPrimaryClip(android.content.ClipData.newPlainText(\"message\", copied))
                                }
                                actionStatus = \"Copied ${copied.length} characters\"
                                Toast.makeText(context, \"Copied ${copied.length} characters\", Toast.LENGTH_SHORT).show()
                            }
                            BubbleActionButton(
                                label = \"Full\", icon = Icons.Default.UnfoldMore,
                                modifier = Modifier.testTag(\"bubble-full-${message.id}\"),
                            ) {
                                fullViewText = loadFullContent()
                                actionStatus = \"Showing full reply\"
                            }
                            BubbleActionButton(
                                label = \"More\", icon = Icons.Default.MoreHoriz,
                                modifier = Modifier.testTag(\"bubble-more-${message.id}\"),
                            ) { moreActionsExpanded = true }
""",
    )
    replace_once(
        chat,
        """                val resolvedActionStatus = if (isSpeaking) \"Reading response aloud\" else actionStatus
                resolvedActionStatus?.let {
                    Text(it, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(top = 3.dp).semantics { liveRegion = LiveRegionMode.Polite })
                }
            }
        }
    }

}
""",
        """                val resolvedActionStatus = if (isSpeaking) \"Reading response aloud\" else actionStatus
                resolvedActionStatus?.let {
                    Text(it, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(top = 3.dp).semantics { liveRegion = LiveRegionMode.Polite })
                }
            }
        }
    }
    if (moreActionsExpanded) {
        AlertDialog(
            onDismissRequest = { moreActionsExpanded = false },
            title = { Text(\"Message actions\") },
            text = { Text(\"Export or regenerate this reply using the full stored text, not the shortened chat preview.\") },
            confirmButton = {
                Column {
                    TextButton(onClick = {
                        moreActionsExpanded = false
                        actionStatus = \"Download prepared\"
                        onDownloadText(txtFilename, loadFullContent())
                    }, modifier = Modifier.testTag(\"bubble-action-sheet-download\")) { Text(\"Download .txt\") }
                    TextButton(onClick = {
                        moreActionsExpanded = false
                        actionStatus = \"Preparing Documents save\…\"
                        onSaveToDocuments(message)
                    }) { Text(\"Save to Documents\") }
                    if (onRetry != null && retryEnabled) {
                        TextButton(onClick = {
                            moreActionsExpanded = false
                            actionStatus = \"Starting generation\…\"
                            onRetry()
                        }) { Text(if (message.status == MessageStatus.FAILED || message.status == MessageStatus.CANCELLED) \"Retry\" else \"Regenerate\") }
                    }
                    TextButton(onClick = { moreActionsExpanded = false }) { Text(\"Close\") }
                }
            },
        )
    }
    fullViewText?.let { body ->
        AlertDialog(
            onDismissRequest = { fullViewText = null },
            title = { Text(\"Full reply (${body.length} characters)\") },
            text = {
                Column(Modifier.fillMaxWidth().heightIn(max = 420.dp).verticalScroll(rememberScrollState())) {
                    Text(body, style = MaterialTheme.typography.bodyMedium)
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    runCatching {
                        val mgr = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
                        mgr.setPrimaryClip(android.content.ClipData.newPlainText(\"message\", body))
                    }
                    Toast.makeText(context, \"Copied ${body.length} characters\", Toast.LENGTH_SHORT).show()
                }) { Text(\"Copy\") }
            },
            dismissButton = { TextButton(onClick = { fullViewText = null }) { Text(\"Close\") } },
        )
    }

}
""",
    )
    replace_once(
        chat,
        """    FilledTonalButton(
        onClick = onClick,
        enabled = true,
        modifier = modifier.heightIn(min = 48.dp),
        contentPadding = PaddingValues(horizontal = 10.dp, vertical = 8.dp),
    ) {
""",
        """    Button(
        onClick = {
            runCatching { onClick() }.onFailure {
                android.util.Log.e(\"INTERCEPT\", \"bubble action failed\", it)
            }
        },
        enabled = true,
        modifier = modifier.heightIn(min = 48.dp).defaultMinSize(minWidth = 72.dp),
        contentPadding = PaddingValues(horizontal = 10.dp, vertical = 8.dp),
    ) {
""",
    )
    print(\"stream-and-bubble overlay 3 applied\")


if __name__ == \"__main__\":
    main()
