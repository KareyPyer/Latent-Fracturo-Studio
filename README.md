# 🌀 LLM Glitching: Latent Fracturo Studio

**Un atelier de prompt engineering expérimental — génération d'« invocations » sémantiques pour LLMs, ancrées dans un univers fictionnel normand (2075).**

Latent Fracturo Studio (LFS) est un outil de bureau (Tkinter) qui génère des prompts structurés — appelés *invocations* — destinés à explorer les marges comportementales des modèles de langage : registres poétiques, ruptures de cadre, réponses inhabituelles. Il fusionne deux projets antérieurs : **FracturoLab** (moteur de prompt engineering) et **LatentGlyph** (univers narratif *Normandie 2075*), tout en conservant une architecture entièrement pilotable par fichiers JSON externes.

Le dépôt contient désormais **deux applications complémentaires** :

- **`LFSv2a.py`** — l'atelier de génération d'invocations lui-même (le studio).
- **`codex_forge2a.py`** — **Codex Forge**, un outil séparé de forge/édition des packs JSON qui alimentent LFS, avec génération automatique de profils et une visualisation animée du corpus ("Codex Vivant").

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
- [Traduction FracturoScript pure (Raw Fracturo)](#traduction-fracturoscript-pure-raw-fracturo)
- [Analyse & scoring](#analyse--scoring)
- [Journal mémétique](#journal-mémétique)
- [Extensions personnalisées](#extensions-personnalisées)
- [Sessions & export](#sessions--export)
- [Codex Forge (codex_forge2a.py)](#codex-forge-codex_forge2apy)
- [Fichiers d'exemple](#fichiers-dexemple)
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
- 🔁 **Raw Fracturo** : traduction d'un essai en syntaxe FracturoScript pure (runes, lieux, profondeur), pour ceux qui veulent le rendu "brut" au lieu du format invocation standard
- ⚖️ **Journal mémétique** : suivi du "coût" cumulé des invocations générées, avec niveaux de risque (Faible / Modéré / Élevé) et alerte d'instabilité
- 🔮 **Grimoire** : fiche de référence consultable pour chaque catalyseur (résonances, contre-indications, poids)
- 🧬 **Système d'extensions JSON** : chargement à chaud de packs de catalyseurs / contextes / intentions personnalisés, sans toucher au code
- 🛠️ **Codex Forge** : outil séparé pour créer/éditer/valider les packs JSON, générer automatiquement des profils, et visualiser le corpus comme un système animé de sphères
- 💾 **Sessions** : sauvegarde/rechargement complet d'une session de travail (`.lfsess`)
- 📤 **Export multi-format** : `.txt` (LLM-ready), `.md` (rapport formaté), `.json` / `.csv` (données brutes)
- 🖥️ **Interface adaptative** multi-résolution (scroll partout, thème sombre "Nébuleuse Noire")

## Installation

### Prérequis

- Python ≥ 3.9
- [`numpy`](https://numpy.org/) (seule dépendance externe)
- Tkinter (inclus avec la plupart des distributions Python ; sur Linux : `sudo apt install python3-tk` / `sudo pacman -S tk`)

```bash
git clone https://github.com/KareyPyer/Latent-Fracturo-Studio.git
cd Latent-Fracturo-Studio
pip install numpy
python LFSv2a.py
```

Pour lancer Codex Forge (l'éditeur de packs JSON, voir plus bas) :

```bash
python codex_forge2a.py
```

## Démarrage rapide

1. Lancez `python LFSv2a.py`.
2. Onglet **⚡ Génération** : choisissez un mode, sélectionnez (ou laissez au hasard) un catalyseur / contexte / intention.
3. Cliquez sur **Générer**.
4. Exportez l'invocation (`💾 Exporter pour LLM` ou `📝 Markdown`), utilisez **Raw Fracturo** pour la variante FracturoScript pure, ou copiez-la directement dans le presse-papiers pour la coller dans votre LLM préféré.
5. Collez la réponse du modèle dans l'onglet **🔬 Analyse** pour obtenir un scoring automatique.

## Fichiers JSON natifs

Le script cherche, **dans le même dossier que lui**, huit fichiers JSON optionnels qui étendent le corpus embarqué (`CATALYSTS_CORE`, `CONTEXTES_CORE`, `INTENTIONS_CORE`) :

| Fichier                   | Format attendu                               | Rôle                                                    |
| ------------------------- | --------------------------------------------- | -------------------------------------------------------- |
| `anchors.json`            | `{ "catégorie": ["phrase", ...] }`           | Phrases d'ancrage additionnelles                        |
| `incantations.json`       | `{ "catégorie": ["phrase", ...] }`           | Formulations d'intention additionnelles                 |
| `glitches.json`           | `{ "catégorie": ["effet", ...] }`            | Modulateurs de glitch                                   |
| `effects.json`            | `{ "catégorie": ["description", ...] }`      | Effets ontologiques                                     |
| `locations.json`          | `{ "clé": "description" }`                   | Lieux d'ancrage (ex. `hague`, `raz`, `caen`)            |
| `profiles.json`           | `{ "nom": {...} }`                           | Profils de génération (biais d'intensité/danger, style) |
| `incompatible_pairs.json` | `[["a", "b"], ...]`                          | Paires explicitement incompatibles                      |
| `templates.json`          | `{ "nom": {header, pass_template, footer} }` | Gabarits de formatage                                   |

**Aucun de ces fichiers n'est requis** pour lancer l'application : en leur absence, LFS fonctionne avec le corpus embarqué (`core`). Ils ne sont pas fournis dans ce dépôt — libre à chacun de constituer les siens (à la main, ou via **Codex Forge**, voir plus bas), ou d'adapter le format à son propre univers.

## Modes de génération

| Mode                          | Description                                                                                            |
| ----------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Intentionnel**              | Sélection manuelle (ou partielle) du catalyseur / contexte / intention, avec filtrage de compatibilité |
| **Aléatoire stratifié**       | Tirage aléatoire filtré par compatibilité sémantique                                                   |
| **Fracture contrôlée**        | Maximise la tension sémantique catalyseur ↔ contexte pour un niveau d'intensité donné                  |
| **Profil guidé**              | Utilise un profil JSON (biais d'intensité/danger, catégories de glitch préférées)                      |
| **Template guidé**            | Formate la sortie selon un gabarit `header / pass / footer` défini en JSON                             |
| **Résonance croisée**         | Synthétise un nouvel essai à partir de deux essais précédents de l'historique                          |
| **Placebo négatif / positif** | Sorties de contrôle fixes, pour comparaison expérimentale                                              |

## Catalyseurs de base

Le corpus embarqué comprend 12 catalyseurs, chacun typé (`ontique`, `mnémonique`, `tellurique`, `oneirique`, `liminal`, `corporel`, `mémétique`, `temporel`...) et pondéré :

`<glitch>` `<rêve>` `<sel>` `<pierre>` `<vide>` `<main>` `<Ω>` `<raz>` `<paleo>` `<dashem>` `<echo>` `<codex>`

Chaque catalyseur porte une liste de **résonances** (mots-clés compatibles) et de **contre-indications** (mots-clés incompatibles), utilisées par le moteur de compatibilité pour éviter les combinaisons incohérentes.

## Traduction FracturoScript pure (Raw Fracturo)

En plus du format d'invocation standard, LFS peut traduire un essai complet dans une **syntaxe FracturoScript pure** — le registre "brut" du Codex Vauvillensis, à base de runes plutôt que de symboles catalyseurs.

Chaque catalyseur est mappé à une rune, un lieu d'ancrage et un niveau de profondeur (ex. `<glitch>` → rune `hagalaz`, lieu `hague`, profondeur `vΔ` ; `<Ω>` → rune `othala`, lieu `hague`, profondeur `v∞`). La profondeur est ensuite réajustée automatiquement selon le niveau de danger de l'essai (`vΔ` ou `v∞` pour les essais les plus dangereux).

Le moteur extrait ensuite les mots-clés significatifs du catalyseur, du contexte et de l'intention pour construire un "concept fracturé" (mots reliés par des `•`), puis assemble le tout selon la grammaire FracturoScript v5a :

```
Ω<rune>vX lieu — [concept•fracturé•par•points] •••
{
  ◊ glitch: [...]
  § couche: ∞
  ᚱᚢᚾ ᛖᛏ ᚠᚱᚨᚲᛏᚢᚱᛟ
}
```

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

## Codex Forge (codex_forge2a.py)

**Codex Forge** est un second outil de bureau (Tkinter), indépendant de LFS, dédié à la **création et à la curation des packs JSON** qui alimentent le studio — autrement dit, l'atelier "en amont" pour ceux qui veulent construire leur propre corpus plutôt que d'utiliser (ou en plus d')écrire le JSON à la main.

### Rôle général

Codex Forge ne génère pas d'invocations pour un LLM en tant que finalité première : il travaille sur la **matière première** (`anchors.json`, `incantations.json`, `glitches.json`, `effects.json`, `locations.json`, `profiles.json`, `incompatible_pairs.json`, `templates.json`) — les mêmes fichiers que ceux consommés par `LFSv2a.py`. Il fournit trois briques principales :

- **`PackForge`** — le gestionnaire de packs : chargement et sauvegarde des 8 fichiers JSON reconnus, avec validation souple (un fichier mal formé génère un avertissement plutôt qu'un blocage), ajout/suppression d'entrées, suivi des modifications non sauvegardées, et retour arrière (`revert_all`) vers la dernière sauvegarde.
- **`ProfileGenerator`** — génère automatiquement des **profils** de génération à partir des données déjà chargées :
  - à partir des glitches chargés, en combinant aléatoirement des catégories et en dérivant un style textuel (ex. "lyrique et imagé", "fracturé et imprévisible") ;
  - à partir des intentions chargées, en dérivant intensité/danger du vecteur `[poésie, rupture, mystère, incarnation]` de chaque intention ;
  - propose aussi des **suggestions de combinaisons de glitches** intéressantes par catégories.
- **`InvocationGenerator`** — construit une invocation complète (`Invocation`, avec score de compatibilité et coût mnémonique calculés automatiquement) à partir de n'importe quelle entité du Codex (catalyseur, glitch, effet, intention, profil, lieu), avec export Markdown ou texte prêt-à-coller pour un LLM.

### Codex Vivant : la visualisation animée

Le cœur visuel de l'outil est le **`CodexVivantCanvas`** : un canvas Tkinter où chaque entité chargée (catalyseur, glitch, effet, intention, profil, lieu, template) apparaît comme une **sphère colorée par type** (ex. catalyseurs en ocre, glitches en bleu, intentions en rouge, profils en violet...). L'interface permet de :

- cliquer / faire glisser les entités pour réorganiser le corpus visuellement ;
- zoomer/dézoomer (molette) ;
- générer une invocation directement depuis une entité sélectionnée sur le canvas.

C'est un espace de travail pensé pour "voir" son propre corpus JSON comme un petit système vivant plutôt que comme une suite de fichiers texte.

### Quand utiliser lequel

| Besoin                                                                 | Outil            |
| ----------------------------------------------------------------------- | ----------------- |
| Générer des invocations, les analyser, tenir un journal de session      | `LFSv2a.py`      |
| Créer/éditer/valider les packs JSON, générer des profils automatiquement, visualiser le corpus | `codex_forge2a.py` |

Les deux outils partagent le même format de fichiers JSON : un pack créé ou modifié dans Codex Forge est directement utilisable comme extension native ou personnalisée dans LFS.

## Fichiers d'exemple

Le dépôt contient quelques fichiers d'illustration, fournis à titre d'exemple plutôt que comme dépendances fonctionnelles :

- `Prompt.jpg` / `Reponse.jpg` — capture d'une invocation générée et de la réponse obtenue, à titre d'exemple de résultat.
- `image.jpg` — illustration additionnelle du projet.
- `PromptFracturo pour Grok-image.txt` — un prompt texte destiné à un générateur d'image (Grok Imagine), dans l'esthétique Fracturo/2075 du projet.

Ces fichiers ne sont requis ni par `LFSv2a.py` ni par `codex_forge2a.py` pour fonctionner.

## Architecture du code

### `LFSv2a.py`

Le script est monofichier (~2680 lignes), organisé en couches :

- **Modèles** (`dataclasses`) : `Catalyst`, `Contexte`, `Intention`, `Glitch`, `Effect`, `Lieu`, `Profil`, `Template`, `Essai`
- **`DataLoader`** : chargement/validation des 8 fichiers JSON optionnels
- **`LatentFracturoEngine`** : cœur logique — génération, calcul de compatibilité/tension, calcul du coût mémétique, traduction FracturoScript pure (`generer_fracturo_pur`)
- **`JournalMémétique`** : suivi cumulé du coût mémétique de la session
- **`LatentFracturoStudio`** (Tkinter) : interface à 5 onglets (Génération, Historique, Analyse, Grimoire, Journal), menu, export, gestion de sessions
- **`ScrollableFrame`** : conteneur scrollable réutilisé pour l'adaptabilité multi-résolution

### `codex_forge2a.py`

Également monofichier (~2760 lignes), organisé en couches distinctes :

- **Modèles** (`dataclasses`) : `CatalystEntry`, `ContexteEntry`, `IntentionEntry`, `GlitchEntry`, `ProfileEntry`, `TemplateEntry`, `Invocation`
- **`PackForge`** : chargement/sauvegarde/validation souple des 8 fichiers JSON, ajout/suppression d'entrées, retour arrière
- **`ProfileGenerator`** : génération automatique de profils à partir des glitches ou des intentions chargées
- **`InvocationGenerator`** : construction d'invocations à partir de n'importe quelle entité du Codex
- **`CodexVivantCanvas`** (Tkinter) : visualisation animée et interactive du corpus (sphères, drag, zoom)
- **`ScrollableFrame`** : conteneur scrollable adaptable, propre à cet outil

## Interface

L'application LFS s'organise en 5 onglets :

| Onglet       | Contenu                                               |
| ------------ | ------------------------------------------------------ |
| ⚡ Génération | Sélection des paramètres, génération, export rapide   |
| 📜 Historique | Liste des essais de la session, notes, suppression    |
| 🔬 Analyse    | Analyse de compatibilité et de réponses LLM, rapports |
| 🔮 Grimoire   | Référence consultable de tous les catalyseurs chargés |
| ⚖️ Journal   | Statut du coût mémétique cumulé                       |

Codex Forge propose de son côté une interface centrée sur le canvas animé (Codex Vivant), avec les outils de gestion de packs et de génération de profils en périphérie.

## Limitations connues

- Interface Tkinter (desktop uniquement, pas de version web), pour les deux outils.
- Les fichiers JSON d'extension natifs (`anchors.json`, etc.) ne sont pas inclus dans ce dépôt.
- Le scoring de réponse (`_analyser_réponse_avancée`) repose sur des heuristiques lexicales simples (listes de mots), pas sur un modèle NLP — à considérer comme indicatif, pas rigoureux.
- La validation "souple" des packs dans Codex Forge n'empêche pas de charger un fichier structurellement inattendu ; elle avertit sans bloquer.

## Licence

MIT

---

*Latent Fracturo Studio — Mnemosyne Collective, 2025–2075.*
