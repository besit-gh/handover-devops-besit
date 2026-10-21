#!/usr/bin/env python3
"""Generate static HTML pages for the Markdown curriculum."""
from pathlib import Path
import html, json, re, shutil
import markdown

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site"
BASE = "/handover-devops-besit"
folders = sorted(p for p in ROOT.iterdir() if p.is_dir() and re.match(r"^(\d{2}-|90-|91-|92-)", p.name))
lessons = []

def slug(path):
    return re.sub(r"[^a-zA-Z0-9-]+", "-", str(path.relative_to(ROOT).with_suffix("")).replace("/", "--")).strip("-").lower()

def title(source, fallback):
    match = re.search(r"(?m)^#\s+(.+)$", source)
    return match.group(1).strip() if match else fallback.replace("-", " ")

def render(source, current):
    def replace_link(match):
        label, target = match.group(1), match.group(2).strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        file_part, _, anchor = target.partition("#")
        candidate = (current.parent / file_part).resolve() if file_part else current
        try:
            candidate.relative_to(ROOT.resolve())
        except ValueError:
            return match.group(0)
        if candidate.is_dir():
            candidate = candidate / "README.md"
        if candidate.suffix == ".md" and candidate.exists():
            url = BASE + "/learn/" + slug(candidate) + "/"
            return "[" + label + "](" + url + (("#" + re.sub(r"[^a-zA-Z0-9_-]", "-", anchor)) if anchor else "") + ")"
        return match.group(0)
    source = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link, source)
    return markdown.markdown(source, extensions=["tables", "fenced_code", "toc", "sane_lists"])

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    assets = ROOT / "web-lessons" / "assets"
    (OUT / "web-lessons" / "assets").mkdir(parents=True)
    for name in ("course.css", "course.js"):
        shutil.copy2(assets / name, OUT / "web-lessons" / "assets" / name)
    for name in ("linux-permissions", "linux-filesystems"):
        dest = OUT / "web-lessons" / name
        dest.mkdir(parents=True)
        shutil.copy2(ROOT / "web-lessons" / name / "index.html", dest / "index.html")
    for folder in folders:
        for path in sorted(folder.rglob("*.md")):
            source = path.read_text(encoding="utf-8")
            course = folder.name.split("-", 1)[-1].replace("-", " ")
            lessons.append({"path": path, "source": str(path.relative_to(ROOT)), "title": title(source, path.stem), "course": course, "url": BASE + "/learn/" + slug(path) + "/", "text": re.sub(r"\s+", " ", re.sub(r"[#*>\[\]()]", " ", source)).lower(), "raw": source})
    lessons.sort(key=lambda x: x["source"])
    index = [{k: x[k] for k in ("title", "course", "url", "source", "text")} for x in lessons]
    groups = {}
    for item in lessons:
        groups.setdefault(item["course"], []).append(item)
    nav = []
    for course, items in groups.items():
        nav.append('<section class="nav-group"><h2>' + html.escape(course) + '</h2>')
        nav.extend('<a class="nav-link" href="' + x["url"] + '">' + html.escape(x["title"]) + '</a>' for x in items)
        nav.append('</section>')
    nav_html = ''.join(nav)
    index_json = json.dumps(index, ensure_ascii=False).replace("</", "<\\/")
    for i, item in enumerate(lessons):
        content = render(item["raw"], item["path"])
        headings = re.findall(r'<h([2-3]) id="([^"]+)">(.*?)</h[2-3]>', content)
        toc = ''.join('<a class="toc-link level-' + level + '" href="#' + anchor + '">' + re.sub("<.*?>", "", label) + '</a>' for level, anchor, label in headings)
        previous = '<a class="pager-link" href="' + lessons[i-1]["url"] + '">← Предыдущий материал</a>' if i else '<span></span>'
        following = '<a class="pager-link next" href="' + lessons[i+1]["url"] + '">Следующий материал →</a>' if i + 1 < len(lessons) else '<a class="pager-link next" href="' + BASE + '/">К каталогу →</a>'
        page = '''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#080d12"><title>''' + html.escape(item["title"]) + ''' · Handover DevOps</title><link rel="stylesheet" href="''' + BASE + '''/web-lessons/assets/course.css"></head><body>
<header class="topbar"><button id="menuOpen" class="menu-button" aria-controls="courseDrawer" aria-expanded="false">☰ Курсы</button><a class="brand" href="''' + BASE + '''/"><span>HANDOVER</span> / DEVOPS</a><label class="search-wrap">⌕ <input id="courseSearch" type="search" placeholder="Найти урок…" aria-label="Поиск"></label><button id="themeToggle" class="quiet-button" aria-label="Переключить контраст">◐</button></header><div class="reading-progress"><span id="readingProgress"></span></div><div class="scrim" id="drawerScrim"></div><aside id="courseDrawer" class="drawer" aria-label="Каталог" aria-hidden="true"><div class="drawer-head"><strong>Учебный маршрут</strong><button id="menuClose" aria-label="Закрыть меню">×</button></div><div id="searchResults" class="search-results" hidden></div><nav><a class="nav-home" href="''' + BASE + '''/">⌂ Главная курса</a>''' + nav_html + '''</nav></aside>
<div class="page-shell"><main class="article"><div class="breadcrumbs"><a href="''' + BASE + '''/">Курс</a><span>/</span><span>''' + html.escape(item["course"]) + '''</span></div><div class="article-meta"><span class="eyebrow">УЧЕБНЫЙ МАТЕРИАЛ</span><span id="readTime"></span></div><h1>''' + html.escape(item["title"]) + '''</h1><p class="intro">Изучай материал по шагам. Проверяй не только что делать, но и почему это работает.</p><div class="lesson-actions"><button id="completeLesson" class="primary-button">✓ Отметить урок пройденным</button><span id="completionState" aria-live="polite"></span></div><div class="article-content">''' + content + '''</div><section class="self-check"><h2>Проверка понимания</h2><p>Перед переходом дальше объясни основные идеи своими словами.</p><label><input type="checkbox" class="self-check-item"> Могу объяснить основные механизмы без подсказки</label><label><input type="checkbox" class="self-check-item"> Могу разобрать практический пример</label><label><input type="checkbox" class="self-check-item"> Могу проверить результат и диагностировать ошибку</label><p id="selfCheckState" class="muted"></p></section><nav class="lesson-pager">''' + previous + following + '''</nav></main><aside class="right-rail"><div class="rail-card"><strong>В этом материале</strong><nav class="toc">''' + toc + '''</nav></div><div class="rail-card"><strong>Твой прогресс</strong><p><span id="progressCount">0</span> материалов завершено</p><div class="mini-progress"><span id="miniProgress"></span></div><p class="muted small">Сохраняется в этом браузере.</p></div></aside></div><footer class="site-footer"><a href="''' + BASE + '''/">Handover DevOps</a><span>Учись безопасно. Проверяй результат.</span></footer><script>window.COURSE_BASE=''' + json.dumps(BASE) + ''';window.COURSE_CURRENT=''' + json.dumps(item["url"]) + ''';window.COURSE_INDEX=''' + index_json + ''';</script><script src="''' + BASE + '''/web-lessons/assets/course.js" defer></script></body></html>'''
        dest = OUT / "learn" / slug(item["path"]) / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page, encoding="utf-8")
    cards = []
    for course, items in groups.items():
        item = items[0]
        cards.append('<a class="course-card" href="' + item["url"] + '"><span class="course-kicker">' + str(len(items)) + ' материалов</span><h2>' + html.escape(course) + '</h2><p>' + html.escape(item["title"]) + '</p><span class="card-arrow">Открыть курс →</span></a>')
    home = '''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#080d12"><title>Handover DevOps — интерактивный учебник</title><link rel="stylesheet" href="''' + BASE + '''/web-lessons/assets/course.css"></head><body><header class="topbar"><button id="menuOpen" class="menu-button" aria-controls="courseDrawer" aria-expanded="false">☰ Каталог</button><a class="brand" href="''' + BASE + '''/"><span>HANDOVER</span> / DEVOPS</a><label class="search-wrap">⌕ <input id="courseSearch" type="search" placeholder="Найти урок…" aria-label="Поиск"></label><button id="themeToggle" class="quiet-button" aria-label="Переключить контраст">◐</button></header><div class="reading-progress"><span id="readingProgress"></span></div><div class="scrim" id="drawerScrim"></div><aside id="courseDrawer" class="drawer" aria-label="Каталог" aria-hidden="true"><div class="drawer-head"><strong>Учебный маршрут</strong><button id="menuClose" aria-label="Закрыть меню">×</button></div><div id="searchResults" class="search-results" hidden></div><nav><a class="nav-home" href="''' + BASE + '''/">⌂ Главная курса</a>''' + nav_html + '''</nav></aside><main class="home-shell"><section class="home-hero"><span class="eyebrow">ОТ ОСНОВ ДО PRODUCTION</span><h1>Инженерные навыки.<br><span>На практике.</span></h1><p>Единый маршрут DevOps: от Linux и сетей до Kubernetes, наблюдаемости, надёжности и передачи сервиса.</p><div class="home-stats"><div><strong>''' + str(len(groups)) + '''</strong><span>курсов</span></div><div><strong>''' + str(len(lessons)) + '''</strong><span>материалов</span></div><div><strong id="homeCompleted">0</strong><span>пройдено</span></div></div></section><section class="catalog-heading"><div><span class="eyebrow">КАТАЛОГ</span><h2>Выбери направление</h2></div><p>Прогресс хранится в этом браузере.</p></section><section class="course-grid">''' + ''.join(cards) + '''</section><section class="featured-labs"><span class="eyebrow">ИНТЕРАКТИВНЫЕ ЛАБОРАТОРИИ</span><h2>Тренируйся на сценариях</h2><div class="featured-grid"><a class="course-card" href="''' + BASE + '''/web-lessons/linux-permissions/"><h3>Права доступа Linux</h3><p>Права rwx, chmod и диагностика отказа в доступе.</p><span class="card-arrow">Запустить лабораторию →</span></a><a class="course-card" href="''' + BASE + '''/web-lessons/linux-filesystems/"><h3>Файловые системы</h3><p>Монтирование, fstab и диагностика проблем хранения.</p><span class="card-arrow">Запустить лабораторию →</span></a></div></section></main><footer class="site-footer"><span>Handover DevOps · интерактивный учебник</span><span>Учись безопасно. Проверяй результат.</span></footer><script>window.COURSE_BASE=''' + json.dumps(BASE) + ''';window.COURSE_CURRENT=''' + json.dumps(BASE + "/") + ''';window.COURSE_INDEX=''' + index_json + ''';</script><script src="''' + BASE + '''/web-lessons/assets/course.js" defer></script></body></html>'''
    (OUT / "index.html").write_text(home, encoding="utf-8")
    print("Generated", len(lessons), "lesson pages across", len(groups), "course groups.")
if __name__ == "__main__":
    main()
