"""Run with python3 tests/check_pdf.py; optionally pass --browser /path/to/chromium."""
import argparse
import html
from pathlib import Path
import subprocess
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    result = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


def pages(pdf):
    document = ET.fromstring(run('pdftotext', '-bbox', str(pdf), '-'))
    return [
        (float(page.attrib['width']), float(page.attrib['height']),
         [word for word in page.iter() if word.tag.endswith('}word')])
        for page in document.iter() if page.tag.endswith('}page')
    ]


def check_pdf(pdf):
    result = pages(pdf)
    assert result and any(words for _, _, words in result), 'Empty PDF'
    for width, height, words in result:
        assert abs(width - 595.28) < 1 and abs(height - 841.89) < 1, 'Not A4'
        for word in words:
            assert 0 <= float(word.attrib['xMin']) <= float(word.attrib['xMax']) <= width + 1
            assert 0 <= float(word.attrib['yMin']) < float(word.attrib['yMax']) <= height + 1
    fonts = run('pdffonts', str(pdf))
    assert 'ScheherazadeNew-Regular' in fonts, 'Missing Scheherazade New'
    for font in fonts.splitlines()[2:]:
        assert font.split()[-5] == 'yes', f'Unembedded font: {font}'
    return [' '.join(word.text or '' for word in words) for _, _, words in result]


def export(folder, name, markdown):
    source = folder / f'{name}.md'
    source.write_text(markdown)
    pdf = source.with_suffix('.pdf')
    run(str(ROOT / 'pandoc/export-israa-pdf.sh'), str(source), str(pdf))
    return check_pdf(pdf)


def check_pandoc(folder):
    text = export(folder, 'headings', '''# Alpha {.no-page-break}

نَصٌّ عَرَبِيٌّ لاختبار الحركات. FIRSTBODY[^note]

## Beta {.no-page-break}

فقرة مع رابط إلى [Typora](https://typora.io) وكود `pandoc --pdf-engine=xelatex`. SECONDBODY

# Gamma

THIRDBODY

# Delta {.nopagebreak}

FOURTHBODY

[^note]: حاشية عربية لاختبار الخط. FOOTNOTECHECK
''')
    assert len(text) == 2, f'Unexpected heading pagination: {len(text)} pages'
    assert 'FIRSTBODY' in text[0] and 'SECONDBODY' in text[0]
    assert 'THIRDBODY' in text[1] and 'FOURTHBODY' in text[1]
    assert 'FOOTNOTECHECK' in text[0], 'Missing footnote'

    url = 'https://example.org/' + '/'.join(f'chapter-{i:03}' for i in range(20)) + '?a=1&b=20%25'
    export(folder, 'url', '<' + url + '>')
    for width, _, words in pages(folder / 'url.pdf'):
        for word in words:
            assert float(word.attrib['xMin']) >= 56 and float(word.attrib['xMax']) <= width - 56, 'URL outside margins'

    rows = '\n'.join(f'| ROW{i:03} | **قيمة** VALUE{i:03} & 50% |' for i in range(90))
    table = export(folder, 'table', '| COLUMNHEAD | الوصف |\n| --- | --- |\n' + rows)
    assert len(table) > 1, 'Table did not span pages'
    assert all('COLUMNHEAD' in page for page in table), 'Missing repeated table header'
    for i in range(90):
        assert sum(page.count(f'ROW{i:03}') for page in table) == 1, f'Lost/duplicated row {i}'
        assert sum(page.count(f'VALUE{i:03}') for page in table) == 1, f'Lost Latin cell {i}'

    for language in ('text', 'python'):
        code = export(folder, 'code-' + language, '```' + language + '\n' + '\n'.join(f'CODE{i:03}' for i in range(100)) + '\n```')
        assert len(code) > 1, 'Code block did not span pages'
        for i in range(100):
            assert sum(page.count(f'CODE{i:03}') for page in code) == 1, f'Lost code line {i}'

    long_line = 'a' * 120
    for language in ('text', 'python'):
        export(folder, 'long-line-' + language, '```' + language + '\n' + long_line + '\n```')
        for width, _, words in pages(folder / f'long-line-{language}.pdf'):
            for word in words:
                assert float(word.attrib['xMin']) >= 56 and float(word.attrib['xMax']) <= width - 56, 'Code outside margins'

    notes = export(folder, 'table-note', '| مفتاح | قيمة |\n| --- | --- |\n| A | نص[^n] |\n\n[^n]: حاشية TABLEFOOTNOTE\n')
    assert any('TABLEFOOTNOTE' in page for page in notes), 'Lost table footnote'
    export(folder, 'table-image', '| مفتاح | صورة |\n| --- | --- |\n| A | ![صورة](' + str(folder / 'headings.pdf') + ') |\n')

    quote = export(folder, 'quote', '\n>\n'.join(
        f'> فقرة مقتبسة طويلة لاختبار الانتقال بين الصفحات. QUOTE{i:03}' for i in range(40)
    ))
    assert len(quote) > 1, 'Quotation did not span pages'
    for i in range(40):
        assert sum(page.count(f'QUOTE{i:03}') for page in quote) == 1, f'Lost quote {i}'
    print('PASS: Pandoc A4, Scheherazade New, footnotes/URLs, heading breaks, repeated table headers, long code/quotes')


