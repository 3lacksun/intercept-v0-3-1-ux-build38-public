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
        ROOT / "app/src/main/java/com/nexarenew/aiconsole/domain/ChatMessageActionPolicy.kt",
        "        content.isNotBlank() && status in setOf(MessageStatus.COMPLETED, MessageStatus.FAILED, MessageStatus.CANCELLED)",
        "        content.isNotBlank() && status != MessageStatus.PENDING",
    )
    replace_once(
        ROOT / "app/src/main/java/com/nexarenew/aiconsole/domain/StreamIdlePolicy.kt",
        "    const val INTER_BYTE_MS = 45_000L",
        "    const val INTER_BYTE_MS = 180_000L",
    )
    replace_once(
        ROOT / "app/src/main/java/com/nexarenew/aiconsole/domain/StreamCompletionPolicy.kt",
        '    fun continuationInstruction(): String =\n        "Continue exactly from where the previous response stopped. Do not repeat text already emitted. Finish the answer completely."\n}',
        '    fun continuationInstruction(): String =\n        "Continue exactly from where the previous response stopped. Do not repeat text already emitted. Finish the answer completely."\n\n    fun isLengthLimit(finishReason: String?): Boolean {\n        val reason = finishReason?.lowercase().orEmpty()\n        return reason == "length" || reason == "max_tokens" || reason == "max_output_tokens"\n    }\n\n    fun shouldContinue(\n        kind: StreamTerminalKind,\n        finishReason: String? = null,\n        outputTokens: Long? = null,\n        maxTokens: Int = 0,\n    ): Boolean {\n        if (kind == StreamTerminalKind.LENGTH || kind == StreamTerminalKind.INCOMPLETE) return true\n        if (isLengthLimit(finishReason)) return true\n        return outputTokens != null && maxTokens > 0 && outputTokens >= maxTokens.toLong()\n    }\n}',
    )
    test = ROOT / "app/src/test/java/com/nexarenew/aiconsole/domain/PureDomainTest.kt"
    old_idle = "        assertFalse(StreamIdlePolicy.isStalled(44_999, receivedAnyBytes = true))\n        assertTrue(StreamIdlePolicy.isStalled(45_000, receivedAnyBytes = true))"
    if test.exists() and old_idle in test.read_text():
        replace_once(
            test,
            old_idle,
            "        assertFalse(StreamIdlePolicy.isStalled(179_999, receivedAnyBytes = true))\n        assertTrue(StreamIdlePolicy.isStalled(180_000, receivedAnyBytes = true))",
        )
    replace_once(
        ROOT / "app/src/main/java/com/nexarenew/aiconsole/network/ProviderClient.kt",
        "import com.nexarenew.aiconsole.domain.StreamTerminalKind",
        "import com.nexarenew.aiconsole.domain.StreamContinuationPolicy\nimport com.nexarenew.aiconsole.domain.StreamTerminalKind",
    )
    replace_once(
        ROOT / "app/src/main/java/com/nexarenew/aiconsole/network/ProviderClient.kt",
        '                finishReason.equals("length", true) -> StreamTerminalKind.LENGTH',
        "                StreamContinuationPolicy.isLengthLimit(finishReason) -> StreamTerminalKind.LENGTH",
    )
    replace_once(
        ROOT / "app/src/main/java/com/nexarenew/aiconsole/network/ProviderClient.kt",
        '    private fun extractDelta(payload: String): String? = runCatching {\n        val delta = JSONObject(payload)\n            .optJSONArray("choices")\n            ?.optJSONObject(0)\n            ?.optJSONObject("delta") ?: return@runCatching null\n        if (!delta.has("content") || delta.isNull("content")) return@runCatching null\n        delta.optString("content").takeIf { it.isNotEmpty() && it != "null" }\n    }.getOrNull()',
        '    private fun extractDelta(payload: String): String? = runCatching {\n        val choice = JSONObject(payload).optJSONArray("choices")?.optJSONObject(0) ?: return@runCatching null\n        textualContent(choice.optJSONObject("delta"))\n            ?: textualContent(choice.optJSONObject("message"))\n            ?: choice.optString("text").takeIf { it.isNotEmpty() && it != "null" }\n    }.getOrNull()\n\n    private fun textualContent(container: JSONObject?): String? {\n        if (container == null) return null\n        if (!container.has("content") || container.isNull("content")) {\n            return container.optString("text").takeIf { it.isNotEmpty() && it != "null" }\n        }\n        val raw = container.get("content")\n        return when (raw) {\n            is String -> raw.takeIf { it.isNotEmpty() && it != "null" }\n            is JSONArray -> buildString {\n                for (i in 0 until raw.length()) {\n                    val item = raw.opt(i)\n                    when (item) {\n                        is String -> if (item.isNotEmpty()) append(item)\n                        is JSONObject -> {\n                            val text = item.optString("text").ifBlank { item.optString("content") }\n                            if (text.isNotBlank() && text != "null") append(text)\n                        }\n                    }\n                }\n            }.takeIf { it.isNotEmpty() }\n            else -> raw.toString().takeIf { it.isNotEmpty() && it != "null" }\n        }\n    }',
    )
    replace_once(
        ROOT / "app/src/main/java/com/nexarenew/aiconsole/data/AppRepository.kt",
        "                if (result?.terminalKind == StreamTerminalKind.COMPLETE) return",
        "                val shouldContinue = result == null || StreamContinuationPolicy.shouldContinue(\n                    result.terminalKind,\n                    result.finishReason,\n                    attemptUsage?.outputTokens,\n                    request.maxTokens,\n                )\n                if (!shouldContinue) return",
    )
    chat = ROOT / "app/src/main/java/com/nexarenew/aiconsole/ui/screens/ChatScreen.kt"
    replace_once(
        chat,
        "import androidx.compose.foundation.layout.*",
        "import androidx.compose.foundation.layout.ExperimentalLayoutApi\nimport androidx.compose.foundation.layout.*",
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
        '                when {\n                    message.status == MessageStatus.STREAMING -> {\n                        Text(\n                            "Generating… actions available when complete.",\n                            style = MaterialTheme.typography.labelSmall,\n                            color = MaterialTheme.colorScheme.onSurfaceVariant,\n                            modifier = Modifier.padding(top = 8.dp).semantics { liveRegion = LiveRegionMode.Polite },\n                        )\n                    }\n                    actionsAvailable -> {\n                        Row(\n                            modifier = Modifier.fillMaxWidth().padding(top = 6.dp),\n                            horizontalArrangement = Arrangement.spacedBy(4.dp),\n                            verticalAlignment = Alignment.CenterVertically,\n                        ) {',
        '                if (message.status == MessageStatus.STREAMING) {\n                    Text(\n                        "Generating…",\n                        style = MaterialTheme.typography.labelSmall,\n                        color = MaterialTheme.colorScheme.onSurfaceVariant,\n                        modifier = Modifier.padding(top = 8.dp).semantics { liveRegion = LiveRegionMode.Polite },\n                    )\n                }\n                when {\n                    actionsAvailable -> {\n                        FlowRow(\n                            modifier = Modifier.fillMaxWidth().padding(top = 6.dp),\n                            horizontalArrangement = Arrangement.spacedBy(4.dp),\n                            verticalArrangement = Arrangement.spacedBy(4.dp),\n                        ) {',
    )
    replace_once(
        chat,
        '                                clipboard.setText(AnnotatedString(message.content))\n                                actionStatus = "Copied"\n                            }',
        '                                clipboard.setText(AnnotatedString(message.content))\n                                actionStatus = "Copied"\n                                Toast.makeText(context, "Copied", Toast.LENGTH_SHORT).show()\n                            }',
    )
    print("stream-and-bubble overlay applied")


if __name__ == "__main__":
    main()
