"""Prepare buildless, self-contained static HTML; no Android or framework build."""
from html import escape
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'docs'
ORIGIN = 'https://tixaro.github.io'
LOGO = '<svg class="logo" viewBox="0 0 48 48" aria-hidden="true"><rect x="1" y="1" width="46" height="46" rx="13" fill="#101a24" stroke="#243441"/><path d="M12 31a15 15 0 1 1 24 0" fill="none" stroke="#4cdef3" stroke-width="3" stroke-linecap="round"/><path d="m24 25 8-9" stroke="#e9f1f8" stroke-width="2.5" stroke-linecap="round"/><circle cx="24" cy="25" r="3" fill="#e9f1f8"/></svg>'

def shell(lang, title, description, canonical, content):
    privacy = 'Polityka prywatności' if lang == 'pl' else 'Privacy policy'
    skip = 'Przejdź do treści' if lang == 'pl' else 'Skip to content'
    pl = ' aria-current="page"' if lang == 'pl' else ''
    en = ' aria-current="page"' if lang == 'en' else ''
    pl_path = '/delete-data/' if canonical.endswith('/delete-data/') else '/privacy/'
    en_path = '/en/delete-data/' if canonical.endswith('/delete-data/') else '/en/privacy/'
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} — Bimmer Dashboard</title><meta name="description" content="{escape(description, quote=True)}">
<meta name="theme-color" content="#070d13"><link rel="stylesheet" href="/styles.css"><link rel="canonical" href="{ORIGIN}{canonical}">
<link rel="alternate" hreflang="pl" href="{ORIGIN}{pl_path}"><link rel="alternate" hreflang="en" href="{ORIGIN}{en_path}">
</head><body><a class="skip" href="#main">{skip}</a>
<header class="top"><div class="wrap"><a class="brand" href="/">{LOGO}<span>Bimmer Dashboard<small>KODZIX · ANDROID</small></span></a>
<nav class="language" aria-label="Language"><a href="{pl_path}" lang="pl"{pl}>Polski</a><a href="{en_path}" lang="en"{en}>English</a></nav></div></header>
{content}
<footer><div class="wrap"><div><p>Bimmer Dashboard · Kodzix</p><p>Konrad Koszela</p><p>Android · bimmer.dashboard</p></div><div><a href="/privacy/">Polityka prywatności</a> · <a href="/en/privacy/">Privacy policy</a><br><a href="/delete-data/">Usuwanie danych</a> · <a href="/en/delete-data/">Data deletion</a><br><a class="contact" href="mailto:kodzixdev@gmail.com">kodzixdev@gmail.com</a></div></div></footer>
</body></html>
'''

def main():
    policies = json.loads((ROOT / 'policy.json').read_text(encoding='utf-8'))
    assert set(policies) == {'pl', 'en'}
    assert [s['id'] for s in policies['pl']['sections']] == [s['id'] for s in policies['en']['sections']]
    for lang, policy in policies.items():
        path = '/privacy/' if lang == 'pl' else '/en/privacy/'
        toc_title = 'Spis treści' if lang == 'pl' else 'Contents'
        updated = 'Aktualizacja' if lang == 'pl' else 'Last updated'
        titles = [re.sub(r'^\d+\.\s*', '', s['title']) for s in policy['sections']]
        toc = ''.join(f'<a href="#{escape(s["id"])}">{index}. {escape(titles[index - 1])}</a>' for index, s in enumerate(policy['sections'], 1))
        sections = ''.join(f'<section id="{escape(s["id"])}"><h2>{index}. {escape(titles[index - 1])}</h2>{s["html"]}</section>' for index, s in enumerate(policy['sections'], 1))
        content = f'''<div class="hero"><div class="wrap"><div class="eyebrow">Bimmer Dashboard</div><h1>{escape(policy['title'])}</h1>
<p class="intro">{escape(policy['intro'])}</p><div class="meta"><span>{updated}: {escape(policy['updated'])}</span><span>Konrad Koszela · Kodzix</span><span>bimmer.dashboard</span></div></div></div>
<main id="main" class="wrap layout"><nav class="toc" aria-label="{toc_title}"><strong>{toc_title}</strong>{toc}</nav><article>{sections}</article></main>'''
        destination = DIST / path.strip('/') / 'index.html'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(shell(lang, policy['title'], policy['intro'], path, content), encoding='utf-8')
    deletions = json.loads((ROOT / 'deletion.json').read_text(encoding='utf-8'))
    for lang, page in deletions.items():
        path = '/delete-data/' if lang == 'pl' else '/en/delete-data/'
        toc_title = 'Na tej stronie' if lang == 'pl' else 'On this page'
        toc = ''.join(f'<a href="#{s["id"]}">{escape(s["title"])}</a>' for s in page['sections'])
        sections = ''.join(f'<section id="{s["id"]}"><h2>{escape(s["title"])}</h2>{s["html"]}</section>' for s in page['sections'])
        content = f'''<div class="hero"><div class="wrap"><div class="eyebrow">Bimmer Dashboard · Kodzix</div><h1>{escape(page['title'])}</h1><p class="intro">{escape(page['intro'])}</p><div class="meta"><span>27.10.2026</span><span>Konrad Koszela · Kodzix</span><span>bimmer.dashboard</span></div></div></div><main id="main" class="wrap layout"><nav class="toc" aria-label="{toc_title}"><strong>{toc_title}</strong>{toc}</nav><article>{sections}</article></main>'''
        destination = DIST / path.strip('/') / 'index.html'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(shell(lang, page['title'], page['intro'], path, content), encoding='utf-8')
    home = f'''<main id="main" class="wrap"><div class="home"><div class="eyebrow">Kodzix · Android</div><h1>Bimmer Dashboard.<br>Prywatność i pomoc.</h1>
<p class="intro">Informacje o danych przetwarzanych przez aplikację, reklamach i kontakcie z deweloperem. Polityka prywatności jest dostępna w języku polskim i angielskim.</p>
<div class="links"><a class="linkcard" href="/privacy/"><strong>Polityka prywatności ↗</strong><span>Polska wersja · dane, reklamy i Twoje prawa</span></a><a class="linkcard" href="/en/privacy/" lang="en"><strong>Privacy policy ↗</strong><span>English version · data, advertising and your rights</span></a></div>
<div class="details"><div><strong>Deweloper</strong>Konrad Koszela · Kodzix</div><div><strong>Kontakt</strong><a href="mailto:kodzixdev@gmail.com">kodzixdev@gmail.com</a></div><div><strong>Aplikacja</strong>bimmer.dashboard</div></div></div></main>'''
    DIST.mkdir(exist_ok=True)
    (DIST / 'index.html').write_text(shell('pl', 'Prywatność i pomoc', 'Bimmer Dashboard: polityka prywatności oraz kontakt z deweloperem Kodzix.', '/', home), encoding='utf-8')
    (DIST / 'app-ads.txt').write_text('google.com, pub-1543055927972919, DIRECT, f08c47fec0942fa0\n', encoding='utf-8')
    (DIST / 'robots.txt').write_text('User-agent: *\nAllow: /\n', encoding='utf-8')
    print('Static HTML ready: homepage, Polish/English privacy policies, app-ads.txt, robots.txt.')

if __name__ == '__main__':
    main()
