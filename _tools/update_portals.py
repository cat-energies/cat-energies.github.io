from pathlib import Path
import json

portals = [
    {'name':'EDF SA','scope':'EDF SA','level':'Entreprise','url':'/edf/','communications':'/edf/communications.json'},
    {'name':'Cattenom','scope':'Cattenom','level':'Site','parent':'DPN','url':'/edf/dpn/cattenom/','communications':'/edf/dpn/cattenom/communications.json'}
]
Path('portails.json').write_text(json.dumps(portals, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

cat_json=Path('edf/dpn/cattenom/communications.json')
cat_data=json.loads(cat_json.read_text(encoding='utf-8'))
cat_data=[x for x in cat_data if x.get('scope') in (None,'','Cattenom')]
for x in cat_data: x['scope']='Cattenom'
cat_json.write_text(json.dumps(cat_data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

edf_json=Path('edf/communications.json')
edf_data=json.loads(edf_json.read_text(encoding='utf-8'))
for x in edf_data: x['scope']='EDF SA'
edf_json.write_text(json.dumps(edf_data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

nav_html='''\n  <section class="scope-switcher" aria-label="Changer de périmètre">\n    <div><strong>Changer de périmètre</strong><span>Accédez aux autres portails CAT Énergies sans dupliquer les contenus.</span></div>\n    <select id="scopeSelect" aria-label="Choisir un périmètre"><option value="">Choisir un portail…</option></select>\n  </section>\n'''
nav_css='''\n  .scope-switcher{margin:0 0 24px;background:#fff;border:1px solid var(--line);border-radius:18px;box-shadow:0 6px 18px rgba(31,72,94,.06);padding:16px 18px;display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap}\n  .scope-switcher strong{display:block;color:var(--primary-dark);margin-bottom:4px}\n  .scope-switcher span{font-size:13px;color:var(--muted)}\n  .scope-switcher select{width:auto;min-width:220px}\n  .scope-badge{display:inline-flex;align-items:center;padding:4px 8px;border-radius:999px;background:#eef1f3;color:#596874;font-size:11px;font-weight:800}\n  @media(max-width:620px){.scope-switcher select{width:100%}}\n'''
new_load='''async function loadCommunications(){\n  try{\n    const response = await fetch("communications.json", { cache: "no-store" });\n    if(!response.ok) throw new Error("HTTP " + response.status);\n    communications = await response.json();\n    const registryResponse = await fetch("/portails.json", { cache: "no-store" });\n    const registry = registryResponse.ok ? await registryResponse.json() : [];\n    const scopeSelect = document.getElementById("scopeSelect");\n    if(scopeSelect){\n      registry.forEach(portal => {\n        const option = document.createElement("option");\n        option.value = portal.url;\n        option.textContent = portal.parent ? (portal.parent + " · " + portal.name) : portal.name;\n        scopeSelect.appendChild(option);\n      });\n      scopeSelect.addEventListener("change", () => { if(scopeSelect.value) window.location.href = scopeSelect.value; });\n    }\n    const globalLoaded = [];\n    for(const portal of registry){\n      try{\n        const r = await fetch(portal.communications, { cache: "no-store" });\n        if(!r.ok) continue;\n        const items = await r.json();\n        items.forEach(item => globalLoaded.push({ ...item, scope: item.scope || portal.scope }));\n      }catch(error){ console.info("Portail non indexé", portal.name, error); }\n    }\n    const seen = new Set();\n    globalCommunications = globalLoaded.filter(item => {\n      const key = item.url || ((item.scope || "") + "|" + (item.title || ""));\n      if(seen.has(key)) return false;\n      seen.add(key);\n      return true;\n    });\n    communications.forEach(item => { item._searchText = normalizeSearchText((item.title||"")+" "+(item.description||"")+" "+(item.category||"")+" "+(item.scope||"")); });\n    globalCommunications.forEach(item => { item._searchText = normalizeSearchText((item.title||"")+" "+(item.description||"")+" "+(item.category||"")+" "+(item.scope||"")); });\n    totalCount.textContent = communications.length + " communication" + (communications.length > 1 ? "s" : "");\n    renderCategories();\n    renderLatest();\n    indexPageContents();\n  }catch(error){\n    console.error(error);\n    latestGrid.innerHTML = '<div class="empty error">Impossible de charger communications.json.</div>';\n    if(searchIndexStatus) searchIndexStatus.textContent = "Erreur de chargement";\n  }\n}\n'''

for portal_path in [Path('edf/index.html'),Path('edf/dpn/cattenom/index.html')]:
    s=portal_path.read_text(encoding='utf-8')
    if '.scope-switcher{' not in s: s=s.replace('</style>',nav_css+'\n</style>',1)
    if 'id="scopeSelect"' not in s: s=s.replace('<main class="container">','<main class="container">'+nav_html,1)
    if 'let globalCommunications = [];' not in s: s=s.replace('let communications = [];\n','let communications = [];\nlet globalCommunications = [];\n',1)
    old='''async function indexPageContents(){\n  if(searchIndexStatus) searchIndexStatus.textContent = "Indexation du contenu des pages…";\n  const results = await Promise.allSettled(communications.map(indexOnePage));\n  const ok = results.filter(r => r.status === "fulfilled" && r.value === true).length;\n  if(searchIndexStatus){\n    searchIndexStatus.textContent = `${ok}/${communications.length} pages indexées pour la recherche`;\n  }\n  if(search.value.trim()) showResults();\n}\n'''
    new='''async function indexPageContents(){\n  if(searchIndexStatus) searchIndexStatus.textContent = "Indexation de la recherche transversale…";\n  const pool = globalCommunications.length ? globalCommunications : communications;\n  const results = await Promise.allSettled(pool.map(indexOnePage));\n  const ok = results.filter(r => r.status === "fulfilled" && r.value === true).length;\n  if(searchIndexStatus){ searchIndexStatus.textContent = ok + "/" + pool.length + " pages indexées tous périmètres confondus"; }\n  if(search.value.trim()) showResults();\n}\n'''
    s=s.replace(old,new,1)
    oldf='''  let filtered = communications.filter(item => {\n    const haystack = item._searchText || normalizeSearchText(\n      `${item.title} ${item.description} ${item.category}`\n    );\n    return (!q || haystack.includes(q)) &&\n           (!activeCategory || item.category === activeCategory);\n  });'''
    newf='''  const sourceItems = q ? (globalCommunications.length ? globalCommunications : communications) : communications;\n  let filtered = sourceItems.filter(item => {\n    const haystack = item._searchText || normalizeSearchText((item.title||"")+" "+(item.description||"")+" "+(item.category||"")+" "+(item.scope||""));\n    return (!q || haystack.includes(q)) && (!activeCategory || item.category === activeCategory);\n  });'''
    s=s.replace(oldf,newf,1)
    oldcard='''            <span class="category type-pill-${categorySlug(item.category)}">${escapeHtml(item.category || "Sans catégorie")}</span>\n            <h3>${escapeHtml(item.title)}</h3>'''
    newcard='''            <span class="category type-pill-${categorySlug(item.category)}">${escapeHtml(item.category || "Sans catégorie")}</span>\n            <span class="scope-badge">${escapeHtml(item.scope || "Périmètre non précisé")}</span>\n            <h3>${escapeHtml(item.title)}</h3>'''
    s=s.replace(oldcard,newcard,1)
    start=s.index('async function loadCommunications(){')
    end=s.index('\nsearch.addEventListener("input"',start)
    s=s[:start]+new_load+s[end:]
    portal_path.write_text(s,encoding='utf-8')
