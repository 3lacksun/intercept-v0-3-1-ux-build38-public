#!/usr/bin/env python3
"""Make the output-token slider actually draggable and steppable."""
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
        "    var outputTokens by rememberSaveable(chat?.id, chat?.maxTokens, outputCeiling) {\n"
        "        mutableIntStateOf(com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(chat?.maxTokens ?: 4096, outputCeiling))\n"
        "    }\n",
        "    var outputTokens by rememberSaveable(chat?.id) {\n"
        "        mutableIntStateOf(com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(chat?.maxTokens ?: 4096, outputCeiling))\n"
        "    }\n"
        "    var slidingTokens by remember { mutableStateOf(false) }\n"
        "    val sliderScrollLock = remember {\n"
        "        object : NestedScrollConnection {\n"
        "            override fun onPreScroll(available: Offset, source: NestedScrollSource): Offset {\n"
        "                return if (slidingTokens) available else Offset.Zero\n"
        "            }\n"
        "        }\n"
        "    }\n"
        "    fun applyOutputTokens(raw: Int, persist: Boolean) {\n"
        "        val saved = com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(raw, outputCeiling)\n"
        "        outputTokens = saved\n"
        "        if (persist && chat != null) vm.updateChatControls(temperatureText.toDoubleOrNull() ?: 0.7, saved)\n"
        "    }\n"
        "    LaunchedEffect(chat?.id, chat?.maxTokens, outputCeiling) {\n"
        "        if (!slidingTokens) {\n"
        "            outputTokens = com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(chat?.maxTokens ?: outputTokens, outputCeiling)\n"
        "        }\n"
        "    }\n",
    )
    must_replace(
        SETTINGS,
        "                            if (outputCeiling > com.nexarenew.aiconsole.domain.OutputTokenPolicy.MIN_TOKENS) {\n"
        "                                Slider(\n"
        "                                    value = outputTokens.toFloat().coerceIn(com.nexarenew.aiconsole.domain.OutputTokenPolicy.MIN_TOKENS.toFloat(), outputCeiling.toFloat()),\n"
        "                                    onValueChange = { raw ->\n"
        "                                        outputTokens = com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(raw.toInt(), outputCeiling)\n"
        "                                    },\n"
        "                                    valueRange = com.nexarenew.aiconsole.domain.OutputTokenPolicy.MIN_TOKENS.toFloat()..outputCeiling.toFloat(),\n"
        "                                    steps = 0,\n"
        "                                    enabled = chat != null,\n"
        "                                    modifier = Modifier.fillMaxWidth(),\n"
        "                                )\n"
        "                            } else {\n"
        "                                Text(\"This model's cap is the 256 minimum, so the slider is fixed.\", style = MaterialTheme.typography.bodySmall)\n"
        "                            }\n",
        "                            if (outputCeiling > com.nexarenew.aiconsole.domain.OutputTokenPolicy.MIN_TOKENS) {\n"
        "                                Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {\n"
        "                                    FilledTonalIconButton(\n"
        "                                        onClick = { applyOutputTokens(outputTokens - com.nexarenew.aiconsole.domain.OutputTokenPolicy.STEP_TOKENS, persist = true) },\n"
        "                                        enabled = chat != null && outputTokens > com.nexarenew.aiconsole.domain.OutputTokenPolicy.MIN_TOKENS,\n"
        "                                    ) { Text(\"-\") }\n"
        "                                    Slider(\n"
        "                                        value = outputTokens.toFloat().coerceIn(com.nexarenew.aiconsole.domain.OutputTokenPolicy.MIN_TOKENS.toFloat(), outputCeiling.toFloat()),\n"
        "                                        onValueChange = { raw ->\n"
        "                                            slidingTokens = true\n"
        "                                            applyOutputTokens(raw.toInt(), persist = false)\n"
        "                                        },\n"
        "                                        onValueChangeFinished = {\n"
        "                                            slidingTokens = false\n"
        "                                            applyOutputTokens(outputTokens, persist = true)\n"
        "                                        },\n"
        "                                        valueRange = com.nexarenew.aiconsole.domain.OutputTokenPolicy.MIN_TOKENS.toFloat()..outputCeiling.toFloat(),\n"
        "                                        steps = 0,\n"
        "                                        enabled = chat != null,\n"
        "                                        modifier = Modifier.weight(1f).height(48.dp).nestedScroll(sliderScrollLock),\n"
        "                                    )\n"
        "                                    FilledTonalIconButton(\n"
        "                                        onClick = { applyOutputTokens(outputTokens + com.nexarenew.aiconsole.domain.OutputTokenPolicy.STEP_TOKENS, persist = true) },\n"
        "                                        enabled = chat != null && outputTokens < outputCeiling,\n"
        "                                    ) { Text(\"+\") }\n"
        "                                }\n"
        "                                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {\n"
        "                                    listOf(256, 1024, 4096, 8192, 32768, outputCeiling).distinct().filter { it in com.nexarenew.aiconsole.domain.OutputTokenPolicy.MIN_TOKENS..outputCeiling }.forEach { preset ->\n"
        "                                        FilterChip(\n"
        "                                            selected = outputTokens == preset,\n"
        "                                            onClick = { applyOutputTokens(preset, persist = true) },\n"
        "                                            enabled = chat != null,\n"
        "                                            label = { Text(if (preset == outputCeiling) \"Max\" else preset.toString()) },\n"
        "                                        )\n"
        "                                    }\n"
        "                                }\n"
        "                            } else {\n"
        "                                Text(\"This model's cap is the 256 minimum, so the slider is fixed.\", style = MaterialTheme.typography.bodySmall)\n"
        "                            }\n",
    )
    print("slider-work overlay applied")


if __name__ == "__main__":
    main()
