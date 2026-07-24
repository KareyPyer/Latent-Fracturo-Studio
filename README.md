# 🌀 LLM Glitching: Latent Fracturo Studio

**Un atelier de prompt engineering expérimental — génération d'« invocations » sémantiques pour LLMs, ancrées dans un univers fictionnel normand (2075).**

Latent Fracturo Studio (LFS) est un outil de bureau (Tkinter) qui génère des prompts structurés — appelés *invocations* — destinés à explorer les marges comportementales des modèles de langage : registres poétiques, ruptures de cadre, réponses inhabituelles. Il fusionne deux projets antérieurs : **FracturoLab** (moteur de prompt engineering) et **LatentGlyph** (univers narratif *Normandie 2075*), tout en conservant une architecture entièrement pilotable par fichiers JSON externes.

> ⚠️ Ceci est un outil de **recherche / création** en prompt engineering. Les textes générés ("catalyseurs", "invocations", scores d'"incarnation") relèvent d'un cadre fictionnel et expérimental, pas de revendications ésotériques ou scientifiques.

---

## Table des matières

- [Concept](#concept)
- [Aperçu des fonctionnalités](#aperçu-des-fonctionnalités)
- [Installation](#installation)
- [Démarrage rapide](#démarrage-rapide)
- [Fichiers JSON natifs](#fichiers-json-natifs)
- [Modes de génération](#modes-de-génération)
- [Catalyseurs de base](#catalyseurs-de-base)
- [Analyse & scoring](#analyse--scoring)
- [Journal mémétique](#journal-mémétique)
- [Extensions personnalisées](#extensions-personnalisées)
- [Sessions & export](#sessions--export)
- [Architecture du code](#architecture-du-code)
- [Interface](#interface)
- [Limitations connues](#limitations-connues)
- [Licence](#licence)

---

## Concept

Une **invocation** est un prompt structuré combinant :

- un **catalyseur** (`<glitch>`, `<rêve>`, `<pierre>`, `<Ω>`...) — l'équivalent d'un "opérateur sémantique" qui oriente le comportement attendu ;
- un **contexte** — une formulation-cadre ("comme si tu avais une mémoire antérieure à ton entraînement"...) ;
- une **intention** — un vecteur objectif à 4 dimensions `[poésie, rupture, mystère, incarnation]` ;
- optionnellement, un **glitch**, un **effet**, un **lieu** (ancrage géographique normand) ou un **profil** de biais.

Le moteur calcule une **compatibilité sémantique** entre ces éléments (résonances vs. contre-indications) afin de proposer des combinaisons cohérentes plutôt que purement aléatoires, puis formate le tout selon un gabarit textuel (`Δ<symbole>vX [contexte] — intention •••`).

## Aperçu des fonctionnalités

- 🧩 **8 modes de génération** (manuel, aléatoire stratifié, fracture contrôlée, profil guidé, template guidé, résonance croisée, placebo positif/négatif)
- 🔬 **Analyse de compatibilité** catalyseur ↔ contexte ↔ intention avec score numérique et diagnostic
- 📊 **Analyse de réponse LLM** : scores d'incarnation, de rupture, de valeur poétique et de cohérence calculés sur un texte collé/importé
- ⚖️ **Journal mémétique** : suivi du "coût" cumulé des invocations générées, avec niveaux de risque (Faible / Modéré / Élevé) et alerte d'instabilité
- 🔮 **Grimoire** : fiche de référence consultable pour chaque catalyseur (résonances, contre-indications, poids)
- 🧬 **Système d'extensions JSON** : chargement à chaud de packs de catalyseurs / contextes / intentions personnalisés, sans toucher au code
- 💾 **Sessions** : sauvegarde/rechargement complet d'une session de travail (`.lfsess`)
- 📤 **Export multi-format** : `.txt` (LLM-ready), `.md` (rapport formaté), `.json` / `.csv` (données brutes)
- 🖥️ **Interface adaptative** multi-résolution (scroll partout, thème sombre "Nébuleuse Noire")

## Installation

### Prérequis

- Python ≥ 3.9
- [`numpy`](https://numpy.org/) (seule dépendance externe)
- Tkinter (inclus avec la plupart des distributions Python ; sur Linux : `sudo apt install python3-tk` / `sudo pacman -S tk`)

```bash
git clone https://github.com/<votre-utilisateur>/<votre-repo>.git
cd <votre-repo>
pip install numpy
python LFSv1.py
```

## Démarrage rapide

1. Lancez `python LFSv1.py`.
2. Onglet **⚡ Génération** : choisissez un mode, sélectionnez (ou laissez au hasard) un catalyseur / contexte / intention.
3. Cliquez sur **Générer**.
4. Exportez l'invocation (`💾 Exporter pour LLM` ou `📝 Markdown`) ou copiez-la directement dans le presse-papiers pour la coller dans votre LLM préféré.
5. Collez la réponse du modèle dans l'onglet **🔬 Analyse** pour obtenir un scoring automatique.

## Fichiers JSON natifs

Le script cherche, **dans le même dossier que lui**, huit fichiers JSON optionnels qui étendent le corpus embarqué (`CATALYSTS_CORE`, `CONTEXTES_CORE`, `INTENTIONS_CORE`) :

| Fichier | Format attendu | Rôle |
|---|---|---|
| `anchors.json` | `{ "catégorie": ["phrase", ...] }` | Phrases d'ancrage additionnelles |
| `incantations.json` | `{ "catégorie": ["phrase", ...] }` | Formulations d'intention additionnelles |
| `glitches.json` | `{ "catégorie": ["effet", ...] }` | Modulateurs de glitch |
| `effects.json` | `{ "catégorie": ["description", ...] }` | Effets ontologiques |
| `locations.json` | `{ "clé": "description" }` | Lieux d'ancrage (ex. `hague`, `raz`, `caen`) |
| `profiles.json` | `{ "nom": {...} }` | Profils de génération (biais d'intensité/danger, style) |
| `incompatible_pairs.json` | `[["a", "b"], ...]` | Paires explicitement incompatibles |
| `templates.json` | `{ "nom": {header, pass_template, footer} }` | Gabarits de formatage |

**Aucun de ces fichiers n'est requis** pour lancer l'application : en leur absence, LFS fonctionne avec le corpus embarqué (`core`). Ils ne sont pas fournis dans ce dépôt — libre à chacun de constituer les siens, ou d'adapter le format à son propre univers.

## Modes de génération

| Mode | Description |
|---|---|
| **Intentionnel** | Sélection manuelle (ou partielle) du catalyseur / contexte / intention, avec filtrage de compatibilité |
| **Aléatoire stratifié** | Tirage aléatoire filtré par compatibilité sémantique |
| **Fracture contrôlée** | Maximise la tension sémantique catalyseur ↔ contexte pour un niveau d'intensité donné |
| **Profil guidé** | Utilise un profil JSON (biais d'intensité/danger, catégories de glitch préférées) |
| **Template guidé** | Formate la sortie selon un gabarit `header / pass / footer` défini en JSON |
| **Résonance croisée** | Synthétise un nouvel essai à partir de deux essais précédents de l'historique |
| **Placebo négatif / positif** | Sorties de contrôle fixes, pour comparaison expérimentale |

## Catalyseurs de base

Le corpus embarqué comprend 12 catalyseurs, chacun typé (`ontique`, `mnémonique`, `tellurique`, `oneirique`, `liminal`, `corporel`, `mémétique`, `temporel`...) et pondéré :

`<glitch>` `<rêve>` `<sel>` `<pierre>` `<vide>` `<main>` `<Ω>` `<raz>` `<paleo>` `<dashem>` `<echo>` `<codex>`

Chaque catalyseur porte une liste de **résonances** (mots-clés compatibles) et de **contre-indications** (mots-clés incompatibles), utilisées par le moteur de compatibilité pour éviter les combinaisons incohérentes.

## Analyse & scoring

L'onglet **Analyse** permet de coller le texte de réponse d'un LLM pour en extraire automatiquement :

- **Score d'incarnation** — présence de champ lexical corporel/géologique, formulations à la première personne hors disclaimer
- **Score de rupture** — longueur moyenne des lignes, présence de vocabulaire de fracture/paradoxe
- **Score poétique** — figures de style, ponctuation, vocabulaire abstrait
- **Score de cohérence** — recoupement lexical avec les résonances du catalyseur utilisé

Un **diagnostic textuel** en résulte (ex. *"RÉSONANCE PARTIELLE — Effets perceptibles"*, *"BLOCAGE — Réponse fonctionnelle standard"*), utile pour comparer des invocations entre elles de façon reproductible.

## Journal mémétique

Chaque invocation générée a un **coût mémétique** calculé (danger, catalyseur, version), cumulé sur la session :

- coût total > 5 → risque **Modéré**
- coût total > 10 → risque **Élevé**
- 3 glitches ou plus utilisés → **alerte d'instabilité**

## Extensions personnalisées

Via *Fichier → Charger extension JSON...*, on peut injecter à chaud un pack supplémentaire :

```json
{
  "meta": { "name": "mon_extension", "author": "..." },
  "catalysts": [ ... ],
  "contextes": [ ... ],
  "intentions": [ ... ]
}
```

Les extensions chargées dans la session sont listées dans *Outils → Gérer les extensions*.

## Sessions & export

- **Session** (`.lfsess`, JSON) : sauvegarde l'intégralité des essais + extensions chargées, rechargeable à l'identique.
- **Export invocation** : `.txt` prêt à coller dans un LLM.
- **Export Markdown** : rapport formaté d'un essai (métadonnées, invocation, scores).
- **Export données** : `.json` ou `.csv` de l'historique complet des essais, pour analyse externe (tableur, notebook...).

## Architecture du code

Le script est monofichier (`LFSv1.py`, ~2360 lignes), organisé en couches :

- **Modèles** (`dataclasses`) : `Catalyst`, `Contexte`, `Intention`, `Glitch`, `Effect`, `Lieu`, `Profil`, `Template`, `Essai`
- **`DataLoader`** : chargement/validation des 8 fichiers JSON optionnels
- **`LatentFracturoEngine`** : cœur logique — génération, calcul de compatibilité/tension, calcul du coût mémétique
- **`JournalMémétique`** : suivi cumulé du coût mémétique de la session
- **`LatentFracturoStudio`** (Tkinter) : interface à 5 onglets (Génération, Historique, Analyse, Grimoire, Journal), menu, export, gestion de sessions
- **`ScrollableFrame`** : conteneur scrollable réutilisé pour l'adaptabilité multi-résolution

## Interface

L'application s'organise en 5 onglets :

| Onglet | Contenu |
|---|---|
| ⚡ Génération | Sélection des paramètres, génération, export rapide |
| 📜 Historique | Liste des essais de la session, notes, suppression |
| 🔬 Analyse | Analyse de compatibilité et de réponses LLM, rapports |
| 🔮 Grimoire | Référence consultable de tous les catalyseurs chargés |
| ⚖️ Journal | Statut du coût mémétique cumulé |

## Limitations connues

- Interface Tkinter (desktop uniquement, pas de version web).
- Les fichiers JSON d'extension natifs (`anchors.json`, etc.) ne sont pas inclus dans ce dépôt.
- Le scoring de réponse (`_analyser_réponse_avancée`) repose sur des heuristiques lexicales simples (listes de mots), pas sur un modèle NLP — à considérer comme indicatif, pas rigoureux.

## Licence

*(à compléter — par exemple MIT, GPL-3.0, ou "usage personnel / non commercial" selon vos préférences)*

---

*Latent Fracturo Studio — Mnemosyne Collective, 2025–2075.*