BROWSER_CHECK = '''
function checkPrint() {
  const failures = [];
  const style = selector => getComputedStyle(document.querySelector(selector));
  const check = (ok, name) => { if (!ok) failures.push(name); };
  check(style('#write').padding === '0px' && style('body').padding === '0px', 'padding');
  check(Math.abs(parseFloat(style('#write').fontSize) - 17 * 96 / 72) < .1, 'body-size');
  check(style('#write').fontFamily.startsWith('"Scheherazade New"'), 'body-font');
  check(style('h1').fontFamily === style('#write').fontFamily && style('h1').fontSynthesis === 'none', 'heading-font');
  check(style('#quote').backgroundColor === 'rgb(247, 247, 247)', 'quote-differentiation');
  const quote_marker = getComputedStyle(document.querySelector('#quote-numbered li'), '::before');
  check(quote_marker.direction === 'rtl' && quote_marker.unicodeBidi === 'isolate'
    && quote_marker.textAlign === 'right', 'quote-number-order');
  check(parseFloat(style('#numbered').paddingRight) >= 3 * parseFloat(style('#write').fontSize) - 1, 'number-gutter');
  for (const selector of ['#intro', '#list p', '#quote p', '#center', '.standalone-url']) {
    check(style(selector).textIndent === '0px', 'indent-' + selector);
  }
  check(parseFloat(style('#prose').textIndent) > 0, 'prose-indent');
  check(style('#inline a').display === 'inline' && style('#inline').direction === 'rtl', 'inline-link');
  check(style('.standalone-url').direction === 'ltr', 'standalone-url');
  check(style('#first').breakBefore === 'auto', 'first-heading');
  check(style('h2').breakBefore === 'auto', 'h2-flow');
  check(style('#chapter').breakBefore === 'page', 'chapter-break');
  check(style('#exception').breakBefore === 'auto', 'chapter-exception');
  check(style('h3').breakAfter === 'avoid-page', 'keep-heading');
  check(style('thead').display === 'table-header-group', 'table-header');
  check(getComputedStyle(document.querySelector('#list li'), '::marker').color === style('#write').color, 'marker-contrast');
  check(parseFloat(style('.footnote-line').fontSize) === 16, 'footnote-size');
  check(style('pre').breakInside === 'auto', 'code-split');
  check(style('img').boxShadow === 'none' && style('img').borderRadius === '0px', 'image');
  check(style('strong').color === style('#write').color, 'bold-contrast');
  check(document.fonts.check('12px "IBM Plex Sans Arabic"'), 'latin-font');
  document.querySelector('#result').textContent = failures.length ? 'CHECKFAIL ' + failures.join(', ') : 'CHECKPASS';
}
window.matchMedia('print').addEventListener('change', event => { if (event.matches) checkPrint(); });
'''


