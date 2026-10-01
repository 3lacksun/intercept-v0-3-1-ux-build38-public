#!/usr/bin/env python3
"""Replace the Compose token Slider with a native SeekBar that blocks parent scroll."""
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
        "import androidx.compose.ui.Modifier\n",
        "import androidx.compose.ui.Modifier\n"
        "import androidx.compose.ui.viewinterop.AndroidView\n"
        "import android.widget.SeekBar\n",
    )
    must_replace(
        SETTINGS,
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
        "                                    )\n",
        "                                    val seekMin = com.nexarenew.aiconsole.domain.OutputTokenPolicy.MIN_TOKENS.toDouble()\n"
        "                                    val seekMax = outputCeiling.toDouble().coerceAtLeast(seekMin)\n"
        "                                    AndroidView(\n"
        "                                        modifier = Modifier.weight(1f).height(48.dp),\n"
        "                                        factory = { ctx ->\n"
        "                                            SeekBar(ctx).apply {\n"
        "                                                max = 1000\n"
        "                                                splitTrack = false\n"
        "                                                setOnTouchListener { view, _ ->\n"
        "                                                    view.parent?.requestDisallowInterceptTouchEvent(true)\n"
        "                                                    false\n"
        "                                                }\n"
        "                                                setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {\n"
        "                                                    override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {\n"
        "                                                        if (!fromUser) return\n"
        "                                                        val ceiling = (tag as? Int) ?: outputCeiling\n"
        "                                                        val maxTok = ceiling.toDouble().coerceAtLeast(seekMin)\n"
        "                                                        val raw = if (maxTok <= seekMin) seekMin.toInt() else (seekMin * Math.pow(maxTok / seekMin, progress / 1000.0)).toInt()\n"
        "                                                        slidingTokens = true\n"
        "                                                        applyOutputTokens(raw, persist = false)\n"
        "                                                    }\n"
        "                                                    override fun onStartTrackingTouch(seekBar: SeekBar?) {\n"
        "                                                        slidingTokens = true\n"
        "                                                        seekBar?.parent?.requestDisallowInterceptTouchEvent(true)\n"
        "                                                    }\n"
        "                                                    override fun onStopTrackingTouch(seekBar: SeekBar?) {\n"
        "                                                        slidingTokens = false\n"
        "                                                        applyOutputTokens(outputTokens, persist = true)\n"
        "                                                    }\n"
        "                                                })\n"
        "                                            }\n"
        "                                        },\n"
        "                                        update = { bar ->\n"
        "                                            bar.isEnabled = chat != null\n"
        "                                            bar.tag = outputCeiling\n"
        "                                            val current = outputTokens.coerceIn(com.nexarenew.aiconsole.domain.OutputTokenPolicy.MIN_TOKENS, outputCeiling).toDouble()\n"
        "                                            val ratio = if (seekMax <= seekMin) 0.0 else kotlin.math.ln(current / seekMin) / kotlin.math.ln(seekMax / seekMin)\n"
        "                                            val pos = (ratio * 1000.0).toInt().coerceIn(0, 1000)\n"
        "                                            if (!slidingTokens && bar.progress != pos) bar.progress = pos\n"
        "                                        },\n"
        "                                    )\n",
    )
    print("slider-native overlay applied")


if __name__ == "__main__":
    main()
