#!/usr/bin/env python3
from pathlib import Path

THEME = Path("src/app/src/main/java/com/nexarenew/aiconsole/ui/theme/InterceptTheme.kt")
CHAT = Path("src/app/src/main/java/com/nexarenew/aiconsole/ui/screens/ChatScreen.kt")


def must_replace(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if old not in text:
        raise SystemExit("pattern not found in %s: %r" % (path, old[:160]))
    path.write_text(text.replace(old, new, 1))


def main() -> None:
    must_replace(
        THEME,
        "import androidx.compose.material3.lightColorScheme\n"
        "import androidx.compose.runtime.Composable\n"
        "import androidx.compose.ui.graphics.Color\n",
        "import androidx.compose.foundation.isSystemInDarkTheme\n"
        "import androidx.compose.material3.darkColorScheme\n"
        "import androidx.compose.material3.lightColorScheme\n"
        "import androidx.compose.runtime.Composable\n"
        "import androidx.compose.runtime.SideEffect\n"
        "import androidx.compose.ui.graphics.Color\n"
        "import androidx.compose.ui.platform.LocalView\n"
        "import androidx.core.view.WindowCompat\n",
    )
    must_replace(
        THEME,
        "private val InterceptLightColors = lightColorScheme(\n",
        "private val InterceptDarkColors = darkColorScheme(\n"
        "    primary = Color(0xFFE8B86D),\n"
        "    onPrimary = Color(0xFF1A1408),\n"
        "    primaryContainer = Color(0xFF3A2A12),\n"
        "    onPrimaryContainer = Color(0xFFF6E7C8),\n"
        "    secondary = Color(0xFFC5CBD3),\n"
        "    onSecondary = Color(0xFF15181C),\n"
        "    secondaryContainer = Color(0xFF2A3038),\n"
        "    onSecondaryContainer = Color(0xFFE6EAEF),\n"
        "    tertiary = Color(0xFF8FCF5A),\n"
        "    onTertiary = Color(0xFF102000),\n"
        "    tertiaryContainer = Color(0xFF1E330C),\n"
        "    onTertiaryContainer = Color(0xFFD7F0BE),\n"
        "    background = Color(0xFF0E1114),\n"
        "    onBackground = Color(0xFFE8ECF1),\n"
        "    surface = Color(0xFF161A1F),\n"
        "    onSurface = Color(0xFFE8ECF1),\n"
        "    surfaceVariant = Color(0xFF222830),\n"
        "    onSurfaceVariant = Color(0xFFB7BEC7),\n"
        "    outline = Color(0xFF8B929A),\n"
        "    outlineVariant = Color(0xFF3A424C),\n"
        "    error = Color(0xFFFFB4AB),\n"
        "    onError = Color(0xFF690005),\n"
        "    errorContainer = Color(0xFF93000A),\n"
        "    onErrorContainer = Color(0xFFFFDAD6),\n"
        ")\n"
        "\n"
        "private val InterceptLightColors = lightColorScheme(\n",
    )
    must_replace(
        THEME,
        "@Composable\n"
        "fun InterceptTheme(content: @Composable () -> Unit) {\n"
        "    MaterialTheme(\n"
        "        colorScheme = InterceptLightColors,\n"
        "        typography = InterceptTypography,\n"
        "        shapes = InterceptShapes,\n"
        "        content = content,\n"
        "    )\n"
        "}\n",
        "@Composable\n"
        "fun InterceptTheme(content: @Composable () -> Unit) {\n"
        "    val dark = isSystemInDarkTheme()\n"
        "    val view = LocalView.current\n"
        "    if (!view.isInEditMode) {\n"
        "        SideEffect {\n"
        "            val window = (view.context as? android.app.Activity)?.window\n"
        "            if (window != null) {\n"
        "                WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !dark\n"
        "                WindowCompat.getInsetsController(window, view).isAppearanceLightNavigationBars = !dark\n"
        "            }\n"
        "        }\n"
        "    }\n"
        "    MaterialTheme(\n"
        "        colorScheme = if (dark) InterceptDarkColors else InterceptLightColors,\n"
        "        typography = InterceptTypography,\n"
        "        shapes = InterceptShapes,\n"
        "        content = content,\n"
        "    )\n"
        "}\n",
    )

    must_replace(
        CHAT,
        "import androidx.compose.foundation.clickable\n",
        "import androidx.compose.foundation.clickable\n"
        "import androidx.compose.foundation.text.selection.SelectionContainer\n"
        "import androidx.compose.ui.window.Dialog\n"
        "import androidx.compose.ui.window.DialogProperties\n"
        "import com.nexarenew.aiconsole.ui.theme.technicalTextStyle\n",
    )
    must_replace(
        CHAT,
        "                    Text(\n"
        "                        if (actionTarget.role.equals(\"assistant\", true)) \"Reply actions\" else \"Message actions\",\n"
        "                        style = MaterialTheme.typography.labelMedium,\n"
        "                    )\n",
        "                    Text(\n"
        "                        if (actionTarget.role.equals(\"assistant\", true)) \"Reply actions\" else \"Message actions\",\n"
        "                        style = MaterialTheme.typography.labelMedium,\n"
        "                    )\n"
        "                    Text(\n"
        "                        \"Tap a bubble, or use these buttons. Full opens a selectable reader.\",\n"
        "                        style = MaterialTheme.typography.labelSmall,\n"
        "                        color = MaterialTheme.colorScheme.onSecondaryContainer.copy(alpha = 0.78f),\n"
        "                    )\n",
    )
    must_replace(
        CHAT,
        "        stickyFullText?.let { body ->\n"
        "            AlertDialog(\n"
        "                onDismissRequest = { stickyFullText = null },\n"
        "                title = { Text(\"Full reply (${body.length} characters)\") },\n"
        "                text = {\n"
        "                    Column(Modifier.fillMaxWidth().heightIn(max = 420.dp).verticalScroll(rememberScrollState())) {\n"
        "                        Text(body, style = MaterialTheme.typography.bodyMedium)\n"
        "                    }\n"
        "                },\n"
        "                confirmButton = {\n"
        "                    TextButton(onClick = {\n"
        "                        runCatching {\n"
        "                            val mgr = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager\n"
        "                            mgr.setPrimaryClip(android.content.ClipData.newPlainText(\"message\", body))\n"
        "                        }\n"
        "                        Toast.makeText(context, \"Copied ${body.length} characters\", Toast.LENGTH_SHORT).show()\n"
        "                    }) { Text(\"Copy\") }\n"
        "                },\n"
        "                dismissButton = { TextButton(onClick = { stickyFullText = null }) { Text(\"Close\") } },\n"
        "            )\n"
        "        }\n",
        "        stickyFullText?.let { body ->\n"
        "            Dialog(\n"
        "                onDismissRequest = { stickyFullText = null },\n"
        "                properties = DialogProperties(usePlatformDefaultWidth = false),\n"
        "            ) {\n"
        "                Surface(\n"
        "                    modifier = Modifier.fillMaxSize().testTag(\"full-reader\"),\n"
        "                    color = MaterialTheme.colorScheme.background,\n"
        "                ) {\n"
        "                    Column(Modifier.fillMaxSize().padding(horizontal = 14.dp, vertical = 10.dp)) {\n"
        "                        Text(\"Full reply\", style = MaterialTheme.typography.titleMedium)\n"
        "                        Text(\n"
        "                            body.length.toString() + \" characters · select and copy any span\",\n"
        "                            style = MaterialTheme.typography.labelSmall,\n"
        "                            color = MaterialTheme.colorScheme.onSurfaceVariant,\n"
        "                        )\n"
        "                        Row(\n"
        "                            modifier = Modifier.fillMaxWidth().padding(top = 8.dp, bottom = 8.dp),\n"
        "                            horizontalArrangement = Arrangement.spacedBy(8.dp),\n"
        "                        ) {\n"
        "                            Button(\n"
        "                                onClick = {\n"
        "                                    runCatching {\n"
        "                                        val mgr = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager\n"
        "                                        mgr.setPrimaryClip(android.content.ClipData.newPlainText(\"message\", body))\n"
        "                                    }\n"
        "                                    Toast.makeText(context, \"Copied \" + body.length + \" characters\", Toast.LENGTH_SHORT).show()\n"
        "                                },\n"
        "                                modifier = Modifier.weight(1f).heightIn(min = 48.dp).testTag(\"reader-copy\"),\n"
        "                            ) { Text(\"Copy all\") }\n"
        "                            OutlinedButton(\n"
        "                                onClick = { stickyFullText = null },\n"
        "                                modifier = Modifier.weight(1f).heightIn(min = 48.dp).testTag(\"reader-close\"),\n"
        "                            ) { Text(\"Close\") }\n"
        "                        }\n"
        "                        Surface(\n"
        "                            modifier = Modifier.fillMaxSize(),\n"
        "                            color = MaterialTheme.colorScheme.surface,\n"
        "                            shape = RoundedCornerShape(16.dp),\n"
        "                            border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),\n"
        "                        ) {\n"
        "                            SelectionContainer {\n"
        "                                Text(\n"
        "                                    body,\n"
        "                                    style = technicalTextStyle(MaterialTheme.typography.bodyMedium),\n"
        "                                    modifier = Modifier.fillMaxWidth().padding(12.dp).verticalScroll(rememberScrollState()),\n"
        "                                )\n"
        "                            }\n"
        "                        }\n"
        "                    }\n"
        "                }\n"
        "            }\n"
        "        }\n",
    )
    must_replace(
        CHAT,
        "                        color = if (isUser) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.primary,\n"
        "                        modifier = Modifier.weight(1f),\n"
        "                    )\n",
        "                        color = if (isUser) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.primary,\n"
        "                        modifier = Modifier.weight(1f),\n"
        "                    )\n"
        "                    if (message.content.isNotBlank()) {\n"
        "                        Text(\n"
        "                            message.content.length.toString() + \" ch\",\n"
        "                            style = MaterialTheme.typography.labelSmall,\n"
        "                            color = MaterialTheme.colorScheme.onSurfaceVariant,\n"
        "                        )\n"
        "                    }\n",
    )
    must_replace(
        CHAT,
        "                            is MessageSegment.Text -> if (segment.value.isNotBlank()) Text(segment.value, style = MaterialTheme.typography.bodyLarge)\n",
        "                            is MessageSegment.Text -> if (segment.value.isNotBlank()) Text(\n"
        "                                segment.value,\n"
        "                                style = if (isAssistant) technicalTextStyle(MaterialTheme.typography.bodyMedium) else MaterialTheme.typography.bodyLarge,\n"
        "                            )\n",
    )
    must_replace(
        CHAT,
        "                if (message.status == MessageStatus.STREAMING) {\n"
        "                    Text(\n"
        "                        \"Generating…\",\n"
        "                        style = MaterialTheme.typography.labelSmall,\n"
        "                        color = MaterialTheme.colorScheme.onSurfaceVariant,\n"
        "                        modifier = Modifier.padding(top = 8.dp).semantics { liveRegion = LiveRegionMode.Polite },\n"
        "                    )\n"
        "                }\n",
        "                if (message.status == MessageStatus.STREAMING) {\n"
        "                    Text(\n"
        "                        \"Generating · \" + message.content.length + \" characters\",\n"
        "                        style = MaterialTheme.typography.labelSmall,\n"
        "                        color = MaterialTheme.colorScheme.tertiary,\n"
        "                        modifier = Modifier.padding(top = 8.dp).semantics { liveRegion = LiveRegionMode.Polite },\n"
        "                    )\n"
        "                } else if (isAssistant && message.content.isNotBlank()) {\n"
        "                    Text(\n"
        "                        \"Tap this reply for Speak, Copy, Full\",\n"
        "                        style = MaterialTheme.typography.labelSmall,\n"
        "                        color = MaterialTheme.colorScheme.onSurfaceVariant,\n"
        "                        modifier = Modifier.padding(top = 6.dp),\n"
        "                    )\n"
        "                }\n",
    )
    print("ux-upgrade overlay applied")


if __name__ == "__main__":
    main()
