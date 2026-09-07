# Kit de communication CAT Énergies

Socle commun pour les communications web CAT Énergies, avec paramètres Cattenom par défaut.

## Principes permanents

- Logo officiel : `/edf/logo-cat-energies.svg`
- Portail Cattenom : `/edf/dpn/cattenom/`
- Contact : `cat-energies-cattenom@edf.fr`
- GoatCounter : `cat-energies-cattenom`
- Les proportions du logo ne doivent jamais être déformées.
- Les pages doivent rester lisibles sur ordinateur et mobile.
- Les avatars sont recommandés pour les sujets humains, participatifs ou de mobilisation ; ils ne sont pas obligatoires sur les communications institutionnelles.

## Types de communication

| Type | Attribut HTML | Accent | Intention |
| --- | --- | --- | --- |
| Communiqué / information | `data-communication="information"` | Bleu | sobre, crédible, informatif |
| Mobilisation | `data-communication="mobilisation"` | Jaune | dynamique, impactant, appel à l'action |
| Adhésion | `data-communication="adhesion"` | Vert | accueillant, positif, CTA visible |
| Sondage / participation | `data-communication="sondage"` | Violet | dialogue, participation, avatars |
| Guide pratique | `data-communication="guide"` | Bleu soutenu | pédagogique, structuré, navigation claire |
| EDF SA / IEG | `data-communication="edf-sa"` | Turquoise | périmètre plus large que Cattenom |

## À inclure dans une nouvelle page

Dans `<head>` :

```html
<link rel="stylesheet" href="/assets/cat-energies/css/cat-theme.css">
<script src="/assets/cat-energies/js/cat-config.js"></script>
<script defer src="/assets/cat-energies/js/cat-tracking.js"></script>
```

Puis définir le type sur `<body>`, par exemple :

```html
<body data-communication="mobilisation">
```

Le tracking GoatCounter est alors chargé depuis la configuration centrale.

## Structure recommandée

```text
assets/cat-energies/
  css/
    cat-theme.css
  js/
    cat-config.js
    cat-tracking.js
edf/
  communiques/
  guides/
  fiches-pratiques/
  dpn/
    cattenom/
      adhesion/
      communiques/
      guides/
      fiches-pratiques/
```

## Règle de périmètre

Une communication strictement locale reste sous `edf/dpn/cattenom/`.
Une communication EDF SA transverse reste sous `edf/` dans sa catégorie correspondante.

Les deux guides de l'alternance peuvent donc coexister lorsqu'ils répondent à deux périmètres différents : EDF SA et Cattenom.
