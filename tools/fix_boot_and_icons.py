#!/usr/bin/env python3
"""Samsung-safe boot + real INTERCEPT mark for 0.3.1-ux."""
from pathlib import Path
import struct
import zlib

ROOT = Path("src/app/src/main")


def png_rgb(width, height, pix):
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    rows = []
    for y in range(height):
        row = bytearray([0])
        for x in range(width):
            row.extend(pix[y * width + x])
        rows.append(bytes(row))
    raw = b"".join(rows)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def intercept_mark(size):
    white = (255, 255, 255)
    black = (11, 11, 11)
    crimson = (185, 2, 18)
    pix = [white] * (size * size)

    def setp(x, y, color):
        if 0 <= x < size and 0 <= y < size:
            pix[y * size + x] = color

    margin = int(size * 0.10)
    x0, y0, x1, y1 = margin, margin, size - margin, size - margin
    radius = max(2, int(size * 0.12))
    for y in range(y0, y1):
        for x in range(x0, x1):
            if x < x0 + radius and y < y0 + radius and (x - (x0 + radius)) ** 2 + (y - (y0 + radius)) ** 2 > radius * radius:
                continue
            if x > x1 - 1 - radius and y < y0 + radius and (x - (x1 - 1 - radius)) ** 2 + (y - (y0 + radius)) ** 2 > radius * radius:
                continue
            if x < x0 + radius and y > y1 - 1 - radius and (x - (x0 + radius)) ** 2 + (y - (y1 - 1 - radius)) ** 2 > radius * radius:
                continue
            if x > x1 - 1 - radius and y > y1 - 1 - radius and (x - (x1 - 1 - radius)) ** 2 + (y - (y1 - 1 - radius)) ** 2 > radius * radius:
                continue
            setp(x, y, black)
    cx = size // 2
    bar = max(2, size // 8)
    top = int(size * 0.28)
    bot = int(size * 0.72)
    cap = max(4, size // 3)
    thick = max(2, size // 12)
    for y in range(top, top + thick):
        for x in range(cx - cap // 2, cx + cap // 2):
            setp(x, y, white)
    for y in range(bot - thick, bot):
        for x in range(cx - cap // 2, cx + cap // 2):
            setp(x, y, white)
    for y in range(top, bot):
        for x in range(cx - bar // 2, cx + bar // 2 + 1):
            setp(x, y, white)
    for y in range(int(size * 0.42), int(size * 0.60)):
        for x in range(cx - bar // 2, cx + bar // 2 + 1):
            setp(x, y, crimson)
    return png_rgb(size, size, pix)


VECTOR = """<?xml version=\"1.0\" encoding=\"utf-8\"?>
<vector xmlns:android=\"http://schemas.android.com/apk/res/android\"
    android:width=\"108dp\"
    android:height=\"108dp\"
    android:viewportWidth=\"108\"
    android:viewportHeight=\"108\">
    <path android:fillColor=\"#0B0B0B\" android:pathData=\"M54,12 L88,26 L83,67 C80,78 69,87 54,96 C39,87 28,78 25,67 L20,26 Z\" />
    <path android:fillColor=\"#FFFFFF\" android:pathData=\"M37,31 H71 V41 H60 V69 H71 V79 H37 V69 H48 V41 H37 Z\" />
    <path android:fillColor=\"#B90212\" android:pathData=\"M48,45 H60 V65 H48 Z\" />
</vector>
"""

ADAPTIVE = """<?xml version=\"1.0\" encoding=\"utf-8\"?>
<adaptive-icon xmlns:android=\"http://schemas.android.com/apk/res/android\">
    <background android:drawable=\"@color/stone_lab_white\" />
    <foreground android:drawable=\"@drawable/ic_launcher_foreground\" />
</adaptive-icon>
"""


def write_icons():
    drawable = ROOT / "res" / "drawable"
    drawable.mkdir(parents=True, exist_ok=True)
    (drawable / "ic_launcher_foreground.xml").write_text(VECTOR)
    (drawable / "ic_intercept_foreground.xml").write_text(VECTOR)
    (drawable / "intercept_launch_background.xml").write_text(
        """<?xml version=\"1.0\" encoding=\"utf-8\"?>
<layer-list xmlns:android=\"http://schemas.android.com/apk/res/android\">
    <item android:drawable=\"@color/stone_lab_white\" />
</layer-list>
"""
    )
    nodpi = ROOT / "res" / "drawable-nodpi"
    nodpi.mkdir(parents=True, exist_ok=True)
    (nodpi / "stone_brand_mark.png").write_bytes(intercept_mark(192))
    for folder, size in (
        ("mipmap-mdpi", 48),
        ("mipmap-hdpi", 72),
        ("mipmap-xhdpi", 96),
        ("mipmap-xxhdpi", 144),
        ("mipmap-xxxhdpi", 192),
    ):
        path = ROOT / "res" / folder
        path.mkdir(parents=True, exist_ok=True)
        mark = intercept_mark(size)
        (path / "ic_launcher.png").write_bytes(mark)
        (path / "ic_launcher_round.png").write_bytes(mark)
    anydpi = ROOT / "res" / "mipmap-anydpi-v26"
    anydpi.mkdir(parents=True, exist_ok=True)
    (anydpi / "ic_launcher.xml").write_text(ADAPTIVE)
    (anydpi / "ic_launcher_round.xml").write_text(ADAPTIVE)


def write_themes():
    values = ROOT / "res" / "values"
    values.mkdir(parents=True, exist_ok=True)
    (values / "themes.xml").write_text(
        """<?xml version=\"1.0\" encoding=\"utf-8\"?>
<resources>
    <style name=\"Theme.Intercept.Base\" parent=\"android:style/Theme.DeviceDefault.Light.NoActionBar\">
        <item name=\"android:windowBackground\">@color/stone_lab_white</item>
        <item name=\"android:statusBarColor\">@color/stone_lab_white</item>
        <item name=\"android:navigationBarColor\">@color/stone_lab_white</item>
        <item name=\"android:windowLightStatusBar\">true</item>
    </style>
    <style name=\"Theme.Intercept\" parent=\"Theme.Intercept.Base\" />
</resources>
"""
    )
    v31 = ROOT / "res" / "values-v31"
    v31.mkdir(parents=True, exist_ok=True)
    (v31 / "themes.xml").write_text(
        """<?xml version=\"1.0\" encoding=\"utf-8\"?>
<resources>
    <style name=\"Theme.Intercept\" parent=\"Theme.Intercept.Base\">
        <item name=\"android:windowSplashScreenBackground\">@color/stone_lab_white</item>
        <item name=\"android:windowSplashScreenIconBackgroundColor\">@color/stone_lab_white</item>
    </style>
</resources>
"""
    )


def patch_main():
    path = ROOT / "java" / "com" / "nexarenew" / "aiconsole" / "MainActivity.kt"
    text = path.read_text()
    text = text.replace(
        "painterResource(R.mipmap.ic_launcher)",
        "painterResource(R.drawable.ic_intercept_foreground)",
    )
    text = text.replace(
        "painterResource(R.drawable.ic_launcher_foreground)",
        "painterResource(R.drawable.ic_intercept_foreground)",
    )
    path.write_text(text)


def patch_app():
    path = ROOT / "java" / "com" / "nexarenew" / "aiconsole" / "KotlinCommandApp.kt"
    text = path.read_text()
    needle = """    fun startBackgroundWork() {\n        if (!isCoreInitialized) return\n        runCatching { PDFBoxResourceLoader.init(this) }\n"""
    insert = """    fun startBackgroundWork() {\n        if (!isCoreInitialized) return\n        runCatching {\n            runCatching { androidx.work.WorkManager.getInstance(this) }.onFailure {\n                androidx.work.WorkManager.initialize(this, workManagerConfiguration)\n            }\n        }\n        runCatching { PDFBoxResourceLoader.init(this) }\n"""
    if "WorkManager.initialize" not in text and needle in text:
        text = text.replace(needle, insert, 1)
        path.write_text(text)


def patch_manifest():
    path = ROOT / "AndroidManifest.xml"
    text = path.read_text()
    if "xmlns:tools=" not in text:
        text = text.replace(
            '<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\">',
            '<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\"\\n    xmlns:tools=\"http://schemas.android.com/tools\">',
            1,
        )
    block = """\n        <provider\n            android:name=\"androidx.startup.InitializationProvider\"\n            android:authorities=\"${applicationId}.androidx-startup\"\n            android:exported=\"false\"\n            tools:node=\"merge\">\n            <meta-data\n                android:name=\"androidx.work.WorkManagerInitializer\"\n                android:value=\"androidx.startup\"\n                tools:node=\"remove\" />\n        </provider>\n"""
    if "WorkManagerInitializer" not in text:
        text = text.replace("</application>", block + "    </application>", 1)
    path.write_text(text)


def main():
    write_icons()
    write_themes()
    patch_main()
    patch_app()
    patch_manifest()
    launch = (ROOT / "res" / "drawable" / "intercept_launch_background.xml").read_text()
    v31 = (ROOT / "res" / "values-v31" / "themes.xml").read_text()
    if "@drawable/ic_launcher_foreground" in launch:
        raise SystemExit("launch background still references vector bitmap")
    if "windowSplashScreenAnimatedIcon" in v31:
        raise SystemExit("v31 splash still sets an animated icon")
    print("boot-safe icon overlay applied")


if __name__ == "__main__":
    main()
