#!/usr/bin/env python3
"""Make the output-token limit an app-wide setting, not only the open chat."""
from pathlib import Path

PREFS = Path("src/app/src/main/java/com/nexarenew/aiconsole/settings/AppPreferences.kt")
VM = Path("src/app/src/main/java/com/nexarenew/aiconsole/ui/AppViewModel.kt")
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
        PREFS,
        "    fun preferredModel(provider: ProviderId): Flow<String?> = value(modelKey(provider))\n",
        "    fun preferredModel(provider: ProviderId): Flow<String?> = value(modelKey(provider))\n"
        "    fun appOutputTokens(): Flow<Int> = value(APP_OUTPUT_TOKENS).map { raw -> raw?.toIntOrNull() ?: 4096 }\n"
        "    suspend fun setAppOutputTokens(value: Int) = set(APP_OUTPUT_TOKENS, value.toString())\n",
    )
    must_replace(
        PREFS,
        "        private val PREFERRED_PROVIDER = stringPreferencesKey(\"preferred_provider\")\n",
        "        private val PREFERRED_PROVIDER = stringPreferencesKey(\"preferred_provider\")\n"
        "        private val APP_OUTPUT_TOKENS = stringPreferencesKey(\"app_max_output_tokens\")\n",
    )
    must_replace(
        VM,
        "    )); val preferredModels: StateFlow<Map<ProviderId, String>> = _preferredModels\n",
        "    )); val preferredModels: StateFlow<Map<ProviderId, String>> = _preferredModels\n"
        "    private val _appOutputTokens = MutableStateFlow(4096)\n"
        "    val appOutputTokens: StateFlow<Int> = _appOutputTokens\n",
    )
    must_replace(
        VM,
        "                preferences.preferredProvider.first()?.let { saved -> ProviderId.fromWire(saved) }?.let { _preferredProvider.value = it }\n",
        "                preferences.preferredProvider.first()?.let { saved -> ProviderId.fromWire(saved) }?.let { _preferredProvider.value = it }\n"
        "                _appOutputTokens.value = preferences.appOutputTokens().first()\n",
    )
    must_replace(
        VM,
        "        val c = Chat(workspaceId = _workspace.value.id, provider = provider, model = model)\n",
        "        val c = Chat(workspaceId = _workspace.value.id, provider = provider, model = model, maxTokens = _appOutputTokens.value)\n",
    )
    must_replace(
        VM,
        "    fun updateChatControls(temperature: Double, maxTokens: Int) {\n",
        "    fun setAppOutputTokens(maxTokens: Int) {\n"
        "        val saved = com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(maxTokens)\n"
        "        _appOutputTokens.value = saved\n"
        "        viewModelScope.launch { preferences.setAppOutputTokens(saved) }\n"
        "        val now = System.currentTimeMillis()\n"
        "        repo.listWorkspaces().forEach { workspace ->\n"
        "            repo.listChats(workspace.id).forEach { existing ->\n"
        "                if (existing.maxTokens != saved) repo.upsertChat(existing.copy(maxTokens = saved, updatedAt = now))\n"
        "            }\n"
        "        }\n"
        "        _chat.value = _chat.value?.copy(maxTokens = saved)\n"
        "        _chats.value = repo.listChats(_workspace.value.id)\n"
        "    }\n"
        "    fun updateChatControls(temperature: Double, maxTokens: Int) {\n",
    )
    must_replace(
        SETTINGS,
        "    val catalogueModel = chat?.let { live ->\n"
        "        val list = models[live.provider].orEmpty()\n"
        "        list.firstOrNull { it.id == live.model }\n"
        "            ?: list.firstOrNull { it.id.equals(live.model, ignoreCase = true) }\n"
        "            ?: list.firstOrNull { it.name.equals(live.model, ignoreCase = true) }\n"
        "    }\n",
        "    val appOutputTokens by vm.appOutputTokens.collectAsStateWithLifecycle()\n"
        "    val limitModelId = preferredModels[provider].takeUnless { it.isNullOrBlank() } ?: chat?.takeIf { it.provider == provider }?.model\n"
        "    val catalogueModel = limitModelId?.let { wanted ->\n"
        "        val list = models[provider].orEmpty()\n"
        "        list.firstOrNull { it.id == wanted }\n"
        "            ?: list.firstOrNull { it.id.equals(wanted, ignoreCase = true) }\n"
        "            ?: list.firstOrNull { it.name.equals(wanted, ignoreCase = true) }\n"
        "    }\n",
    )
    must_replace(
        SETTINGS,
        "    var outputTokens by rememberSaveable(chat?.id) {\n"
        "        mutableIntStateOf(com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(chat?.maxTokens ?: 4096, outputCeiling))\n"
        "    }\n",
        "    var outputTokens by rememberSaveable {\n"
        "        mutableIntStateOf(com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(appOutputTokens, outputCeiling))\n"
        "    }\n",
    )
    must_replace(
        SETTINGS,
        "        if (persist && chat != null) vm.updateChatControls(temperatureText.toDoubleOrNull() ?: 0.7, saved)\n",
        "        if (persist) vm.setAppOutputTokens(saved)\n",
    )
    must_replace(
        SETTINGS,
        "    LaunchedEffect(chat?.id, chat?.maxTokens, outputCeiling) {\n"
        "        if (!slidingTokens) {\n"
        "            outputTokens = com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(chat?.maxTokens ?: outputTokens, outputCeiling)\n"
        "        }\n"
        "    }\n",
        "    LaunchedEffect(appOutputTokens, outputCeiling) {\n"
        "        if (!slidingTokens) {\n"
        "            outputTokens = com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(appOutputTokens, outputCeiling)\n"
        "        }\n"
        "    }\n",
    )
    must_replace(
        SETTINGS,
        "                            Text(\"Current chat AI controls\",style=MaterialTheme.typography.titleMedium)\n",
        "                            Text(\"App output limit\",style=MaterialTheme.typography.titleMedium)\n"
        "                            Text(\"This limit is used by every chat, including new ones. Sends still stop at each model's published cap.\", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)\n",
    )
    must_replace(
        SETTINGS,
        "                            Text(\"Maximum output tokens: $outputTokens / $outputCeiling\", style = MaterialTheme.typography.titleSmall)\n",
        "                            Text(\"Maximum output tokens for the app: $outputTokens / $outputCeiling\", style = MaterialTheme.typography.titleSmall)\n",
    )
    must_replace(
        SETTINGS,
        "                                catalogueModel?.let { \"Reading ${it.name} (${it.id})\" } ?: \"No catalogue row for ${chat?.model ?: \"this chat\"}. The slider cannot read a model cap until that id is loaded.\",\n",
        "                                catalogueModel?.let { \"Reading ${it.name} (${it.id}) for the whole app\" } ?: \"No catalogue row for ${limitModelId ?: \"the selected model\"}. Refresh models, then the app limit can use that cap.\",\n",
    )
    must_replace(
        SETTINGS,
        "                                        enabled = chat != null && outputTokens > com.nexarenew.aiconsole.domain.OutputTokenPolicy.MIN_TOKENS,\n",
        "                                        enabled = outputTokens > com.nexarenew.aiconsole.domain.OutputTokenPolicy.MIN_TOKENS,\n",
    )
    must_replace(
        SETTINGS,
        "                                            bar.isEnabled = chat != null\n",
        "                                            bar.isEnabled = true\n",
    )
    must_replace(
        SETTINGS,
        "                                        enabled = chat != null && outputTokens < outputCeiling,\n",
        "                                        enabled = outputTokens < outputCeiling,\n",
    )
    must_replace(
        SETTINGS,
        "                                            enabled = chat != null,\n"
        "                                            label = { Text(if (preset == outputCeiling) \"Max\" else preset.toString()) },\n",
        "                                            enabled = true,\n"
        "                                            label = { Text(if (preset == outputCeiling) \"Max\" else preset.toString()) },\n",
    )
    must_replace(
        SETTINGS,
        "                            Button(onClick={\n"
        "                                val saved = com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(outputTokens, outputCeiling)\n"
        "                                vm.updateChatControls(temperatureText.toDoubleOrNull()?:0.7, saved)\n"
        "                                temperatureText=(vm.chat.value?.temperature?:0.7).toString()\n"
        "                                outputTokens = vm.chat.value?.maxTokens ?: saved\n"
        "                            },enabled=chat!=null){Text(\"Save chat controls\")}\n",
        "                            Button(onClick={\n"
        "                                val saved = com.nexarenew.aiconsole.domain.OutputTokenPolicy.normalize(outputTokens, outputCeiling)\n"
        "                                vm.updateChatControls(temperatureText.toDoubleOrNull()?:0.7, saved)\n"
        "                                vm.setAppOutputTokens(saved)\n"
        "                                temperatureText=(vm.chat.value?.temperature?:0.7).toString()\n"
        "                                outputTokens = saved\n"
        "                            }){Text(\"Save app controls\")}\n",
    )
    print("app-token-limit overlay applied")


if __name__ == "__main__":
    main()
