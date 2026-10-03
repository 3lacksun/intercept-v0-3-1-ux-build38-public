#!/usr/bin/env python3
"""Add a manual output-token field next to the app-wide slider."""
from pathlib import Path

SETTINGS = Path("src/app/src/main/java/com/nexarenew/aiconsole/ui/screens/SettingsScreen.kt")


def must_replace(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if old not in text:
        raise SystemExit("pattern not found in %s: %r" % (path, old[:180]))
    if text.count(old) != 1:
        raise SystemExit("pattern not unique in %s (%d)" % (path, text.count(old)))
    path.write_text(text.replace(old, new, 1))


def main() -> None:
    must_replace(
        SETTINGS,
        "import androidx.compose.material3.*\n",
        "import androidx.compose.material3.*\n"
        "import androidx.compose.foundation.text.KeyboardActions\n"
        "import androidx.compose.foundation.text.KeyboardOptions\n"
        "import androidx.compose.ui.text.input.ImeAction\n"
        "import androidx.compose.ui.text.input.KeyboardType\n",
    )
    must_replace(
        SETTINGS,
        "    var outputTokens by rememberSaveable {\n"
        "        mutableIntStateOf(com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(appOutputTokens, outputCeiling))\n"
        "    }\n",
        "    var outputTokens by rememberSaveable {\n"
        "        mutableIntStateOf(com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(appOutputTokens, outputCeiling))\n"
        "    }\n"
        "    var tokenEntry by rememberSaveable { mutableStateOf(outputTokens.toString()) }\n"
        "    var editingTokens by rememberSaveable { mutableStateOf(false) }\n",
    )
    must_replace(
        SETTINGS,
        "                            Text(\"Maximum output tokens for the app: $outputTokens / $outputCeiling\", style = MaterialTheme.typography.titleSmall)\n",
        "                            Text(\"Maximum output tokens for the app: $outputTokens / $outputCeiling\", style = MaterialTheme.typography.titleSmall)\n"
        "                            Text(\"Type a value when the slider is awkward. It is saved for the whole app and clamped to this model's cap.\", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)\n"
        "                            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {\n"
        "                                OutlinedTextField(\n"
        "                                    value = if (editingTokens) tokenEntry else outputTokens.toString(),\n"
        "                                    onValueChange = { raw ->\n"
        "                                        editingTokens = true\n"
        "                                        tokenEntry = raw.filter { it.isDigit() }.take(9)\n"
        "                                    },\n"
        "                                    modifier = Modifier.weight(1f),\n"
        "                                    singleLine = true,\n"
        "                                    label = { Text(\"Output tokens\") },\n"
        "                                    supportingText = { Text(\"Cap $outputCeiling\") },\n"
        "                                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number, imeAction = ImeAction.Done),\n"
        "                                    keyboardActions = KeyboardActions(onDone = {\n"
        "                                        val parsed = tokenEntry.filter { it.isDigit() }.toIntOrNull()\n"
        "                                        val saved = com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(parsed ?: outputTokens, outputCeiling)\n"
        "                                        editingTokens = false\n"
        "                                        slidingTokens = false\n"
        "                                        applyOutputTokens(saved, persist = true)\n"
        "                                        tokenEntry = saved.toString()\n"
        "                                    }),\n"
        "                                )\n"
        "                                Button(\n"
        "                                    onClick = {\n"
        "                                        val parsed = tokenEntry.filter { it.isDigit() }.toIntOrNull()\n"
        "                                        val saved = com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(parsed ?: outputTokens, outputCeiling)\n"
        "                                        editingTokens = false\n"
        "                                        slidingTokens = false\n"
        "                                        applyOutputTokens(saved, persist = true)\n"
        "                                        tokenEntry = saved.toString()\n"
        "                                    },\n"
        "                                    modifier = Modifier.heightIn(min = 48.dp),\n"
        "                                ) { Text(\"Set\") }\n"
        "                            }\n",
    )
    print("token-entry overlay applied")


if __name__ == "__main__":
    main()
