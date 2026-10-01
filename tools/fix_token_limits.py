#!/usr/bin/env python3
"""Bind the output slider to the selected model's published completion cap."""
from pathlib import Path

SETTINGS = Path("src/app/src/main/java/com/nexarenew/aiconsole/ui/screens/SettingsScreen.kt")
CLIENT = Path("src/app/src/main/java/com/nexarenew/aiconsole/network/ProviderClient.kt")


def must_replace(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if old not in text:
        raise SystemExit("pattern not found in %s: %r" % (path, old[:180]))
    if text.count(old) != 1:
        raise SystemExit("pattern not unique in %s (%d)" % (path, text.count(old)))
    path.write_text(text.replace(old, new, 1))


def main() -> None:
    must_replace(
        CLIENT,
        "            publishedMaxOut?.let { \"maxout:$it\" },\n",
        "            publishedMaxOut?.let { \"maxout:$it\" },\n",
    )
    must_replace(
        SETTINGS,
        "    val catalogueModel = chat?.let { live -> models[live.provider].orEmpty().firstOrNull { it.id == live.model } }\n"
        "    val outputLimit = com.nexarenew.aiconsole.domain.OutputTokenPolicy.outputCeiling(catalogueModel?.modality, catalogueModel?.contextLength)\n"
        "    val outputCeiling = outputLimit.first\n"
        "    val outputPublished = outputLimit.second\n"
        "    val outputKnown = outputLimit.third\n",
        "    val catalogueModel = chat?.let { live ->\n"
        "        val list = models[live.provider].orEmpty()\n"
        "        list.firstOrNull { it.id == live.model }\n"
        "            ?: list.firstOrNull { it.id.equals(live.model, ignoreCase = true) }\n"
        "            ?: list.firstOrNull { it.name.equals(live.model, ignoreCase = true) }\n"
        "    }\n"
        "    val outputLimit = com.nexarenew.aiconsole.domain.OutputTokenPolicy.outputCeiling(catalogueModel?.modality, catalogueModel?.contextLength)\n"
        "    val outputCeiling = outputLimit.first\n"
        "    val outputPublished = outputLimit.second\n"
        "    val outputKnown = outputLimit.third && catalogueModel != null\n"
        "    var refreshedCaps by remember { mutableStateOf(setOf<String>()) }\n"
        "    LaunchedEffect(chat?.provider, chat?.model, catalogueModel?.modality) {\n"
        "        val live = chat ?: return@LaunchedEffect\n"
        "        val missingPublishedCap = catalogueModel?.modality?.contains(\"maxout:\") != true\n"
        "        val key = live.provider.wire\n"
        "        if (missingPublishedCap && vm.hasKey(live.provider) && key !in refreshedCaps) {\n"
        "            refreshedCaps = refreshedCaps + key\n"
        "            vm.refreshModels(live.provider)\n"
        "        }\n"
        "    }\n",
    )
    must_replace(
        SETTINGS,
        "                            Text(\"Maximum output tokens: $outputTokens\", style = MaterialTheme.typography.titleSmall)\n",
        "                            Text(\"Maximum output tokens: $outputTokens / $outputCeiling\", style = MaterialTheme.typography.titleSmall)\n"
        "                            Text(\n"
        "                                catalogueModel?.let { \"Reading ${it.name} (${it.id})\" } ?: \"No catalogue row for ${chat?.model ?: \"this chat\"}. The slider cannot read a model cap until that id is loaded.\",\n"
        "                                style = MaterialTheme.typography.bodySmall,\n"
        "                                color = MaterialTheme.colorScheme.onSurfaceVariant,\n"
        "                            )\n",
    )
    must_replace(
        SETTINGS,
        "                                if (outputPublished) \"Stops at this model's published max output ($outputCeiling). Step 256. A long prompt still reduces what can be generated.\"\n"
        "                                else if (outputKnown) \"This provider did not publish a max output. Slider stops at the context window minus 256 ($outputCeiling). Refresh models if a published cap appears.\"\n"
        "                                else \"Model cap not loaded. Slider stops at 8,192 until you refresh the catalogue.\",\n",
        "                                if (outputPublished) \"Published max output for this model is $outputCeiling. Step 256. A long prompt still reduces what can be generated.\"\n"
        "                                else if (outputKnown) \"This provider did not publish a max output. Slider stops at the context window minus 256 ($outputCeiling).\"\n"
        "                                else \"This chat model is not in the loaded catalogue, so its output cap has not been read. Refresh models, then pick the model again.\",\n",
    )
    print("token-limit overlay applied")


if __name__ == "__main__":
    main()
