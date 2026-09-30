#!/usr/bin/env python3
from pathlib import Path

ROOT = Path("src")


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if old not in text:
        raise SystemExit(f"pattern not found in {path}")
    path.write_text(text.replace(old, new, 1))


def main() -> None:
    replace_once(
        ROOT / "app/src/main/java/com/nexarenew/aiconsole/network/ProviderClient.kt",
        '''            if (terminal == StreamTerminalKind.INCOMPLETE) {
                throw IncompleteProviderStreamException(provider, "Provider stream ended without [DONE] or a terminal finish_reason.")
            }
            return ProviderStreamResult(terminal, finishReason)''',
        "            return ProviderStreamResult(terminal, finishReason)",
    )
    replace_once(
        ROOT / "app/src/main/java/com/nexarenew/aiconsole/ui/AppViewModel.kt",
        '''                    repo.streamClaimedOutbox(request, owner, token, { delta ->
                        rawReplyBuf.append(delta)
                        publishStreaming()
                    }, { reasoningDelta ->
                        providerReasoningBuf.append(reasoningDelta)
                        publishStreaming()
                    }, { usage -> providerUsage = usage })
                    publishStreaming(force = true)''',
        '''                    try {
                        repo.streamClaimedOutbox(request, owner, token, { delta ->
                            rawReplyBuf.append(delta)
                            publishStreaming()
                        }, { reasoningDelta ->
                            providerReasoningBuf.append(reasoningDelta)
                            publishStreaming()
                        }, { usage -> providerUsage = usage })
                    } finally {
                        publishStreaming(force = true)
                    }''',
    )
    chat = ROOT / "app/src/main/java/com/nexarenew/aiconsole/ui/screens/ChatScreen.kt"
    replace_once(
        chat,
        '''                                clipboard.setText(AnnotatedString(message.content))
                                actionStatus = "Copied"
                                Toast.makeText(context, "Copied", Toast.LENGTH_SHORT).show()
                            }''',
        '''                                clipboard.setText(AnnotatedString(message.content))
                                runCatching {
                                    val mgr = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
                                    mgr.setPrimaryClip(android.content.ClipData.newPlainText("message", message.content))
                                }
                                actionStatus = "Copied"
                                Toast.makeText(context, "Copied", Toast.LENGTH_SHORT).show()
                            }''',
    )
    replace_once(
        chat,
        '''    FilledTonalButton(
        onClick = onClick,
        modifier = modifier.heightIn(min = 48.dp),
        contentPadding = PaddingValues(horizontal = 8.dp, vertical = 6.dp),
    ) {''',
        '''    FilledTonalButton(
        onClick = onClick,
        enabled = true,
        modifier = modifier.heightIn(min = 48.dp),
        contentPadding = PaddingValues(horizontal = 10.dp, vertical = 8.dp),
    ) {''',
    )
    print("stream-and-bubble overlay 2 applied")


if __name__ == "__main__":
    main()
