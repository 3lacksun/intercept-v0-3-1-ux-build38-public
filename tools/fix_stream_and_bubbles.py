#!/usr/bin/env python3
from pathlib import Path

ROOT = Path("src")


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if old not in text:
        raise SystemExit(f"pattern not found in {path}")
    path.write_text(text.replace(old, new, 1))


def write_if(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> None:
    write_if(
        ROOT / "app/src/main/java/com/nexarenew/aiconsole/domain/ChatMessageActionPolicy.kt",
        """package com.nexarenew.aiconsole.domain

import com.nexarenew.aiconsole.model.MessageStatus

/** Stable availability policy for actions that operate on a message's final visible content. */
object ChatMessageActionPolicy {
    fun contentActionsAvailable(status: MessageStatus, content: String): Boolean =
        content.isNotBlank() && status != MessageStatus.PENDING
}
""",
    )
    replace_once(
        ROOT / "app/src/main/java/com/nexarenew/aiconsole/domain/StreamIdlePolicy.kt",
        "    const val INTER_BYTE_MS = 45_000L",
        "    const val INTER_BYTE_MS = 180_000L",
    )
    replace_once(
        ROOT / "app/src/main/java/com/nexarenew/aiconsole/domain/StreamCompletionPolicy.kt",
        '''    fun continuationInstruction(): String =
        "Continue exactly from where the previous response stopped. Do not repeat text already emitted. Finish the answer completely."
}''',
        '''    fun continuationInstruction(): String =
        "Continue exactly from where the previous response stopped. Do not repeat text already emitted. Finish the answer completely."

    fun isLengthLimit(finishReason: String?): Boolean {
        val reason = finishReason?.lowercase().orEmpty()
        return reason == "length" || reason == "max_tokens" || reason == "max_output_tokens"
    }

    fun shouldContinue(
        kind: StreamTerminalKind,
        finishReason: String? = null,
        outputTokens: Long? = null,
        maxTokens: Int = 0,
    ): Boolean {
        if (kind == StreamTerminalKind.LENGTH || kind == StreamTerminalKind.INCOMPLETE) return true
        if (isLengthLimit(finishReason)) return true
        return outputTokens != null && maxTokens > 0 && outputTokens >= maxTokens.toLong()
    }
}''',
    )
    test = ROOT / "app/src/test/java/com/nexarenew/aiconsole/domain/PureDomainTest.kt"
    old_idle = (
        "        assertFalse(StreamIdlePolicy.isStalled(44_999, receivedAnyBytes = true))\n"
        "        assertTrue(StreamIdlePolicy.isStalled(45_000, receivedAnyBytes = true))"
    )
    if test.exists() and old_idle in test.read_text():
        replace_once(
            test,
            old_idle,
            "        assertFalse(StreamIdlePolicy.isStalled(179_999, receivedAnyBytes = true))\n"
            "        assertTrue(StreamIdlePolicy.isStalled(180_000, receivedAnyBytes = true))",
        )
    replace_once(
        ROOT / "app/src/main/java/com/nexarenew/aiconsole/network/ProviderClient.kt",
        "import com.nexarenew.aiconsole.domain.StreamTerminalKind",
        "import com.nexarenew.aiconsole.domain.StreamContinuationPolicy\n"
        "import com.nexarenew.aiconsole.domain.StreamTerminalKind",
    )
    replace_once(
        ROOT / "app/src/main/java/com/nexarenew/aiconsole/network/ProviderClient.kt",
        '                finishReason.equals("length", true) -> StreamTerminalKind.LENGTH',
        "                StreamContinuationPolicy.isLengthLimit(finishReason) -> StreamTerminalKind.LENGTH",
    )
    replace_once(
        ROOT / "app/src/main/java/com/nexarenew/aiconsole/network/ProviderClient.kt",
        '''    private fun extractDelta(payload: String): String? = runCatching {
        val delta = JSONObject(payload)
            .optJSONArray("choices")
            ?.optJSONObject(0)
            ?.optJSONObject("delta") ?: return@runCatching null
        if (!delta.has("content") || delta.isNull("content")) return@runCatching null
        delta.optString("content").takeIf { it.isNotEmpty() && it != "null" }
    }.getOrNull()''',
        '''    private fun extractDelta(payload: String): String? = runCatching {
        val choice = JSONObject(payload).optJSONArray("choices")?.optJSONObject(0) ?: return@runCatching null
        textualContent(choice.optJSONObject("delta"))
            ?: textualContent(choice.optJSONObject("message"))
            ?: choice.optString("text").takeIf { it.isNotEmpty() && it != "null" }
    }.getOrNull()

    private fun textualContent(container: JSONObject?): String? {
        if (container == null) return null
        if (!container.has("content") || container.isNull("content")) {
            return container.optString("text").takeIf { it.isNotEmpty() && it != "null" }
        }
        val raw = container.get("content")
        return when (raw) {
            is String -> raw.takeIf { it.isNotEmpty() && it != "null" }
            is JSONArray -> buildString {
                for (i in 0 until raw.length()) {
                    val item = raw.opt(i)
                    when (item) {
                        is String -> if (item.isNotEmpty()) append(item)
                        is JSONObject -> {
                            val text = item.optString("text").ifBlank { item.optString("content") }
                            if (text.isNotBlank() && text != "null") append(text)
                        }
                    }
                }
            }.takeIf { it.isNotEmpty() }
            else -> raw.toString().takeIf { it.isNotEmpty() && it != "null" }
        }
    }''',
    )
    replace_once(
        ROOT / "app/src/main/java/com/nexarenew/aiconsole/data/AppRepository.kt",
        "                if (result?.terminalKind == StreamTerminalKind.COMPLETE) return",
        '''                val shouldContinue = result == null || StreamContinuationPolicy.shouldContinue(
                    result.terminalKind,
                    result.finishReason,
                    attemptUsage?.outputTokens,
                    request.maxTokens,
                )
                if (!shouldContinue) return''',
    )
    chat = ROOT / "app/src/main/java/com/nexarenew/aiconsole/ui/screens/ChatScreen.kt"
    replace_once(
        chat,
        "import androidx.compose.foundation.layout.*",
        "import androidx.compose.foundation.layout.ExperimentalLayoutApi\n"
        "import androidx.compose.foundation.layout.*",
    )
    replace_once(
        chat,
        "@Composable private fun MessageBubble(",
        "@OptIn(ExperimentalLayoutApi::class)\n@Composable private fun MessageBubble(",
    )
    replace_once(
        chat,
        "                    if (isAssistant && message.status == MessageStatus.COMPLETED && message.content.isNotBlank()) {",
        "                    if (isAssistant && message.content.isNotBlank() && message.status != MessageStatus.PENDING) {",
    )
    replace_once(
        chat,
        '''                when {
                    message.status == MessageStatus.STREAMING -> {
                        Text(
                            "Generating… actions available when complete.",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.padding(top = 8.dp).semantics { liveRegion = LiveRegionMode.Polite },
                        )
                    }
                    actionsAvailable -> {
                        Row(
                            modifier = Modifier.fillMaxWidth().padding(top = 6.dp),
                            horizontalArrangement = Arrangement.spacedBy(4.dp),
                            verticalAlignment = Alignment.CenterVertically,
                        ) {''',
        '''                if (message.status == MessageStatus.STREAMING) {
                    Text(
                        "Generating…",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.padding(top = 8.dp).semantics { liveRegion = LiveRegionMode.Polite },
                    )
                }
                when {
                    actionsAvailable -> {
                        FlowRow(
                            modifier = Modifier.fillMaxWidth().padding(top = 6.dp),
                            horizontalArrangement = Arrangement.spacedBy(4.dp),
                            verticalArrangement = Arrangement.spacedBy(4.dp),
                        ) {''',
    )
    replace_once(
        chat,
        '''                                clipboard.setText(AnnotatedString(message.content))
                                actionStatus = "Copied"
                            }''',
        '''                                clipboard.setText(AnnotatedString(message.content))
                                actionStatus = "Copied"
                                Toast.makeText(context, "Copied", Toast.LENGTH_SHORT).show()
                            }''',
    )
    print("stream-and-bubble overlay applied")


if __name__ == "__main__":
    main()
