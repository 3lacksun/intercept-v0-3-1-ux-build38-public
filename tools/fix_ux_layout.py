#!/usr/bin/env python3
from pathlib import Path

CHAT = Path("src/app/src/main/java/com/nexarenew/aiconsole/ui/screens/ChatScreen.kt")


def must_replace(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if old not in text:
        raise SystemExit("pattern not found in %s: %r" % (path, old[:160]))
    path.write_text(text.replace(old, new, 1))


def main() -> None:
    must_replace(
        CHAT,
        "import androidx.compose.foundation.clickable\n",
        "import androidx.compose.foundation.clickable\n"
        "import androidx.compose.ui.draw.clip\n"
        "import androidx.compose.ui.draw.clipToBounds\n",
    )
    must_replace(
        CHAT,
        "        Box(Modifier.weight(1f).fillMaxWidth()) {",
        "        Box(Modifier.weight(1f).fillMaxWidth().clipToBounds()) {",
    )
    must_replace(
        CHAT,
        "                        GeneratedImageArtifactCard(vm, image)",
        "                        Box(Modifier.fillMaxWidth().clip(MaterialTheme.shapes.large)) {\n"
        "                            GeneratedImageArtifactCard(vm, image)\n"
        "                        }",
    )
    must_replace(
        CHAT,
        "        val actionTarget = msgs.firstOrNull { it.id == selectedActionMessageId }\n"
        "            ?: msgs.lastOrNull { it.role.equals(\"assistant\", true) && it.content.isNotBlank() }\n"
        "        if (actionTarget != null && ChatMessageActionPolicy.contentActionsAvailable(actionTarget.status, actionTarget.content)) {",
        "        val actionTarget = msgs.firstOrNull { it.id == selectedActionMessageId }\n"
        "        if (actionTarget != null && ChatMessageActionPolicy.contentActionsAvailable(actionTarget.status, actionTarget.content)) {",
    )
    must_replace(
        CHAT,
        "                    Text(\n"
        "                        \"Tap a bubble, or use these buttons. Full opens a selectable reader.\",\n"
        "                        style = MaterialTheme.typography.labelSmall,\n"
        "                        color = MaterialTheme.colorScheme.onSecondaryContainer.copy(alpha = 0.78f),\n"
        "                    )\n",
        "                    Text(\n"
        "                        \"Selected reply · \" + actionTarget.content.length + \" characters\",\n"
        "                        style = MaterialTheme.typography.labelSmall,\n"
        "                        color = MaterialTheme.colorScheme.onSecondaryContainer.copy(alpha = 0.78f),\n"
        "                    )\n",
    )
    must_replace(
        CHAT,
        "                    Text(\n"
        "                        \"Tap this reply for Speak, Copy, Full\",\n"
        "                        style = MaterialTheme.typography.labelSmall,\n"
        "                        color = MaterialTheme.colorScheme.onSurfaceVariant,\n"
        "                        modifier = Modifier.padding(top = 6.dp),\n"
        "                    )\n",
        "                    TextButton(\n"
        "                        onClick = onSelect,\n"
        "                        modifier = Modifier.fillMaxWidth().heightIn(min = 40.dp).padding(top = 2.dp).testTag(\"bubble-open-actions\"),\n"
        "                    ) { Text(\"Actions\") }\n",
    )
    must_replace(
        CHAT,
        "                    actionsAvailable -> {\n"
        "                        FlowRow(\n",
        "                    false && actionsAvailable -> {\n"
        "                        FlowRow(\n",
    )
    print("ux-layout overlay applied")


if __name__ == "__main__":
    main()
