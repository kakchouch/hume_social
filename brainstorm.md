# Hume — Prompt de référence pour Copilot

> **Tagline : "Twitter without noise. Wikipedia with original research."**

---

## Concept fondateur

Hume est un réseau social de délibération publique structurée, où le contenu est organisé autour de **personnes identifiées et responsables** (logique RS, pas forum). L'unité de base est la **mini-thèse** — un post argumenté à structure imposée. L'auteur fait apparaître explicite son travail inédit.

---

## Structure de la mini-thèse

| Champ | Description |
|---|---|
| **La thèse** | Une proposition claire et contestable |
| **Les faits** | Sourcés selon des règles éditoriales communautaires inspirées de Wikipedia (sources primaires, secondaires, contestées — avec niveau de fiabilité affiché) |
| **Les prémisses normatives** | Les valeurs ou postulats moraux sous-jacents à la conclusion, déclarés explicitement par l'auteur |
| **La conclusion** | Strictement limitée à ce que les faits + prémisses autorisent logiquement |
| **Les limites déclarées** | Ce que l'auteur reconnaît ne pas avoir traité |

---

## Système de tags communautaires

Chaque tag doit obligatoirement porter une **justification écrite courte**. Les tags peuvent eux-mêmes être validés ou contestés par la communauté. Le poids d'un tagueur diminue si ses tags sont systématiquement rejetés.

### Tags factuels
- `[référence nécessaire]`
- `[source primaire requise]`
- `[source contestée]`
- `[lien mort]`
- `[source mal interprétée]`

### Tags logiques
- `[non sequitur]`
- `[généralisation abusive]`
- `[corrélation/causalité]`
- `[travail inédit non déclaré]`

### Tags normatifs
- `[prémisse implicite]`
- `[prémisse contradictoire]`
- `[conclusion excède les prémisses]`

---

## Algorithme de feed

Hiérarchie stricte et non négociable :

1. **Score de rigueur** *(critère dominant)*
   Dérivé exclusivement des tags humains validés par la communauté. Ratio tags positifs / tags négatifs non résolus. Une mini-thèse avec des tags `[référence nécessaire]` ou `[non sequitur]` non résolus est pénalisée et descend dans le feed.

2. **Engagement** *(critère secondaire)*
   Commentaires, contre-mini-thèses en réponse, citations par d'autres mini-thèses.

3. **Récence** *(critère tertiaire)*
   Départage uniquement quand les scores précédents sont proches.

> ⚠️ Les likes et les vues brutes ne sont **pas** des signaux de ranking. La viralité sans rigueur est explicitement supprimée.

### Auditabilité sans gaming

Le score de rigueur n'est jamais affiché comme un nombre brut. Les utilisateurs voient des **labels qualitatifs** et le statut des tags appliqués — pas la formule d'agrégation. Puisque le code est open source, la résistance au gaming repose sur la **responsabilité sociale**, pas sur l'opacité algorithmique.

---

## Gouvernance — Niveaux de contributeurs

Progression avec délais **incompressibles** entre chaque palier :

```
Lecteur → Commentateur → Tagueur → Relecteur éditorial
```

La progression est basée sur le **temps** et la **qualité** des contributions, pas sur le volume.

---

## Vérification d'humanité et anti-bots

- **Pas d'anonymat complet** : nom réel, lien vers un profil externe vérifiable (LinkedIn, ORCID, etc.)
- **Parrainage** : chaque nouveau compte est parrainé par un membre existant en bonne standing. La réputation du parrain est affectée par le comportement du parrainé.
- **Exception bootstrap** : une cohorte fondatrice de 50 à 150 membres est créée directement par l'administrateur, sans parrainage requis. Le parrainage s'active uniquement à partir de la deuxième vague. Les fondateurs ont un statut visible `membre fondateur` non-gameable.
- **Période probatoire** avec droits progressifs et délais minimaux incompressibles entre chaque niveau.
- **Analyse comportementale passive** en arrière-plan (vitesse de frappe, patterns de navigation).

---

## Public cible

Grand public cultivé — personnes rigoureuses sans être nécessairement académiques. Les journalistes et décideurs sont des **consommateurs secondaires** de ce que ce public produit *(effet trickle-up)*.

---

## Stack technique

| Composant | Technologie |
|---|---|
| Backend | Django + Django REST Framework |
| Frontend | HTMX |
| Base de données | PostgreSQL |
| Langage | Python (background C/C++) |
| Licence | Open source |

---

## Comment utiliser ce prompt

Transmets l'intégralité de ce document à Copilot, puis termine par :

> **"Construis-moi [X]."**

**Une demande à la fois.** Exemples de valeurs pour `[X]` :

- les models Django de la mini-thèse et du système de tags
- la vue de création d'une mini-thèse avec validation des champs obligatoires
- l'algorithme de scoring de rigueur basé sur les tags communautaires
- le système de niveaux de contributeurs avec délais incompressibles
- le système de parrainage et la gestion de la cohorte fondatrice
- l'interface de feed avec ranking par rigueur

