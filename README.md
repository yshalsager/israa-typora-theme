# Israa Typora Theme

Israa is an RTL Arabic Typora theme with matching Pandoc/XeLaTeX PDF export settings.

- Body text: Scheherazade New
- Headings: PT Bold Heading
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

- Pandoc 2.0 or newer
- XeLaTeX
- TeX packages used by the profile: `fontspec`, `polyglossia`, `bidi`, `fancyhdr`, `booktabs`, `tabularx`, `longtable`, `colortbl`, `fancyvrb`

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

- A4 page with Arabic RTL text.
- `h1` and `h2` start on new pages, except the first heading.
- Running header follows the current `h1` and `h2`.
- Footer contains the page number.
- Markdown tables are rendered through `table-widths.lua` to avoid Pandoc LaTeX table alignment issues under RTL.
- Inline Latin words are wrapped through `latin-inline.lua` for font fallback.

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
