#!/usr/bin/env python3
"""Full visual pass: palette, type, headers, bubbles, and navigation."""
from pathlib import Path

THEME = Path("src/app/src/main/java/com/nexarenew/aiconsole/ui/theme/InterceptTheme.kt")
STONE = Path("src/app/src/main/java/com/nexarenew/aiconsole/ui/components/StoneUi.kt")
MAIN = Path("src/app/src/main/java/com/nexarenew/aiconsole/MainActivity.kt")
CHAT = Path("src/app/src/main/java/com/nexarenew/aiconsole/ui/screens/ChatScreen.kt")


def must_replace(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if old not in text:
        raise SystemExit("pattern not found in %s: %r" % (path, old[:160]))
    if text.count(old) != 1:
        raise SystemExit("pattern not unique in %s (%d)" % (path, text.count(old)))
    path.write_text(text.replace(old, new, 1))


def main() -> None:
    must_replace(
        THEME,
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
        ")\n",
        "private val InterceptDarkColors = darkColorScheme(\n"
        "    primary = Color(0xFFE7C27A),\n"
        "    onPrimary = Color(0xFF221A08),\n"
        "    primaryContainer = Color(0xFF3C2E14),\n"
        "    onPrimaryContainer = Color(0xFFF8E8C4),\n"
        "    secondary = Color(0xFFD5C7B2),\n"
        "    onSecondary = Color(0xFF1C1814),\n"
        "    secondaryContainer = Color(0xFF2C2823),\n"
        "    onSecondaryContainer = Color(0xFFF0E6D6),\n"
        "    tertiary = Color(0xFF9ED48A),\n"
        "    onTertiary = Color(0xFF102008),\n"
        "    tertiaryContainer = Color(0xFF1C3316),\n"
        "    onTertiaryContainer = Color(0xFFD8F3CC),\n"
        "    background = Color(0xFF100E0C),\n"
        "    onBackground = Color(0xFFF3EDE4),\n"
        "    surface = Color(0xFF1A1714),\n"
        "    onSurface = Color(0xFFF3EDE4),\n"
        "    surfaceVariant = Color(0xFF28241F),\n"
        "    onSurfaceVariant = Color(0xFFCDBFAD),\n"
        "    outline = Color(0xFF8E8274),\n"
        "    outlineVariant = Color(0xFF3E372F),\n"
        "    error = Color(0xFFFFB4AB),\n"
        "    onError = Color(0xFF690005),\n"
        "    errorContainer = Color(0xFF93000A),\n"
        "    onErrorContainer = Color(0xFFFFDAD6),\n"
        ")\n",
    )
    must_replace(
        THEME,
        "private val InterceptLightColors = lightColorScheme(\n"
        "    primary = StoneCrimson,\n"
        "    onPrimary = StoneLabWhite,\n"
        "    primaryContainer = Color(0xFFFFE8EB),\n"
        "    onPrimaryContainer = Color(0xFF3B0008),\n"
        "    secondary = StoneGraphite,\n"
        "    onSecondary = StoneLabWhite,\n"
        "    secondaryContainer = Color(0xFFE4E7EC),\n"
        "    onSecondaryContainer = StoneGraphite,\n"
        "    tertiary = StoneAcidGreen,\n"
        "    onTertiary = StoneLabWhite,\n"
        "    tertiaryContainer = Color(0xFFE3F3D6),\n"
        "    onTertiaryContainer = Color(0xFF142C00),\n"
        "    background = StoneCanvas,\n"
        "    onBackground = StoneGraphite,\n"
        "    surface = StoneLabWhite,\n"
        "    onSurface = StoneGraphite,\n"
        "    surfaceVariant = StoneSurfaceGrey,\n"
        "    onSurfaceVariant = Color(0xFF3A4048),\n"
        "    outline = Color(0xFF6B7178),\n"
        "    outlineVariant = StoneSteelGrey,\n"
        "    error = StoneError,\n"
        "    onError = StoneLabWhite,\n"
        "    errorContainer = Color(0xFFFDE7EB),\n"
        "    onErrorContainer = Color(0xFF41000C),\n"
        ")\n",
        "private val InterceptLightColors = lightColorScheme(\n"
        "    primary = Color(0xFF8C1D2C),\n"
        "    onPrimary = Color(0xFFFFF8F4),\n"
        "    primaryContainer = Color(0xFFF8E4D2),\n"
        "    onPrimaryContainer = Color(0xFF3A120C),\n"
        "    secondary = Color(0xFF3E342C),\n"
        "    onSecondary = Color(0xFFFFF8F4),\n"
        "    secondaryContainer = Color(0xFFE7DDD2),\n"
        "    onSecondaryContainer = Color(0xFF241C16),\n"
        "    tertiary = Color(0xFF2F6B32),\n"
        "    onTertiary = Color(0xFFF4FFF2),\n"
        "    tertiaryContainer = Color(0xFFD7EED4),\n"
        "    onTertiaryContainer = Color(0xFF0E2910),\n"
        "    background = Color(0xFFF6F1EA),\n"
        "    onBackground = Color(0xFF1C1714),\n"
        "    surface = Color(0xFFFFFBF7),\n"
        "    onSurface = Color(0xFF1C1714),\n"
        "    surfaceVariant = Color(0xFFEFE6DB),\n"
        "    onSurfaceVariant = Color(0xFF5C534A),\n"
        "    outline = Color(0xFF8A7D72),\n"
        "    outlineVariant = Color(0xFFDDD2C6),\n"
        "    error = Color(0xFFB3261E),\n"
        "    onError = Color(0xFFFFF8F4),\n"
        "    errorContainer = Color(0xFFF9DEDC),\n"
        "    onErrorContainer = Color(0xFF410E0B),\n"
        ")\n",
    )
    must_replace(
        THEME,
        "private val InterceptTypography = Typography(\n"
        "    headlineSmall = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.SemiBold, fontSize = 20.sp, lineHeight = 26.sp),\n"
        "    titleLarge = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.SemiBold, fontSize = 18.sp, lineHeight = 24.sp),\n"
        "    titleMedium = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.SemiBold, fontSize = 16.sp, lineHeight = 22.sp),\n"
        "    titleSmall = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.SemiBold, fontSize = 14.sp, lineHeight = 18.sp),\n"
        "    bodyLarge = TextStyle(fontFamily = FontFamily.SansSerif, fontSize = 16.sp, lineHeight = 24.sp),\n"
        "    bodyMedium = TextStyle(fontFamily = FontFamily.SansSerif, fontSize = 15.sp, lineHeight = 22.sp),\n"
        "    bodySmall = TextStyle(fontFamily = FontFamily.SansSerif, fontSize = 13.sp, lineHeight = 18.sp),\n"
        "    labelLarge = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.SemiBold, fontSize = 14.sp, lineHeight = 18.sp),\n"
        "    labelMedium = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.Medium, fontSize = 12.sp, lineHeight = 16.sp),\n"
        "    labelSmall = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.Medium, fontSize = 11.sp, lineHeight = 14.sp),\n"
        ")\n",
        "private val InterceptTypography = Typography(\n"
        "    headlineSmall = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.SemiBold, fontSize = 22.sp, lineHeight = 28.sp, letterSpacing = (-0.3).sp),\n"
        "    titleLarge = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.SemiBold, fontSize = 18.sp, lineHeight = 24.sp, letterSpacing = (-0.2).sp),\n"
        "    titleMedium = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.SemiBold, fontSize = 16.sp, lineHeight = 22.sp),\n"
        "    titleSmall = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.Medium, fontSize = 14.sp, lineHeight = 18.sp),\n"
        "    bodyLarge = TextStyle(fontFamily = FontFamily.SansSerif, fontSize = 16.sp, lineHeight = 24.sp),\n"
        "    bodyMedium = TextStyle(fontFamily = FontFamily.SansSerif, fontSize = 15.sp, lineHeight = 22.sp),\n"
        "    bodySmall = TextStyle(fontFamily = FontFamily.SansSerif, fontSize = 13.sp, lineHeight = 18.sp),\n"
        "    labelLarge = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.SemiBold, fontSize = 14.sp, lineHeight = 18.sp),\n"
        "    labelMedium = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.Medium, fontSize = 12.sp, lineHeight = 16.sp, letterSpacing = 0.2.sp),\n"
        "    labelSmall = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.Medium, fontSize = 11.sp, lineHeight = 14.sp, letterSpacing = 0.4.sp),\n"
        ")\n",
    )
    must_replace(
        THEME,
        "private val InterceptShapes = Shapes(\n"
        "    extraSmall = RoundedCornerShape(6.dp),\n"
        "    small = RoundedCornerShape(8.dp),\n"
        "    medium = RoundedCornerShape(12.dp),\n"
        "    large = RoundedCornerShape(16.dp),\n"
        "    extraLarge = RoundedCornerShape(20.dp),\n"
        ")\n",
        "private val InterceptShapes = Shapes(\n"
        "    extraSmall = RoundedCornerShape(10.dp),\n"
        "    small = RoundedCornerShape(14.dp),\n"
        "    medium = RoundedCornerShape(18.dp),\n"
        "    large = RoundedCornerShape(24.dp),\n"
        "    extraLarge = RoundedCornerShape(28.dp),\n"
        ")\n",
    )
    must_replace(
        STONE,
        "        Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(1.dp)) {\n"
        "            if (eyebrow.isNotBlank()) {\n"
        "                Text(eyebrow, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.SemiBold)\n"
        "            }\n"
        "            Text(title, style = MaterialTheme.typography.headlineSmall, maxLines = 1, overflow = TextOverflow.Ellipsis)\n",
        "        Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {\n"
        "            if (eyebrow.isNotBlank()) {\n"
        "                Text(eyebrow.uppercase(), style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.SemiBold)\n"
        "            }\n"
        "            Text(title, style = MaterialTheme.typography.headlineSmall, maxLines = 1, overflow = TextOverflow.Ellipsis)\n",
    )
    must_replace(
        MAIN,
        "                    HorizontalDivider(color = StoneCrimson, thickness = 2.dp)\n",
        "                    HorizontalDivider(color = MaterialTheme.colorScheme.primary.copy(alpha = 0.55f), thickness = 1.dp)\n",
    )
    must_replace(
        MAIN,
        "                    colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.surface),\n",
        "                    colors = TopAppBarDefaults.topAppBarColors(\n"
        "                        containerColor = MaterialTheme.colorScheme.background,\n"
        "                        titleContentColor = MaterialTheme.colorScheme.onBackground,\n"
        "                    ),\n",
    )
    must_replace(
        MAIN,
        "                NavigationBar(\n"
        "                    modifier = Modifier.testTag(\"main-bottom-navigation\"),\n"
        "                    containerColor = MaterialTheme.colorScheme.surface,\n"
        "                    tonalElevation = 4.dp,\n"
        "                ) {\n",
        "                NavigationBar(\n"
        "                    modifier = Modifier.testTag(\"main-bottom-navigation\"),\n"
        "                    containerColor = MaterialTheme.colorScheme.surface,\n"
        "                    tonalElevation = 0.dp,\n"
        "                ) {\n",
    )
    must_replace(
        CHAT,
        "            color = if (isUser) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surface,\n"
        "            contentColor = if (isUser) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurface,\n",
        "            color = if (isUser) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant,\n"
        "            contentColor = if (isUser) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurface,\n",
    )
    must_replace(
        CHAT,
        "            shadowElevation = if (isUser) 0.dp else 1.dp,\n"
        "            border = if (isUser) null else BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),\n",
        "            shadowElevation = 0.dp,\n"
        "            border = BorderStroke(1.dp, if (isUser) MaterialTheme.colorScheme.primary.copy(alpha = 0.18f) else MaterialTheme.colorScheme.outlineVariant),\n",
    )
    print("visual-upgrade overlay applied")


if __name__ == "__main__":
    main()