def check_browser(folder, browser, base_css):
    # Only this test document owns @page; production CSS leaves margins to Typora.
    content = '''<div id="write"><div id="result">CHECKWAIT</div>
    <h1 id="first">القسم الأول</h1><p id="intro">نَصٌّ عَرَبِيٌّ مع الحركات.</p>
    <p id="prose">فقرة ثانية مع <strong>نص غامق</strong>.</p>
    <p id="inline">نص قبل <a href="https://typora.io">Typora</a> ونص بعد الرابط.</p>
    <p class="standalone-url"><a href="https://typora.io">https://typora.io/documentation/export/very-long-address-with-many-segments/one/two/three/four/five/six/seven/eight/nine/ten</a></p>
    <h2>عنوان فرعي</h2><h3>عنوان المستوى الثالث</h3>
    <ul id="list"><li><p>عنصر قائمة</p><ul><li>عنصر متداخل</li></ul></li></ul>
    <ol id="numbered" start="55"><li>المسؤولية والعجز</li><li>تعدد أبواب العلاج</li><li>مراجعة وتطبيق</li></ol>
    <blockquote id="quote"><p>اقتباس مع <a href="https://typora.io">رابط</a>.</p>
    <ol id="quote-numbered" start="12"><li>عنصر مقتبس</li><li>عنصر آخر</li></ol></blockquote>
    <p id="center" style="text-align:center">نص في الوسط</p>
    <table><thead><tr><th>COLUMNHEAD</th><th>الوصف</th></tr></thead><tbody>
    ''' + ''.join(f'<tr><td>ROW{i:03}</td><td>اختبار الجدول</td></tr>' for i in range(60)) + '''
    </tbody></table><pre class="md-fences">''' + '\n'.join(f'CODE{i:03}' for i in range(100)) + '''</pre>
    <h1 id="chapter">القسم الثاني</h1><p>فقرة بعد فاصل الصفحة.</p>
    <h1 id="exception" class="no-page-break">عنوان بدون فاصل</h1><p>فقرة أخيرة.</p>
    <div class="footnotes"><p class="footnote-line">حاشية للاختبار.</p></div>
    <img alt="اختبار صورة" width="1600" height="3000"
      src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='1600' height='3000'%3E%3Crect width='1600' height='3000' fill='%23ddd'/%3E%3C/svg%3E">
    </div>'''
    for theme in ('light', 'dark'):
        links = ([base_css] if base_css else []) + [ROOT / f'israa-rtl-{theme}.css']
        document = '<!doctype html><html lang="ar"><meta charset="utf-8">'
        document += ''.join(f'<link rel="stylesheet" href="{html.escape(path.as_uri())}">' for path in links)
        document += '<style>@page { size:A4; margin:18mm 20mm 20mm; }</style>'
        document += '<body class="typora-export is-mac">' + content + '<script>' + BROWSER_CHECK + '</script></body></html>'
        source = folder / f'browser-{theme}.html'
        source.write_text(document)
        pdf = source.with_suffix('.pdf')
        run(browser, '--headless', '--no-pdf-header-footer', '--allow-file-access-from-files',
            f'--user-data-dir={folder / "browser-profile"}', '--virtual-time-budget=5000',
            f'--print-to-pdf={pdf}', source.as_uri())
        text = check_pdf(pdf)
        assert 'CHECKPASS' in text[0] and not any('CHECKFAIL' in page for page in text), text[0]
        for i in range(60):
            assert sum(page.count(f'ROW{i:03}') for page in text) == 1, f'Lost browser row {i}'
        for page in text:
            if 'ROW' in page:
                assert 'COLUMNHEAD' in page, 'Missing browser table header'
        for i in range(100):
            assert sum(page.count(f'CODE{i:03}') for page in text) == 1, f'Lost browser code {i}'
        print(f'PASS: {theme} browser print styles, links, indentation, fonts, tables/code ({len(text)} pages)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--browser', help='Chromium-compatible browser executable')
    parser.add_argument('--base-css', type=Path, help='Optional Typora base.css to test the real cascade')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='israa-pdf-') as directory:
        folder = Path(directory)
        check_pandoc(folder)
        if args.browser:
            check_browser(folder, args.browser, args.base_css.resolve() if args.base_css else None)
