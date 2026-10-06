# Israa Typora Theme

Israa is an RTL Arabic Typora theme with matching Pandoc/XeLaTeX PDF export settings.

- Body text: Scheherazade New
- Editor headings: PT Bold Heading; exported headings: Scheherazade New Bold
- Inline Latin fallback: IBM Plex Sans Arabic
- Variants: light and dark

## Attribution

This theme is based on the visual style and typography of the [Ithraa Al-Motoon template project](https://ithraa.sa/projects/template) by شركة إثراء المتون.

## Contents

```text
israa-rtl-light.css       Typora light theme
israa-rtl-dark.css        Typora dark theme
israa-rtl/                Theme fonts and font licenses
pandoc/                   PDF export profile for Pandoc/XeLaTeX
```

## Install The Typora Theme

Typora treats each `.css` file in its theme folder as one theme entry. Theme filenames should be lowercase and hyphenated, so these files appear in Typora as `Israa Rtl Light` and `Israa Rtl Dark`.

1. Open Typora preferences and click **Open Theme Folder**. This is the safest cross-platform method because Typora opens the exact folder used by your installation.
2. Copy these items into that folder:

   ```text
   israa-rtl-light.css
   israa-rtl-dark.css
   israa-rtl/
   ```

3. Restart Typora.
4. Select the theme from the **Themes** menu.

Typical theme folder locations:

macOS:

```text
/Users/{username}/Library/Application Support/abnerworks.Typora/themes/
```

Windows:

```text
C:\Users\{username}\AppData\Roaming\Typora\themes\
```

Linux:

```text
~/.config/Typora/themes/
```

If Typora was installed through a sandboxed package manager, the actual location may differ. Use **Open Theme Folder** in Typora preferences in that case.

## Use The Pandoc PDF Export

Requirements:

- Pandoc 3.1 or newer (tested with 3.12)
- XeLaTeX
- TeX packages used by the profile: `fontspec`, `polyglossia`, `bidi`, `fancyhdr`, `etoolbox`, `booktabs`, `array`, `longtable`, `colortbl`, `fvextra`

`fvextra` provides wrapping for long code lines. Install it through your TeX distribution (`tlmgr install fvextra` for TeX Live).

From the repository root:

```bash
./pandoc/export-israa-pdf.sh pandoc/sample.md pandoc/sample.pdf
```

The script changes into `pandoc/` before running Pandoc, so the font path in `israa-header.tex` is relative:

```text
../israa-rtl/
```

## Typora Custom Export

Typora can call Pandoc-based custom export commands from the export preferences. Add a custom export item and use this command pattern, replacing the repo path with your local path:

```bash
/path/to/israa-typora-theme/pandoc/export-israa-pdf.sh "${currentPath}" "${outputPath}"
```

The profile uses:

```text
pandoc/israa-defaults.yaml
pandoc/israa-header.tex
pandoc/heading-page-breaks.lua
pandoc/latin-inline.lua
pandoc/table-widths.lua
```

## Use The Pandoc DOCX Export

The repo also includes a Pandoc reference document for Word/DOCX output:

```text
pandoc/reference.docx
```

It uses Scheherazade New for body text and PT Bold Heading for title and heading styles.

From the repository root:

```bash
./pandoc/export-israa-docx.sh pandoc/sample.md pandoc/sample.docx
```

For Typora custom export:

```bash
/path/to/israa-typora-theme/pandoc/export-israa-docx.sh "${currentPath}" "${outputPath}"
```

## PDF Layout Notes

### Native Typora PDF Export

In **Preferences → Export → PDF**, use:

- Theme: **Israa Rtl Light** (the editor can still use the dark theme).
- Paper: **A4**, portrait.
- Margins: **18 mm top, 20 mm left/right/bottom**. The theme removes document padding so it does not add a second set of margins.
- Disable **Page Break Between Top Headings**; the theme handles chapter breaks.
- Optional footer: `${pageNo} / ${pageCount}`. Leave room in the margins for headers and footers.

The stylesheet cannot configure Typora's export preferences; set these once in Typora itself.

### Shared Print Layout

- Arabic RTL prose: Scheherazade New, **17pt**, line height **1.7**.
- Exported headings: Scheherazade New Bold (the real 700 face, not synthetic extra-bold), **26 / 22 / 19 / 17.5 / 17pt**. H2 uses a restrained blue accent; other headings are near-black.
- Subsequent H1 chapters start on new pages; the first H1 does not, even after front matter or a TOC. H2–H6 flow with the text and stay with the following content.
- Paragraphs use a **1em first-line indent** and modest spacing. Paragraphs after headings, in lists, and in quotations are not indented.
- Code blocks: **10.5pt**; inline code: **11pt**; footnotes: **12pt**; tables: **14pt**.
- Typora quotations retain a subtle gray fill and fine border; Pandoc quotations use an understated leading rule. Ordered lists reserve extra space for multi-digit markers.
- Long tables repeat their headers; long code blocks and quotations may span pages; long code lines wrap. Images lose screen-only shadows and rounded corners; native-export images are capped at 235 mm high.
- Print-specific styling applies to both theme variants, without changing their screen decoration.

### Pandoc PDF Export

The Pandoc profile uses the same A4 margins and type scale. Its running header follows the current H1/H2, and the footer contains the page number.

- Add `{.no-page-break}` or `{.nopagebreak}` to an H1 to suppress its chapter break. H2 no longer needs an exception.
- `table-widths.lua` sets column proportions and header styling while leaving table rendering to Pandoc's native `longtable` writer, preserving footnotes, images, inline formatting, and repeated headers.
- Inline Latin words use `latin-inline.lua`; inline code is isolated as LTR text.
- Pandoc's native image sizing fits images to the available page area.

Example:

```markdown
# عنوان يبقى في الصفحة نفسها {.no-page-break}
```

For native Typora print/export, use the same class on an HTML heading:

```html
<h1 class="no-page-break">عنوان يبقى في الصفحة نفسها</h1>
```

### Standalone URLs

Ordinary links remain inline and use bidi isolation, including links inside quotations. A paragraph containing prose and one link is not mistakenly treated as a standalone URL.

For a dedicated LTR URL paragraph in Typora, opt in explicitly:

```html
<p class="standalone-url"><a href="https://typora.io">https://typora.io</a></p>
```

### Export Checks

With Pandoc, XeLaTeX, and Poppler (`pdfinfo`, `pdftotext`, `pdffonts`) available:

```bash
python3 tests/check_pdf.py
```

To also check both themes in a Chromium-compatible browser:

```bash
python3 tests/check_pdf.py --browser /path/to/chromium --base-css /path/to/Typora/style/base.css
```

`--base-css` is optional; on macOS it is normally `/Applications/Typora.app/Contents/Resources/TypeMark/style/base.css`. Browser checks validate the CSS cascade and paged rendering, not Typora's native macOS PDF exporter.

## Font And License Notes

Theme source files, scripts, and documentation are licensed under the MIT License. See `LICENSE`.

Bundled Google Fonts:

- Scheherazade New: SIL Open Font License
- IBM Plex Sans Arabic: SIL Open Font License

Bundled legacy/private fonts:

- `PT_Bold_Heading.ttf`

## Typora References

- [About Themes](https://support.typora.io/About-Themes/)
- [Write Custom Theme for Typora](https://theme.typora.io/doc/Write-Custom-Theme/)
- [Export](https://support.typora.io/Export/)
- [Install and Use Pandoc](https://support.typora.io/Install-and-Use-Pandoc/)
