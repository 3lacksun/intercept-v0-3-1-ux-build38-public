#!/usr/bin/env python3
"""Replace the free max-token field with a slider capped to each model's published output."""
from pathlib import Path

POLICY = Path("src/app/src/main/java/com/nexarenew/aiconsole/domain/OutputTokenPolicy.kt")
CLIENT = Path("src/app/src/main/java/com/nexarenew/aiconsole/network/ProviderClient.kt")
SETTINGS = Path("src/app/src/main/java/com/nexarenew/aiconsole/ui/screens/SettingsScreen.kt")
VM = Path("src/app/src/main/java/com/nexarenew/aiconsole/ui/AppViewModel.kt")
REPO = Path("src/app/src/main/java/com/nexarenew/aiconsole/data/AppRepository.kt")


def must_replace(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if old not in text:
        raise SystemExit("pattern not found in %s: %r" % (path, old[:200]))
    if text.count(old) != 1:
        raise SystemExit("pattern not unique in %s (%d)" % (path, text.count(old)))
    path.write_text(text.replace(old, new, 1))


def main() -> None:
    must_replace(
        POLICY,
        "    fun normalize(value: Int): Int {\n"
        "        val clamped = value.coerceIn(MIN_TOKENS, MAX_TOKENS)\n"
        "        return ((clamped / STEP_TOKENS) * STEP_TOKENS).coerceAtLeast(MIN_TOKENS)\n"
        "    }\n"
        "}\n",
        "    fun normalize(value: Int): Int = normalize(value, MAX_TOKENS)\n"
        "\n"
        "    fun normalize(value: Int, ceiling: Int): Int {\n"
        "        val limit = ceiling.coerceIn(MIN_TOKENS, MAX_TOKENS)\n"
        "        val clamped = value.coerceIn(MIN_TOKENS, limit)\n"
        "        return ((clamped / STEP_TOKENS) * STEP_TOKENS).coerceAtLeast(MIN_TOKENS).coerceAtMost(limit)\n"
        "    }\n"
        "\n"
        "    /**\n"
        "     * Ceiling for the output slider and for request clamping.\n"
        "     * First value is the stop. Second is true only when the provider published a completion cap.\n"
        "     * Third is true when the stop comes from a known model (published cap or context window).\n"
        "     */\n"
        "    fun outputCeiling(modality: String?, contextLength: Int?): Triple<Int, Boolean, Boolean> {\n"
        "        val published = Regex(\"maxout:(\\\\d+)\").find(modality.orEmpty())?.groupValues?.getOrNull(1)?.toIntOrNull()\n"
        "        if (published != null && published > 0) {\n"
        "            val stop = published.coerceIn(MIN_TOKENS, MAX_TOKENS)\n"
        "            val stepped = (stop / STEP_TOKENS) * STEP_TOKENS\n"
        "            val ceiling = (if (stepped >= MIN_TOKENS) stepped else MIN_TOKENS).coerceAtMost(stop)\n"
        "            return Triple(ceiling, true, true)\n"
        "        }\n"
        "        if (contextLength != null && contextLength > 0) {\n"
        "            val stop = (contextLength - STEP_TOKENS).coerceAtLeast(MIN_TOKENS).coerceAtMost(contextLength).coerceAtMost(MAX_TOKENS)\n"
        "            val stepped = (stop / STEP_TOKENS) * STEP_TOKENS\n"
        "            val ceiling = (if (stepped >= MIN_TOKENS) stepped else MIN_TOKENS).coerceAtMost(contextLength)\n"
        "            return Triple(ceiling, false, true)\n"
        "        }\n"
        "        return Triple(8_192, false, false)\n"
        "    }\n"
        "}\n",
    )
    must_replace(
        CLIENT,
        "        val contextLength = item.optInt(\"context_length\").takeIf { item.has(\"context_length\") && it > 0 }\n"
        "            ?: item.optInt(\"context_window\").takeIf { item.has(\"context_window\") && it > 0 }\n",
        "        val contextLength = item.optInt(\"context_length\").takeIf { item.has(\"context_length\") && it > 0 }\n"
        "            ?: item.optInt(\"context_window\").takeIf { item.has(\"context_window\") && it > 0 }\n"
        "            ?: item.optJSONObject(\"top_provider\")?.optInt(\"context_length\")?.takeIf { item.optJSONObject(\"top_provider\")?.has(\"context_length\") == true && it > 0 }\n"
        "        val publishedMaxOut = publishedMaxOutput(item)\n",
    )
    must_replace(
        CLIENT,
        "            item.optString(\"modality\").trim().takeIf(String::isNotBlank)?.let { \"modality:$it\" },\n",
        "            item.optString(\"modality\").trim().takeIf(String::isNotBlank)?.let { \"modality:$it\" },\n"
        "            publishedMaxOut?.let { \"maxout:$it\" },\n",
    )
    # Insert parser before parseCatalogModel's return is not needed; add helper before parseCatalogModel.
    must_replace(
        CLIENT,
        "    private fun parseCatalogModel(provider: ProviderId, item: JSONObject): ParsedCatalogModel? {\n",
        "    private fun publishedMaxOutput(item: JSONObject): Int? {\n"
        "        val found = ArrayList<Int>()\n"
        "        fun take(obj: JSONObject?, key: String) {\n"
        "            if (obj == null || !obj.has(key) || obj.isNull(key)) return\n"
        "            val value = obj.optInt(key)\n"
        "            if (value > 0) found.add(value)\n"
        "        }\n"
        "        take(item.optJSONObject(\"top_provider\"), \"max_completion_tokens\")\n"
        "        take(item.optJSONObject(\"per_request_limits\"), \"completion_tokens\")\n"
        "        take(item, \"max_completion_tokens\")\n"
        "        take(item, \"max_output_tokens\")\n"
        "        take(item.optJSONObject(\"config\"), \"max_tokens\")\n"
        "        return found.minOrNull()\n"
        "    }\n"
        "\n"
        "    private fun parseCatalogModel(provider: ProviderId, item: JSONObject): ParsedCatalogModel? {\n",
    )
    must_replace(
        SETTINGS,
        "    var maxTokensText by rememberSaveable(chat?.id,chat?.maxTokens){mutableStateOf((chat?.maxTokens ?: 4096).toString())}\n",
        "    val catalogueModel = chat?.let { live -> models[live.provider].orEmpty().firstOrNull { it.id == live.model } }\n"
        "    val outputLimit = com.nexarenew.aiconsole.domain.OutputTokenPolicy.outputCeiling(catalogueModel?.modality, catalogueModel?.contextLength)\n"
        "    val outputCeiling = outputLimit.first\n"
        "    val outputPublished = outputLimit.second\n"
        "    val outputKnown = outputLimit.third\n"
        "    var outputTokens by rememberSaveable(chat?.id, chat?.maxTokens, outputCeiling) {\n"
        "        mutableIntStateOf(com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(chat?.maxTokens ?: 4096, outputCeiling))\n"
        "    }\n",
    )
    must_replace(
        SETTINGS,
        "                            OutlinedTextField(maxTokensText,{maxTokensText=it.filter{ch->ch.isDigit()}},label={Text(\"Maximum output tokens • 256-step • ceiling 1,048,576\")},modifier=Modifier.fillMaxWidth())\n"
        "                            Button(onClick={vm.updateChatControls(temperatureText.toDoubleOrNull()?:0.7,maxTokensText.toIntOrNull()?:4096);temperatureText=(vm.chat.value?.temperature?:0.7).toString();maxTokensText=(vm.chat.value?.maxTokens?:4096).toString()},enabled=chat!=null){Text(\"Save chat controls\")}\n",
        "                            Text(\"Maximum output tokens: $outputTokens\", style = MaterialTheme.typography.titleSmall)\n"
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
        "                            }\n"
        "                            Text(\n"
        "                                if (outputPublished) \"Stops at this model's published max output ($outputCeiling). Step 256. A long prompt still reduces what can be generated.\"\n"
        "                                else if (outputKnown) \"This provider did not publish a max output. Slider stops at the context window minus 256 ($outputCeiling). Refresh models if a published cap appears.\"\n"
        "                                else \"Model cap not loaded. Slider stops at 8,192 until you refresh the catalogue.\",\n"
        "                                style = MaterialTheme.typography.bodySmall,\n"
        "                                color = MaterialTheme.colorScheme.onSurfaceVariant,\n"
        "                            )\n"
        "                            Button(onClick={\n"
        "                                val saved = com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(outputTokens, outputCeiling)\n"
        "                                vm.updateChatControls(temperatureText.toDoubleOrNull()?:0.7, saved)\n"
        "                                temperatureText=(vm.chat.value?.temperature?:0.7).toString()\n"
        "                                outputTokens = vm.chat.value?.maxTokens ?: saved\n"
        "                            },enabled=chat!=null){Text(\"Save chat controls\")}\n",
    )
    must_replace(
        VM,
        "        val updated = current.copy(temperature = temperature.coerceIn(0.0, maxTemperature), maxTokens = com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(maxTokens), updatedAt = System.currentTimeMillis())\n",
        "        val catalogueModel = _models.value[current.provider].orEmpty().firstOrNull { it.id == current.model }\n"
        "        val outputLimit = com.nexarenew.aiconsole.domain.OutputTokenPolicy.outputCeiling(catalogueModel?.modality, catalogueModel?.contextLength)\n"
        "        val ceiling = if (outputLimit.third) outputLimit.first else com.nexarenew.aiconsole.domain.OutputTokenPolicy.MAX_TOKENS\n"
        "        val updated = current.copy(temperature = temperature.coerceIn(0.0, maxTemperature), maxTokens = com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(maxTokens, ceiling), updatedAt = System.currentTimeMillis())\n",
    )
    must_replace(
        REPO,
        "    fun stream(chat: Chat, all: List<Message>, cancellation: CancellationToken, onDelta: (String) -> Unit, onReasoningDelta: (String) -> Unit = {}, onUsage: (ProviderUsage) -> Unit = {}, webSearchEnabled: Boolean = false) =\n"
        "        client.stream(chat.provider, keys.get(\"api.${chat.provider.wire}\"), chat.model, all, chat.temperature, chat.maxTokens, cancellation, onDelta, onReasoningDelta, onUsage, webSearchEnabled)\n",
        "    fun cappedOutputTokens(chat: Chat): Int {\n"
        "        val model = cachedModels(chat.provider).firstOrNull { it.id == chat.model }\n"
        "        val outputLimit = com.nexarenew.aiconsole.domain.OutputTokenPolicy.outputCeiling(model?.modality, model?.contextLength)\n"
        "        val ceiling = if (outputLimit.third) outputLimit.first else com.nexarenew.aiconsole.domain.OutputTokenPolicy.MAX_TOKENS\n"
        "        return com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(chat.maxTokens, ceiling)\n"
        "    }\n"
        "\n"
        "    fun stream(chat: Chat, all: List<Message>, cancellation: CancellationToken, onDelta: (String) -> Unit, onReasoningDelta: (String) -> Unit = {}, onUsage: (ProviderUsage) -> Unit = {}, webSearchEnabled: Boolean = false) =\n"
        "        client.stream(chat.provider, keys.get(\"api.${chat.provider.wire}\"), chat.model, all, chat.temperature, cappedOutputTokens(chat), cancellation, onDelta, onReasoningDelta, onUsage, webSearchEnabled)\n",
    )
    must_replace(
        REPO,
        "            maxTokens = chat.maxTokens,\n",
        "            maxTokens = cappedOutputTokens(chat),\n",
    )
    must_replace(
        REPO,
        "        client.stream(chat.provider, keys.get(\"api.${chat.provider.wire}\"), chat.model, requestMessages, chat.temperature, chat.maxTokens, CancellationToken(), { reply += it }, { reasoning += it }, { providerUsage = it })\n",
        "        client.stream(chat.provider, keys.get(\"api.${chat.provider.wire}\"), chat.model, requestMessages, chat.temperature, cappedOutputTokens(chat), CancellationToken(), { reply += it }, { reasoning += it }, { providerUsage = it })\n",
    )
    must_replace(
        REPO,
        "                        request.maxTokens,\n",
        "                        cappedOutputTokens(com.nexarenew.aiconsole.model.Chat(workspaceId = request.workspaceId, provider = request.provider, model = request.model, maxTokens = request.maxTokens)),\n",
    )
    print("token-slider overlay applied")


if __name__ == "__main__":
    main()
