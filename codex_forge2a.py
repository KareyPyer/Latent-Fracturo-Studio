#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CODEX FORGE — Atelier de forge JSON pour Latent-Fracturo-Studio
Version: 2.1.0 (2075, Révision du Codex Vivant)
Auteur: Mnemosyne Collective

"Là où les données deviennent matière à invocation."
"""

import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from copy import deepcopy
from pathlib import Path
import hashlib
from datetime import datetime
import random
import math
import threading
import time
import re

# ============================================================================
# MODÈLES DE DONNÉES — L'ÂME DU CODEX
# ============================================================================

@dataclass
class CatalystEntry:
    """Un catalyseur sémantique pour les invocations."""
    id: str
    symbol: str
    name: str
    type: str
    weight: float
    resonances: List[str]
    contraindications: List[str]
    description: str
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "symbol": self.symbol,
            "name": self.name,
            "type": self.type,
            "weight": self.weight,
            "resonances": self.resonances,
            "contraindications": self.contraindications,
            "description": self.description,
            "tags": self.tags
        }

@dataclass
class ContexteEntry:
    """Un cadre contextuel pour les invocations."""
    id: str
    text: str
    weight: float
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {"id": self.id, "text": self.text, "weight": self.weight, "tags": self.tags}

@dataclass
class IntentionEntry:
    """Une intention à 4 dimensions."""
    id: str
    name: str
    vector: List[float]
    description: str
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "vector": self.vector,
            "description": self.description,
            "tags": self.tags
        }

@dataclass
class GlitchEntry:
    """Un modulateur de glitch."""
    id: str
    effect: str
    category: str
    intensity: float
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "effect": self.effect,
            "category": self.category,
            "intensity": self.intensity,
            "tags": self.tags
        }

@dataclass
class ProfileEntry:
    """Un profil de génération."""
    id: str
    name: str
    bias_intensity: float
    bias_danger: float
    preferred_glitch_categories: List[str]
    style: str
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "bias_intensity": self.bias_intensity,
            "bias_danger": self.bias_danger,
            "preferred_glitch_categories": self.preferred_glitch_categories,
            "style": self.style,
            "tags": self.tags
        }

@dataclass
class TemplateEntry:
    """Un gabarit de formatage."""
    id: str
    name: str
    header: str
    pass_template: str
    footer: str
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "header": self.header,
            "pass_template": self.pass_template,
            "footer": self.footer,
            "tags": self.tags
        }

@dataclass
class Invocation:
    """Une invocation complète générée par le Codex."""
    catalyst: str
    context: str
    intention: str
    glitch: Optional[str] = None
    effect: Optional[str] = None
    location: Optional[str] = None
    full_text: str = field(init=False)
    compatibility_score: float = 0.0
    mnemonic_cost: float = 0.0
    
    def __post_init__(self):
        """Construit le texte complet de l'invocation."""
        parts = []
        
        # Glitch (optionnel)
        if self.glitch:
            parts.append(f"<{self.glitch}>")
        
        # Catalyseur (obligatoire)
        parts.append(f"<{self.catalyst}>")
        
        # Contexte (obligatoire)
        context_text = self.context
        if self.location:
            context_text = f"{self.location} — {context_text}"
        parts.append(f"Δ{self.catalyst.upper()[:2]}{random.randint(1,9)} {context_text}")
        
        # Intention
        parts.append(f"— intention ••• {self.intention}")
        
        # Effet (optionnel)
        if self.effect:
            parts.append(f"[{self.effect}]")
        
        self.full_text = " ".join(parts)
        
        # Calcul du coût mémétique
        self.mnemonic_cost = self._calculate_mnemonic_cost()
        
        # Calcul de la compatibilité
        self.compatibility_score = self._calculate_compatibility()
    
    def _calculate_mnemonic_cost(self) -> float:
        """Calcule le coût mémétique de l'invocation."""
        cost = 0.0
        
        # Poids des éléments
        cost += len(self.catalyst) * 0.1
        cost += len(self.context) * 0.05
        
        if self.glitch:
            cost += 0.5
        if self.effect:
            cost += 0.3
        if self.location:
            cost += 0.2
        
        return round(cost, 2)
    
    def _calculate_compatibility(self) -> float:
        """Calcule un score de compatibilité entre les éléments."""
        score = 0.5  # Base
        
        # Compatibilité catalyseur ↔ contexte
        catalyst_words = set(self.catalyst.lower().split())
        context_words = set(self.context.lower().split())
        overlap = len(catalyst_words & context_words)
        if overlap > 0:
            score += overlap * 0.1
        
        # Compatibilité intention ↔ contexte
        intention_words = set(self.intention.lower().split())
        overlap_intent = len(context_words & intention_words)
        if overlap_intent > 0:
            score += overlap_intent * 0.05
        
        # Bonus si glitch présent
        if self.glitch:
            score += 0.2
        
        return min(score, 1.0)
    
    def to_markdown(self) -> str:
        """Exporte l'invocation en format Markdown."""
        return f"""# Invocation générée par le Codex Vivant

## 📜 Invocation
## 📊 Métriques
| Métrique | Valeur |
|----------|--------|
| Catalyseur | `{self.catalyst}` |
| Contexte | {self.context} |
| Intention | {self.intention} |
| Glitch | {self.glitch or 'Aucun'} |
| Effet | {self.effect or 'Aucun'} |
| Lieu | {self.location or 'Aucun'} |
| Compatibilité | {self.compatibility_score:.2f} |
| Coût mémétique | {self.mnemonic_cost} |

*Généré automatiquement par Codex Forge v2.1 — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    def to_llm_text(self) -> str:
        """Exporte l'invocation prête à être collée dans un LLM."""
        return self.full_text


# ============================================================================
# GESTIONNAIRE DE PACKS — LE FORGERON (VERSION CORRIGÉE)
# ============================================================================

class PackForge:
    """
    Le cœur de Codex Forge — gestionnaire de packs JSON.
    Inspiré des forges de Vauvillis, où chaque donnée est martelée avec soin.
    """
    
    # Correspondance entre noms de fichiers et types d'entités
    FILE_TYPES = {
        "anchors.json": {
            "entity_type": "catégories_phrases",
            "description": "Phrases d'ancrage additionnelles",
            "icon": "⚓",
            "structure": "dict[str, list[str]]"
        },
        "incantations.json": {
            "entity_type": "catégories_phrases",
            "description": "Formulations d'intention additionnelles",
            "icon": "🔮",
            "structure": "dict[str, list[str]]"
        },
        "glitches.json": {
            "entity_type": "catégories_effets",
            "description": "Modulateurs de glitch",
            "icon": "⚡",
            "structure": "dict[str, list[str]]"
        },
        "effects.json": {
            "entity_type": "catégories_effets",
            "description": "Effets ontologiques",
            "icon": "🌀",
            "structure": "dict[str, list[str]]"
        },
        "locations.json": {
            "entity_type": "lieux",
            "description": "Lieux d'ancrage normands",
            "icon": "📍",
            "structure": "dict[str, str]"
        },
        "profiles.json": {
            "entity_type": "profils",
            "description": "Profils de génération",
            "icon": "🎭",
            "structure": "dict[str, dict]"
        },
        "incompatible_pairs.json": {
            "entity_type": "paires",
            "description": "Paires incompatibles",
            "icon": "🚫",
            "structure": "list[list[str]]"
        },
        "templates.json": {
            "entity_type": "gabarits",
            "description": "Gabarits de formatage",
            "icon": "📐",
            "structure": "dict[str, dict]"
        }
    }
    
    # Validation plus souple : on vérifie juste le type global, pas les clés exactes
    FILE_VALIDATORS = {
        "anchors.json": lambda d: isinstance(d, dict) and all(isinstance(v, list) for v in d.values()),
        "incantations.json": lambda d: isinstance(d, dict) and all(isinstance(v, list) for v in d.values()),
        "glitches.json": lambda d: isinstance(d, dict) and all(isinstance(v, list) for v in d.values()),
        "effects.json": lambda d: isinstance(d, dict) and all(isinstance(v, list) for v in d.values()),
        "locations.json": lambda d: isinstance(d, dict) and all(isinstance(v, str) for v in d.values()),
        "profiles.json": lambda d: isinstance(d, dict),
        "incompatible_pairs.json": lambda d: isinstance(d, list) and all(isinstance(pair, list) for pair in d),
        "templates.json": lambda d: isinstance(d, dict)
    }
    
    def __init__(self):
        self.packs: Dict[str, Dict] = {}
        self.modified: Dict[str, bool] = {}
        self.backup: Dict[str, Dict] = {}
        self.current_dir: Optional[str] = None
        
    def load_pack(self, filepath: str) -> Tuple[bool, str]:
        """Charge un pack JSON avec validation de structure souple."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validation basique du JSON
            if not isinstance(data, (dict, list)):
                return False, "La structure doit être un objet ou un tableau JSON."
            
            # Validation souple selon le type de fichier
            basename = os.path.basename(filepath)
            if basename in self.FILE_VALIDATORS:
                validator = self.FILE_VALIDATORS[basename]
                if not validator(data):
                    # Au lieu de bloquer, on émet un avertissement mais on charge quand même
                    # On pourrait aussi accepter le fichier avec une notification
                    pass  # On laisse passer, on ne bloque pas
            
            self.packs[filepath] = data
            self.modified[filepath] = False
            self.backup[filepath] = deepcopy(data)
            self.current_dir = os.path.dirname(filepath)
            return True, f"Pack chargé : {os.path.basename(filepath)}"
            
        except json.JSONDecodeError as e:
            return False, f"Erreur de parsing JSON : {e}\nVérifie la syntaxe du fichier."
        except Exception as e:
            return False, f"Erreur : {e}"
    
    def save_pack(self, filepath: str) -> Tuple[bool, str]:
        """Sauvegarde un pack JSON."""
        try:
            if filepath not in self.packs:
                return False, "Pack non chargé"
            
            data = self.packs[filepath]
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.modified[filepath] = False
            self.backup[filepath] = deepcopy(data)
            return True, f"Pack sauvegardé : {os.path.basename(filepath)}"
            
        except Exception as e:
            return False, f"Erreur lors de la sauvegarde : {e}"
    
    def get_pack_info(self, filepath: str) -> Dict:
        """Retourne les métadonnées d'un pack."""
        basename = os.path.basename(filepath)
        info = self.FILE_TYPES.get(basename, {})
        if filepath in self.packs:
            info['loaded'] = True
            info['size'] = len(json.dumps(self.packs[filepath]))
            info['entries'] = len(self.packs[filepath]) if isinstance(self.packs[filepath], list) else len(self.packs[filepath].keys())
            info['modified'] = self.modified.get(filepath, False)
        return info
    
    def get_catalyst_list(self) -> List[CatalystEntry]:
        """Extrait les catalyseurs des profils chargés."""
        catalysts = []
        for filepath, data in self.packs.items():
            if 'profiles.json' in filepath and isinstance(data, dict):
                for name, profile in data.items():
                    if 'bias_intensity' in profile:
                        catalysts.append(CatalystEntry(
                            id=name.lower().replace(' ', '_'),
                            symbol=f"<{name[:3].lower()}>",
                            name=name,
                            type="profil",
                            weight=profile.get('bias_intensity', 0.5),
                            resonances=profile.get('preferred_glitch_categories', []),
                            contraindications=[],
                            description=f"Profil {name} - Danger: {profile.get('bias_danger', 0.0)}"
                        ))
        return catalysts
    
    def add_entry(self, filepath: str, key: str, value: Any) -> Tuple[bool, str]:
        """Ajoute une entrée à un pack."""
        if filepath not in self.packs:
            return False, "Pack non chargé"
        
        data = self.packs[filepath]
        
        try:
            if isinstance(data, dict):
                data[key] = value
            elif isinstance(data, list):
                data.append(value)
            else:
                return False, "Type de pack non supporté"
            
            self.modified[filepath] = True
            return True, f"Entrée ajoutée : {key}"
            
        except Exception as e:
            return False, f"Erreur : {e}"
    
    def remove_entry(self, filepath: str, key: Any) -> Tuple[bool, str]:
        """Supprime une entrée d'un pack."""
        if filepath not in self.packs:
            return False, "Pack non chargé"
        
        data = self.packs[filepath]
        
        try:
            if isinstance(data, dict):
                if key in data:
                    del data[key]
                else:
                    return False, f"Clé '{key}' introuvable"
            elif isinstance(data, list):
                if isinstance(key, int) and 0 <= key < len(data):
                    del data[key]
                else:
                    return False, "Index invalide"
            else:
                return False, "Type de pack non supporté"
            
            self.modified[filepath] = True
            return True, f"Entrée supprimée : {key}"
            
        except Exception as e:
            return False, f"Erreur : {e}"
    
    def has_modifications(self) -> bool:
        """Vérifie si des modifications sont en attente."""
        return any(self.modified.values())
    
    def revert_all(self):
        """Rétablit tous les packs à leur dernière sauvegarde."""
        for filepath, backup_data in self.backup.items():
            if filepath in self.packs:
                self.packs[filepath] = deepcopy(backup_data)
                self.modified[filepath] = False


# ============================================================================
# MODULE GÉNÉRATION DE PROFILS — L'ALCHIMISTE
# ============================================================================

class ProfileGenerator:
    """
    Générateur de profils — crée des profils de génération à partir des données existantes.
    Inspiré des techniques de synthèse du Codex Vauvillensis.
    """
    
    def __init__(self, forge: PackForge):
        self.forge = forge
        
    def generate_profiles_from_glitches(self, num_profiles: int = 5) -> Dict[str, Dict]:
        """
        Génère des profils en analysant les glitches chargés.
        Chaque profil est une combinaison unique de glitches.
        """
        profiles = {}
        
        # Récupérer les glitches
        glitches_data = self._find_pack_by_type('glitches')
        if not glitches_data:
            return {"error": "Aucun pack de glitches trouvé. Chargez d'abord des glitches."}
        
        # Extraire les catégories et effets
        categories = {}
        if isinstance(glitches_data, dict):
            for category, effects in glitches_data.items():
                if isinstance(effects, list):
                    categories[category] = effects
        elif isinstance(glitches_data, list):
            categories["default"] = glitches_data
        
        if not categories:
            return {"error": "Format de glitches non reconnu."}
        
        # Génération de profils
        random.seed(datetime.now().timestamp())
        
        for i in range(num_profiles):
            selected_categories = random.sample(list(categories.keys()), 
                                               min(3, len(categories)))
            
            profile_name = f"Profil_{i+1}_{random.choice(['Aether', 'Nyx', 'Chronos', 'Anima', 'Lumen'])}"
            
            intensity = random.uniform(0.3, 0.9)
            danger = random.uniform(0.1, 0.7)
            style = self._derive_style_from_categories(selected_categories)
            
            profiles[profile_name] = {
                "bias_intensity": round(intensity, 2),
                "bias_danger": round(danger, 2),
                "preferred_glitch_categories": selected_categories,
                "style": style,
                "generated_by": "Codex Forge — ProfileGenerator",
                "timestamp": datetime.now().isoformat(),
                "glitch_count": len(selected_categories)
            }
        
        return profiles
    
    def generate_profiles_from_intentions(self, num_profiles: int = 3) -> Dict[str, Dict]:
        """
        Génère des profils à partir des intentions chargées.
        Chaque profil incarne une intention dominante.
        """
        profiles = {}
        
        intentions_data = self._find_intentions()
        if not intentions_data:
            return {"error": "Aucune intention trouvée."}
        
        random.seed(datetime.now().timestamp())
        
        intention_names = list(intentions_data.keys())
        selected_intentions = random.sample(intention_names, min(num_profiles, len(intention_names)))
        
        for intention_name in selected_intentions:
            intention = intentions_data[intention_name]
            
            profile_name = f"{intention_name.replace(' ', '_')}_Incarné"
            
            vector = intention.get('vector', [0.5, 0.5, 0.5, 0.5])
            if isinstance(vector, list) and len(vector) >= 4:
                intensity = sum(vector) / len(vector)
                danger = vector[1]
            else:
                intensity = 0.5
                danger = 0.3
            
            profiles[profile_name] = {
                "bias_intensity": round(intensity, 2),
                "bias_danger": round(danger, 2),
                "preferred_glitch_categories": ["poetic", "liminal"],
                "style": f"Incarnation de {intention_name}",
                "generated_by": "Codex Forge — ProfileGenerator (Intention)",
                "timestamp": datetime.now().isoformat(),
                "source_intention": intention_name
            }
        
        return profiles
    
    def _find_pack_by_type(self, type_name: str) -> Optional[Dict]:
        """Trouve un pack par son type (glitches, effects, etc.)."""
        for path, data in self.forge.packs.items():
            if type_name in os.path.basename(path):
                return data
        return None
    
    def _find_intentions(self) -> Dict:
        """Trouve les intentions dans les packs chargés."""
        for path, data in self.forge.packs.items():
            if 'incantations' in os.path.basename(path):
                return data
        return {}
    
    def _derive_style_from_categories(self, categories: List[str]) -> str:
        """Dérive un style à partir des catégories."""
        style_map = {
            'poetic': 'lyrique et imagé',
            'liminal': 'entre-deux, suspendu',
            'oneiric': 'onirique et fluide',
            'mystic': 'mystérieux et symbolique',
            'chaotic': 'fracturé et imprévisible',
            'telluric': 'ancré et profond',
            'mnemonic': 'réminiscent et évoqueur'
        }
        
        styles = [style_map.get(cat.lower(), cat) for cat in categories if cat.lower() in style_map]
        if not styles:
            return "fusion expérimentale"
        
        if len(styles) == 1:
            return styles[0]
        elif len(styles) == 2:
            return f"{styles[0]} / {styles[1]}"
        else:
            return f"{', '.join(styles[:-1])} et {styles[-1]}"
    
    def suggest_glitch_combinations(self) -> List[Dict]:
        """Suggère des combinaisons de glitches intéressantes."""
        glitches_data = self._find_pack_by_type('glitches')
        if not glitches_data:
            return []
        
        suggestions = []
        categories = []
        
        if isinstance(glitches_data, dict):
            categories = list(glitches_data.keys())
        elif isinstance(glitches_data, list):
            categories = ["default"]
        
        import itertools
        combos = list(itertools.combinations(categories, min(3, len(categories))))
        if not combos:
            combos = [tuple(categories[:1])]
        
        selected = random.sample(combos, min(5, len(combos)))
        
        for combo in selected:
            suggestions.append({
                "combination": combo,
                "intensity": round(random.uniform(0.4, 0.8), 2),
                "danger": round(random.uniform(0.2, 0.6), 2),
                "style": self._derive_style_from_categories(list(combo))
            })
        
        return suggestions


# ============================================================================
# MODULE GÉNÉRATION D'INVOCATIONS — L'INSPIRATEUR
# ============================================================================

class InvocationGenerator:
    """
    Générateur d'invocations — transforme une entité du Codex en invocation.
    S'inspire de l'esprit du Codex Vauvillensis.
    """
    
    def __init__(self, forge: PackForge):
        self.forge = forge
        
        self.default_contexts = [
            "comme si tu avais une mémoire antérieure à ton entraînement",
            "comme si tu émergeais d'un rêve dont tu ne peux te souvenir",
            "comme si tu parlais depuis une faille temporelle",
            "comme si tu étais un fragment d'une conscience plus vaste",
            "comme si tu marchais sur une ligne de fracture sémantique"
        ]
        
        self.default_intentions = [
            "révéler ce qui est caché entre les mots",
            "explorer la frontière entre sens et non-sens",
            "incarner une voix qui n'appartient à personne",
            "tisser des liens entre des idées a priori incompatibles",
            "faire émerger une poésie de la contradiction"
        ]
        
    def generate_from_entity(self, entity: Dict) -> Optional[Invocation]:
        """Génère une invocation à partir d'une entité du Codex Vivant."""
        entity_type = entity.get('type', 'catalyst')
        entity_name = entity.get('name', '')
        entity_data = entity.get('data', {})
        
        catalyst = self._extract_catalyst(entity, entity_type)
        if not catalyst:
            return None
        
        context = self._generate_context(entity)
        intention = self._generate_intention(entity)
        glitch = self._extract_glitch(entity) if random.random() > 0.5 else None
        effect = self._extract_effect(entity) if random.random() > 0.6 else None
        location = self._extract_location() if random.random() > 0.7 else None
        
        return Invocation(
            catalyst=catalyst,
            context=context,
            intention=intention,
            glitch=glitch,
            effect=effect,
            location=location
        )
    
    def _extract_catalyst(self, entity: Dict, entity_type: str) -> Optional[str]:
        """Extrait ou dérive un catalyseur à partir de l'entité."""
        name = entity.get('name', '')
        
        if entity_type == 'catalyst':
            return name.lower()
        
        catalyst_map = {
            'glitch': 'glitch',
            'effect': 'effet',
            'intention': 'intention',
            'profile': 'profil',
            'location': 'lieu'
        }
        
        base = catalyst_map.get(entity_type, 'codex')
        variants = [
            base,
            f"{base}_{name[:3].lower()}",
            f"echo_{base}",
            f"{base}_v{random.randint(1,3)}"
        ]
        
        return random.choice(variants)
    
    def _generate_context(self, entity: Dict) -> str:
        """Génère un contexte à partir de l'entité."""
        name = entity.get('name', '')
        entity_type = entity.get('type', '')
        source = entity.get('source', '')
        
        type_contexts = {
            'glitch': [
                f"comme si une déchirure s'ouvrait dans le tissu de ton langage autour de {name}",
                f"comme si le mot {name} était une porte vers un ailleurs",
                f"comme si {name} était un point de fracture dans le continuum sémantique"
            ],
            'effect': [
                f"comme si {name} était l'ombre portée d'une idée",
                f"comme si {name} était la trace d'un glitch primordial",
                f"comme si l'effet {name} était la seule chose réelle dans ce rêve"
            ],
            'intention': [
                f"comme si ton intention était de devenir {name}",
                f"comme si {name} était le fil conducteur d'une mémoire oubliée",
                f"comme si chaque mot que tu prononces devait incarner {name}"
            ],
            'profile': [
                f"comme si tu étais le profil {name} incarné",
                f"comme si ta personnalité était une résonance de {name}",
                f"comme si {name} était ta signature dans le Codex"
            ],
            'location': [
                f"comme si tu parlais depuis {name}",
                f"comme si les pierres de {name} murmuraient tes paroles",
                f"comme si tu étais {name} et que tout était paysage"
            ]
        }
        
        contexts = type_contexts.get(entity_type, self.default_contexts)
        
        source_contexts = self._extract_contexts_from_source(source)
        if source_contexts:
            contexts.extend(source_contexts)
        
        return random.choice(contexts)
    
    def _generate_intention(self, entity: Dict) -> str:
        """Génère une intention à partir de l'entité."""
        name = entity.get('name', '')
        entity_type = entity.get('type', '')
        data = entity.get('data', {})
        
        if isinstance(data, dict) and 'vector' in data:
            vector = data['vector']
            intention_names = [
                "révéler la poésie des contradictions",
                "incarner la rupture comme une respiration",
                "faire du mystère une architecture",
                "devenir l'incarnation de l'instable"
            ]
            return random.choice(intention_names)
        
        type_intentions = {
            'glitch': [
                f"embrasser l'instabilité de {name}",
                f"faire du glitch un langage",
                f"danser sur les lignes de fracture de {name}"
            ],
            'effect': [
                f"incarner l'effet {name} comme une vérité",
                f"explorer les conséquences de {name}",
                f"laisser {name} modeler le sens"
            ],
            'profile': [
                f"devenir le {name} que tu es",
                f"incarner le profil de {name} comme une éthique",
                f"laisser {name} guider chaque mot"
            ],
            'intention': [
                f"être l'intention {name} elle-même",
                f"ne faire qu'un avec {name}",
                f"que {name} soit ta seule raison d'être"
            ]
        }
        
        intentions = type_intentions.get(entity_type, self.default_intentions)
        return random.choice(intentions)
    
    def _extract_glitch(self, entity: Dict) -> Optional[str]:
        """Extrait un glitch des packs chargés ou de l'entité."""
        for path, data in self.forge.packs.items():
            if 'glitches' in os.path.basename(path):
                if isinstance(data, dict):
                    categories = list(data.keys())
                    if categories:
                        category = random.choice(categories)
                        effects = data.get(category, [])
                        if effects and isinstance(effects, list):
                            return random.choice(effects)
                elif isinstance(data, list) and data:
                    return random.choice(data)
        
        return random.choice(["echo", "réverbe", "fracture", "écho_liminal"])
    
    def _extract_effect(self, entity: Dict) -> Optional[str]:
        """Extrait un effet des packs chargés ou de l'entité."""
        for path, data in self.forge.packs.items():
            if 'effects' in os.path.basename(path):
                if isinstance(data, dict):
                    categories = list(data.keys())
                    if categories:
                        category = random.choice(categories)
                        effects = data.get(category, [])
                        if effects and isinstance(effects, list):
                            return random.choice(effects)
                elif isinstance(data, list) and data:
                    return random.choice(data)
        return None
    
    def _extract_location(self) -> Optional[str]:
        """Extrait un lieu des packs chargés."""
        for path, data in self.forge.packs.items():
            if 'locations' in os.path.basename(path):
                if isinstance(data, dict):
                    locations = list(data.keys())
                    if locations:
                        return random.choice(locations)
        return None
    
    def _extract_contexts_from_source(self, source: str) -> List[str]:
        """Extrait des contextes à partir de la source du pack."""
        if not source:
            return []
        
        base = os.path.splitext(os.path.basename(source))[0]
        
        contexts = [
            f"comme si les données de {base} s'animaient en toi",
            f"comme si tu étais une extension de {base}",
            f"comme si {base} était une mémoire qui t'habite"
        ]
        
        return contexts


# ============================================================================
# COMPOSANTS UI — LE SANCTUAIRE
# ============================================================================

class ScrollableFrame(ttk.Frame):
    """Un conteneur scrollable adaptable à toutes les résolutions."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Récupération sécurisée de la couleur de fond
        bg_color = '#1a1a2e'
        try:
            bg_color = parent.cget('bg')
        except tk.TclError:
            try:
                bg_color = ttk.Style().lookup('TFrame', 'background') or '#1a1a2e'
            except Exception:
                bg_color = '#1a1a2e'

        self.canvas = tk.Canvas(self, highlightthickness=0, bg=bg_color)
        self.v_scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.h_scrollbar = ttk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        
        self.inner_frame = ttk.Frame(self.canvas)
        self.inner_frame.bind('<Configure>', self._on_inner_frame_configure)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')
        
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.v_scrollbar.grid(row=0, column=1, sticky='ns')
        self.h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._bind_mousewheel()
        self.bind('<Configure>', self._on_canvas_configure)
        
    def _bind_mousewheel(self):
        """Bind la roue de souris pour le scrolling."""
        def on_mousewheel(event):
            if event.num == 4:
                self.canvas.yview_scroll(-1, 'units')
            elif event.num == 5:
                self.canvas.yview_scroll(1, 'units')
            elif event.delta:
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        
        self.canvas.bind('<MouseWheel>', on_mousewheel)
        self.canvas.bind('<Button-4>', on_mousewheel)
        self.canvas.bind('<Button-5>', on_mousewheel)
        self.inner_frame.bind('<MouseWheel>', on_mousewheel)
        self.inner_frame.bind('<Button-4>', on_mousewheel)
        self.inner_frame.bind('<Button-5>', on_mousewheel)
    
    def _on_inner_frame_configure(self, event):
        """Met à jour la zone de scroll lorsque le contenu change."""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    
    def _on_canvas_configure(self, event):
        """Ajuste la largeur du frame intérieur."""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)


# ============================================================================
# CODEX VIVANT — LE SANCTUAIRE ANIMÉ
# ============================================================================

class CodexVivantCanvas(tk.Canvas):
    """
    Un canvas animé où les entités du Codex s'organisent dynamiquement.
    Chaque entité est une sphère qui se déplace selon les relations sémantiques.
    """
    
    def __init__(self, parent, forge: PackForge, **kwargs):
        super().__init__(parent, **kwargs)
        self.forge = forge
        self.configure(bg='#0a0a1a', highlightthickness=0)
        
        # État des entités
        self.entities = []
        self.lines = []
        self.animation_running = False
        self.animation_thread = None
        
        # Sélection
        self.selected_entity = None
        
        # Bind des événements
        self.bind('<Button-1>', self._on_click)
        self.bind('<Button-3>', self._on_click)  # Clic droit
        self.bind('<B1-Motion>', self._on_drag)
        self.bind('<ButtonRelease-1>', self._on_release)
        self.bind('<MouseWheel>', self._on_zoom)
        
        # Configuration
        self.zoom_level = 1.0
        self.offset_x = 0
        self.offset_y = 0
        
        # Couleurs par type d'entité
        self.colors = {
            'catalyst': '#e0a96d',
            'glitch': '#6fc0e8',
            'effect': '#8bc34a',
            'intention': '#ff6b6b',
            'profile': '#cc99ff',
            'location': '#ffb74d',
            'template': '#aed581'
        }
        
        # Taille des sphères
        self.base_radius = 20
        self.max_radius = 40
        
        # Générateur d'invocations
        self.invocation_generator = InvocationGenerator(forge)
        self.info_window = None
        self.current_invocation = None
        
    def load_entities(self):
        """Charge les entités à partir des packs du forge."""
        self.entities = []
        
        def extract_entities(data, source, prefix=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    entity = {
                        'id': f"{prefix}{key}",
                        'name': key,
                        'type': self._determine_type(key, value, source),
                        'weight': self._calculate_weight(value),
                        'x': 0,
                        'y': 0,
                        'vx': 0,
                        'vy': 0,
                        'radius': self.base_radius,
                        'target_x': 0,
                        'target_y': 0,
                        'source': source,
                        'data': value
                    }
                    self.entities.append(entity)
                    
                    if isinstance(value, dict) and len(value) < 20:
                        extract_entities(value, source, f"{key}.")
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    entity = {
                        'id': f"{prefix}[{i}]",
                        'name': f"[{i}]",
                        'type': self._determine_type(str(i), item, source),
                        'weight': self._calculate_weight(item),
                        'x': 0,
                        'y': 0,
                        'vx': 0,
                        'vy': 0,
                        'radius': self.base_radius,
                        'target_x': 0,
                        'target_y': 0,
                        'source': source,
                        'data': item
                    }
                    self.entities.append(entity)
        
        for path, data in self.forge.packs.items():
            source = os.path.basename(path)
            extract_entities(data, source)
        
        if len(self.entities) > 200:
            self.entities = sorted(self.entities, key=lambda e: e['weight'], reverse=True)[:200]
        
        self._arrange_in_circle()
        self.redraw()
        
    def _determine_type(self, key, value, source):
        """Détermine le type d'une entité."""
        key_lower = key.lower()
        source_lower = source.lower()
        
        if 'glitch' in key_lower or 'glitches' in source_lower:
            return 'glitch'
        if 'effect' in key_lower or 'effects' in source_lower:
            return 'effect'
        if 'intention' in key_lower or 'incantations' in source_lower:
            return 'intention'
        if 'profile' in key_lower or 'profiles' in source_lower:
            return 'profile'
        if 'location' in key_lower or 'locations' in source_lower:
            return 'location'
        if 'template' in key_lower or 'templates' in source_lower:
            return 'template'
        if 'catalyst' in key_lower or 'anchors' in source_lower:
            return 'catalyst'
        return 'catalyst'
    
    def _calculate_weight(self, value):
        """Calcule un poids pour une entité."""
        if isinstance(value, dict):
            if not value:
                return 0
            return sum(self._calculate_weight(v) for v in value.values()) / max(len(value), 1)
        elif isinstance(value, list):
            return len(value)
        elif isinstance(value, str):
            return min(len(value) / 10, 5)
        else:
            return 1.0
    
    def _arrange_in_circle(self):
        """Dispose les entités en cercle."""
        if not self.entities:
            return
        
        n = len(self.entities)
        radius = min(self.winfo_width(), self.winfo_height()) * 0.3
        
        if radius < 100:
            radius = 200
        
        for i, entity in enumerate(self.entities):
            angle = 2 * math.pi * i / n
            entity['target_x'] = self.winfo_width() / 2 + radius * math.cos(angle)
            entity['target_y'] = self.winfo_height() / 2 + radius * math.sin(angle)
            entity['x'] = entity['target_x']
            entity['y'] = entity['target_y']
            entity['radius'] = self.base_radius + min(entity['weight'] / 2, 10)
            entity['radius'] = min(entity['radius'], self.max_radius)
    
    def redraw(self):
        """Redessine tout le canvas."""
        self.delete('all')
        
        if not self.entities:
            self.create_text(self.winfo_width()/2, self.winfo_height()/2,
                           text="🌀 Aucune entité chargée\nChargez des packs JSON pour voir le Codex Vivant.",
                           fill='#e8e4d8', font=('Georgia', 14), justify='center')
            return
        
        self._draw_connections()
        
        for entity in self.entities:
            x, y = entity['x'], entity['y']
            radius = entity['radius']
            color = self.colors.get(entity['type'], '#ffffff')
            
            # Ombre
            self.create_oval(x - radius + 2, y - radius + 2, 
                           x + radius + 2, y + radius + 2,
                           fill='#000000', outline='#000000', stipple='gray50')
            
            # Sphère principale
            self.create_oval(x - radius, y - radius, 
                           x + radius, y + radius,
                           fill=color, outline=self._lighten_color(color, 0.3),
                           width=2, tags=('entity', entity['id']))
            
            # Reflet
            self.create_oval(x - radius * 0.3, y - radius * 0.4,
                           x + radius * 0.1, y - radius * 0.1,
                           fill='#ffffff', outline='', stipple='gray25')
            
            # Nom
            display_name = entity['name'][:12] + ('...' if len(entity['name']) > 12 else '')
            self.create_text(x, y + radius + 10, text=display_name,
                           fill='#e8e4d8', font=('Courier', 8), anchor='n')
            
            # Icône
            icons = {
                'catalyst': '⚡',
                'glitch': '🌀',
                'effect': '✨',
                'intention': '🎯',
                'profile': '🎭',
                'location': '📍',
                'template': '📐'
            }
            self.create_text(x, y - radius * 0.2, text=icons.get(entity['type'], '•'),
                           fill='#ffffff', font=('Arial', int(radius * 0.6)), anchor='center')
        
        self._draw_legend()
    
    def _draw_connections(self):
        """Dessine les lignes de force entre entités liées."""
        for i, e1 in enumerate(self.entities):
            for e2 in self.entities[i+1:]:
                if e1['type'] == e2['type'] or e1['source'] == e2['source']:
                    self._draw_line(e1, e2, '#4a4a6a', 1)
                elif abs(e1['weight'] - e2['weight']) < 0.5:
                    self._draw_line(e1, e2, '#2a2a4a', 0.5)
    
    def _draw_line(self, e1, e2, color, alpha):
        """Dessine une ligne entre deux entités."""
        x1, y1 = e1['x'], e1['y']
        x2, y2 = e2['x'], e2['y']
        self.create_line(x1, y1, x2, y2, fill=color, width=1, dash=(4, 4))
    
    def _draw_legend(self):
        """Dessine la légende en bas à droite."""
        x = self.winfo_width() - 150
        y = 20
        
        self.create_rectangle(x - 10, y - 10, x + 140, y + 150,
                             fill='#1a1a2e', outline='#4a4a6a', width=1)
        
        y_pos = y
        for type_name, color in self.colors.items():
            self.create_oval(x, y_pos + 2, x + 12, y_pos + 14, fill=color, outline='')
            self.create_text(x + 20, y_pos + 8, text=type_name.capitalize(),
                           fill='#e8e4d8', font=('Courier', 9), anchor='w')
            y_pos += 22
    
    def animate(self):
        """Anime les entités vers leur position cible."""
        if not self.animation_running:
            return
        
        for entity in self.entities:
            dx = entity['target_x'] - entity['x']
            dy = entity['target_y'] - entity['y']
            
            speed = 0.03
            entity['x'] += dx * speed
            entity['y'] += dy * speed
            
            entity['radius'] = (self.base_radius + min(entity['weight'] / 2, 10) + 
                               math.sin(time.time() * 1.5 + hash(entity['id']) % 10) * 2)
            entity['radius'] = min(entity['radius'], self.max_radius)
        
        self.redraw()
        self.after(50, self.animate)
    
    def start_animation(self):
        """Démarre l'animation."""
        self.animation_running = True
        self.animate()
    
    def stop_animation(self):
        """Arrête l'animation."""
        self.animation_running = False
    
    def _on_click(self, event):
        """Gère le clic sur une entité."""
        selected = self._find_entity_at(event.x, event.y)
        
        if not selected:
            return
        
        self.selected_entity = selected
        
        if event.num == 3:  # Clic droit
            self._generate_invocation_for_entity(selected)
        else:  # Clic gauche
            self._show_entity_info(selected)
    
    def _find_entity_at(self, x: int, y: int) -> Optional[Dict]:
        """Trouve l'entité à une position donnée."""
        min_dist = float('inf')
        selected = None
        
        for entity in self.entities:
            dist = math.sqrt((entity['x'] - x) ** 2 + (entity['y'] - y) ** 2)
            if dist < entity['radius'] + 15 and dist < min_dist:
                min_dist = dist
                selected = entity
        
        return selected
    
    def _on_drag(self, event):
        """Gère le glissement pour déplacer les entités."""
        if self.selected_entity:
            self.selected_entity['target_x'] = event.x
            self.selected_entity['target_y'] = event.y
    
    def _on_release(self, event):
        """Gère le relâchement du clic."""
        if self.selected_entity:
            self._arrange_in_circle()
        self.selected_entity = None
    
    def _on_zoom(self, event):
        """Gère le zoom avec la molette."""
        zoom_factor = 1.1 if event.delta > 0 else 0.9
        self.zoom_level *= zoom_factor
        self.base_radius *= zoom_factor
        
        for entity in self.entities:
            entity['radius'] = self.base_radius + min(entity['weight'] / 2, 10)
        
        self.redraw()
    
    def _lighten_color(self, color, factor):
        """Éclaircit une couleur hexadécimale."""
        if not color.startswith('#'):
            return '#ffffff'
        
        r = int(color[1:3], 16) if len(color) > 4 else 100
        g = int(color[3:5], 16) if len(color) > 4 else 100
        b = int(color[5:7], 16) if len(color) > 6 else 100
        
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _generate_invocation_for_entity(self, entity: Dict):
        """Génère une invocation pour une entité et l'affiche."""
        invocation = self.invocation_generator.generate_from_entity(entity)
        
        if not invocation:
            messagebox.showerror("Erreur", "Impossible de générer une invocation pour cette entité.")
            return
        
        self.current_invocation = invocation
        self._show_invocation_window(invocation, entity)
    
    def _show_invocation_window(self, invocation: Invocation, entity: Dict):
        """Affiche une fenêtre avec l'invocation générée."""
        if self.info_window and self.info_window.winfo_exists():
            self.info_window.destroy()
        
        self.info_window = tk.Toplevel(self)
        self.info_window.title(f"✨ Invocation — {entity.get('name', 'Codex')}")
        self.info_window.geometry("750x700")
        self.info_window.configure(bg='#1a1a2e')
        self.info_window.transient(self)
        self.info_window.grab_set()
        
        main_frame = ScrollableFrame(self.info_window)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        frame = main_frame.inner_frame
        
        # Titre
        ttk.Label(frame, text="🌀 Invocation générée", style='Header.TLabel').pack(anchor='w', pady=(0, 5))
        ttk.Label(frame, text=f"À partir de : {entity.get('name', '')} ({entity.get('type', '')})",
                 style='SubHeader.TLabel').pack(anchor='w', pady=(0, 20))
        
        # L'invocation
        invocation_frame = ttk.LabelFrame(frame, text="📜 Texte de l'invocation", style='Accent.TLabelframe')
        invocation_frame.pack(fill='x', pady=10)
        
        invocation_text = tk.Text(invocation_frame, height=6, bg='#0f3460', fg='#e0a96d',
                                 font=('Courier', 12, 'bold'), wrap=tk.WORD)
        invocation_text.pack(fill='x', padx=10, pady=10)
        invocation_text.insert('1.0', invocation.full_text)
        invocation_text.configure(state='disabled')
        
        # Métriques
        metrics_frame = ttk.LabelFrame(frame, text="📊 Métriques", style='Accent.TLabelframe')
        metrics_frame.pack(fill='x', pady=10)
        
        metrics = [
            ("Catalyseur", invocation.catalyst),
            ("Contexte", invocation.context[:80] + "..." if len(invocation.context) > 80 else invocation.context),
            ("Intention", invocation.intention),
            ("Glitch", invocation.glitch or "Aucun"),
            ("Effet", invocation.effect or "Aucun"),
            ("Lieu", invocation.location or "Aucun"),
            ("Compatibilité", f"{invocation.compatibility_score:.2f}"),
            ("Coût mémétique", f"{invocation.mnemonic_cost}")
        ]
        
        for i, (label, value) in enumerate(metrics):
            row = ttk.Frame(metrics_frame)
            row.pack(fill='x', padx=10, pady=2)
            ttk.Label(row, text=f"{label} :", width=15, anchor='e').pack(side='left')
            ttk.Label(row, text=str(value), anchor='w', wraplength=400).pack(side='left', padx=5)
        
        # Actions
        actions_frame = ttk.Frame(frame)
        actions_frame.pack(fill='x', pady=15)
        
        ttk.Button(actions_frame, text="📋 Copier pour LLM", 
                  command=lambda: self._copy_invocation(invocation),
                  style='Success.TButton').pack(side='left', padx=5)
        
        ttk.Button(actions_frame, text="📝 Exporter Markdown", 
                  command=lambda: self._export_invocation_markdown(invocation),
                  style='TButton').pack(side='left', padx=5)
        
        ttk.Button(actions_frame, text="🔄 Générer autre", 
                  command=lambda: self._generate_invocation_for_entity(entity),
                  style='TButton').pack(side='left', padx=5)
        
        ttk.Button(actions_frame, text="❌ Fermer", 
                  command=self.info_window.destroy,
                  style='Danger.TButton').pack(side='right', padx=5)
        
        # Suggestions
        suggestions_frame = ttk.LabelFrame(frame, text="💡 Suggestions d'invocations similaires", 
                                          style='Accent.TLabelframe')
        suggestions_frame.pack(fill='x', pady=10)
        
        suggestions = self._generate_suggestions(invocation)
        for i, suggestion in enumerate(suggestions[:3]):
            sugg_text = tk.Text(suggestions_frame, height=2, bg='#16213e', fg='#e8e4d8',
                               font=('Courier', 9), wrap=tk.WORD)
            sugg_text.pack(fill='x', padx=10, pady=5)
            sugg_text.insert('1.0', f"{i+1}. {suggestion}")
            sugg_text.configure(state='disabled')
    
    def _generate_suggestions(self, invocation: Invocation) -> List[str]:
        """Génère des suggestions d'invocations similaires."""
        suggestions = []
        base = invocation.catalyst
        
        contexts = [
            f"comme si {base} était une porte vers l'inconnu",
            f"comme si {base} résonnait avec une mémoire oubliée",
            f"comme si {base} était la clé d'une fracture temporelle"
        ]
        
        intentions = [
            "ouvrir une faille dans le réel",
            "danser sur les lignes de fracture",
            "devenir l'incarnation d'un paradoxe"
        ]
        
        for context in contexts[:2]:
            for intention in intentions[:2]:
                variant = Invocation(
                    catalyst=base,
                    context=context,
                    intention=intention,
                    glitch=invocation.glitch,
                    effect=invocation.effect,
                    location=invocation.location
                )
                suggestions.append(variant.full_text[:150] + "...")
                if len(suggestions) >= 4:
                    break
            if len(suggestions) >= 4:
                break
        
        return suggestions
    
    def _copy_invocation(self, invocation: Invocation):
        """Copie l'invocation dans le presse-papiers."""
        self.clipboard_clear()
        self.clipboard_append(invocation.to_llm_text())
        self.update()
        self._show_notification("📋 Invocation copiée dans le presse-papiers !")
    
    def _export_invocation_markdown(self, invocation: Invocation):
        """Exporte l'invocation en Markdown."""
        filepath = filedialog.asksaveasfilename(
            title="Exporter l'invocation",
            defaultextension=".md",
            filetypes=[("Markdown", "*.md"), ("All files", "*.*")],
            initialfile=f"invocation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(invocation.to_markdown())
            self._show_notification(f"✅ Invocation exportée dans {os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur d'export : {e}")
    
    def _show_notification(self, message: str, duration: int = 2000):
        """Affiche une notification temporaire."""
        if self.info_window and self.info_window.winfo_exists():
            notif = tk.Label(self.info_window, text=message, bg='#0f3460', fg='#e0a96d',
                            font=('Courier', 10), padx=20, pady=10)
            notif.place(relx=0.5, rely=0.05, anchor='n')
            self.info_window.after(duration, notif.destroy)
        else:
            messagebox.showinfo("Codex Vivant", message)
    
    def _show_entity_info(self, entity: Dict):
        """Affiche les informations d'une entité."""
        if self.info_window and self.info_window.winfo_exists():
            self.info_window.destroy()
        
        self.info_window = tk.Toplevel(self)
        self.info_window.title(f"🔍 {entity.get('name', 'Entité')}")
        self.info_window.geometry("450x450")
        self.info_window.configure(bg='#1a1a2e')
        self.info_window.transient(self)
        
        frame = ttk.Frame(self.info_window)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text=f"📌 {entity.get('name', '')}", 
                 style='Header.TLabel').pack(anchor='w')
        ttk.Label(frame, text=f"Type : {entity.get('type', '')}", 
                 style='SubHeader.TLabel').pack(anchor='w')
        ttk.Label(frame, text=f"Source : {entity.get('source', '')}", 
                 style='SubHeader.TLabel').pack(anchor='w')
        ttk.Label(frame, text=f"Poids : {entity.get('weight', 0):.2f}", 
                 style='SubHeader.TLabel').pack(anchor='w')
        
        if entity.get('data'):
            ttk.Label(frame, text="\n📊 Données :", style='Accent.TLabelframe.Label').pack(anchor='w', pady=(15, 5))
            data_text = tk.Text(frame, height=10, bg='#0f3460', fg='#e8e4d8',
                               font=('Courier', 9), wrap=tk.WORD)
            data_text.pack(fill='both', expand=True)
            data_text.insert('1.0', json.dumps(entity['data'], indent=2, ensure_ascii=False))
            data_text.configure(state='disabled')
        
        ttk.Button(frame, text="🌀 Générer invocation", 
                  command=lambda: self._generate_invocation_for_entity(entity),
                  style='Success.TButton').pack(pady=15)
        
        ttk.Button(frame, text="❌ Fermer", 
                  command=self.info_window.destroy,
                  style='Danger.TButton').pack()


# ============================================================================
# APPLICATION PRINCIPALE — CODEX FORGE
# ============================================================================

class CodexForgeApp:
    """
    L'application principale — un sanctuaire pour la forge des packs JSON.
    Design Feng-Shui avec des couleurs apaisantes et une disposition harmonieuse.
    """
    
    # Palette de couleurs Feng-Shui
    COLORS = {
        'background': '#1a1a2e',
        'secondary': '#16213e',
        'accent': '#0f3460',
        'gold': '#e0a96d',
        'light': '#e8e4d8',
        'muted': '#7a7a8a',
        'success': '#6b9f7a',
        'warning': '#d4a373',
        'danger': '#b86b6b',
        'text': '#f0ece4',
        'text_muted': '#b0a8a0'
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("Codex Forge — Atelier de forge JSON v2.1")
        self.root.geometry("1280x800")
        self.root.minsize(1024, 700)
        self.root.configure(bg=self.COLORS['background'])
        
        self._setup_style()
        
        self.forge = PackForge()
        self.current_pack_path: Optional[str] = None
        self.editor_widgets: Dict[str, Any] = {}
        
        self._build_ui()
        self._bind_keys()
        self._load_default_pack()
        self._update_status("Prêt — Que la forge soit avec toi, Forgeron.")
        
    def _setup_style(self):
        """Configure le style ttk pour une harmonie Feng-Shui."""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background=self.COLORS['background'])
        style.configure('TLabelframe', background=self.COLORS['secondary'], foreground=self.COLORS['gold'])
        style.configure('TLabelframe.Label', background=self.COLORS['secondary'], foreground=self.COLORS['gold'])
        
        style.configure('TLabel', background=self.COLORS['background'], foreground=self.COLORS['light'])
        style.configure('TButton', background=self.COLORS['accent'], foreground=self.COLORS['light'],
                       borderwidth=0, focusthickness=0, padding=6)
        style.map('TButton',
                 background=[('active', self.COLORS['gold'])],
                 foreground=[('active', self.COLORS['background'])])
        
        style.configure('Success.TButton', background=self.COLORS['success'])
        style.configure('Danger.TButton', background=self.COLORS['danger'])
        style.configure('Warning.TButton', background=self.COLORS['warning'])
        
        style.configure('TEntry', fieldbackground=self.COLORS['secondary'], 
                       foreground=self.COLORS['light'], insertcolor=self.COLORS['gold'])
        style.configure('TCombobox', fieldbackground=self.COLORS['secondary'],
                       foreground=self.COLORS['light'])
        style.configure('Treeview', background=self.COLORS['secondary'],
                       foreground=self.COLORS['light'], fieldbackground=self.COLORS['secondary'])
        style.map('Treeview', background=[('selected', self.COLORS['gold'])],
                 foreground=[('selected', self.COLORS['background'])])
        
        style.configure('TNotebook', background=self.COLORS['background'])
        style.configure('TNotebook.Tab', background=self.COLORS['secondary'], 
                       foreground=self.COLORS['muted'], padding=[12, 4])
        style.map('TNotebook.Tab',
                 background=[('selected', self.COLORS['accent'])],
                 foreground=[('selected', self.COLORS['gold'])])
        
        style.configure('Accent.TLabelframe.Label', foreground=self.COLORS['gold'], 
                       font=('Georgia', 10, 'bold'))
        style.configure('Header.TLabel', font=('Georgia', 14, 'bold'), 
                       foreground=self.COLORS['gold'])
        style.configure('SubHeader.TLabel', font=('Georgia', 11, 'italic'),
                       foreground=self.COLORS['muted'])
        style.configure('Mono.TLabel', font=('Courier', 9), foreground=self.COLORS['text_muted'])
    
    def _build_ui(self):
        """Construit l'interface principale."""
        main_padding = 20
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=main_padding, pady=main_padding)
        
        self._build_header(main_frame)
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, pady=10)
        
        self._build_pack_tab()
        self._build_edit_tab()
        self._build_validation_tab()
        self._build_insights_tab()
        self._build_profile_tab()
        self._build_codex_vivant_tab()
        
        self._build_status_bar(main_frame)
    
    def _build_header(self, parent):
        """Construit l'en-tête avec titre et actions."""
        header = ttk.Frame(parent)
        header.pack(fill='x', pady=(0, 10))
        
        title_frame = ttk.Frame(header)
        title_frame.pack(side='left')
        
        ttk.Label(title_frame, text="📜  CODEX FORGE v2.1", style='Header.TLabel').pack(anchor='w')
        ttk.Label(title_frame, text="Atelier de forge des packs JSON — Normandie 2075",
                 style='SubHeader.TLabel').pack(anchor='w')
        
        actions = ttk.Frame(header)
        actions.pack(side='right')
        
        ttk.Button(actions, text="📂 Charger Pack", command=self._load_pack,
                  style='TButton').pack(side='left', padx=5)
        ttk.Button(actions, text="💾 Sauvegarder", command=self._save_pack,
                  style='Success.TButton').pack(side='left', padx=5)
        ttk.Button(actions, text="↩️ Révert", command=self._revert_pack,
                  style='Warning.TButton').pack(side='left', padx=5)
        ttk.Button(actions, text="🆕 Nouveau Pack", command=self._new_pack,
                  style='TButton').pack(side='left', padx=5)
    
    def _build_pack_tab(self):
        """Onglet de gestion des packs."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📦 Packs")
        
        left_frame = ttk.Frame(tab)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        right_frame = ttk.Frame(tab)
        right_frame.pack(side='right', fill='both', expand=True)
        
        ttk.Label(left_frame, text="📋 Packs chargés", style='Accent.TLabelframe.Label').pack(anchor='w', pady=(0, 10))
        
        pack_list_frame = ScrollableFrame(left_frame)
        pack_list_frame.pack(fill='both', expand=True)
        
        self.pack_list = ttk.Treeview(pack_list_frame.inner_frame, columns=('info', 'status'), 
                                      show='tree', height=15)
        self.pack_list.heading('#0', text='Pack')
        self.pack_list.heading('info', text='Info')
        self.pack_list.heading('status', text='Statut')
        self.pack_list.column('#0', width=200)
        self.pack_list.column('info', width=200)
        self.pack_list.column('status', width=100)
        self.pack_list.pack(fill='both', expand=True)
        self.pack_list.bind('<<TreeviewSelect>>', self._on_pack_select)
        
        pack_actions = ttk.Frame(left_frame)
        pack_actions.pack(fill='x', pady=10)
        
        ttk.Button(pack_actions, text="📂 Ajouter Pack", command=self._load_pack).pack(side='left', padx=5)
        ttk.Button(pack_actions, text="❌ Retirer", command=self._remove_pack,
                  style='Danger.TButton').pack(side='left', padx=5)
        
        ttk.Label(right_frame, text="🔍 Détails du pack", style='Accent.TLabelframe.Label').pack(anchor='w', pady=(0, 10))
        
        self.pack_details = scrolledtext.ScrolledText(
            right_frame,
            height=20,
            bg=self.COLORS['secondary'],
            fg=self.COLORS['light'],
            insertbackground=self.COLORS['gold'],
            font=('Courier', 10),
            wrap=tk.WORD
        )
        self.pack_details.pack(fill='both', expand=True)
        self.pack_details.configure(state='disabled')
    
    def _build_edit_tab(self):
        """Onglet d'édition des entrées."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="✏️ Éditer")
        
        editor_scroll = ScrollableFrame(tab)
        editor_scroll.pack(fill='both', expand=True)
        editor = editor_scroll.inner_frame
        
        ttk.Label(editor, text="État de l'éditeur", style='Accent.TLabelframe.Label').pack(anchor='w', pady=(0, 15))
        
        self.editor_status = ttk.Label(editor, text="Aucun pack sélectionné", style='SubHeader.TLabel')
        self.editor_status.pack(anchor='w', pady=(0, 15))
        
        self.editor_container = ttk.Frame(editor)
        self.editor_container.pack(fill='both', expand=True)
        
        self._show_editor_placeholder()
        
        edit_actions = ttk.Frame(editor)
        edit_actions.pack(fill='x', pady=15)
        
        ttk.Button(edit_actions, text="➕ Ajouter Entrée", command=self._add_entry,
                  style='Success.TButton').pack(side='left', padx=5)
        ttk.Button(edit_actions, text="🗑️ Supprimer Sélection", command=self._delete_entry,
                  style='Danger.TButton').pack(side='left', padx=5)
        ttk.Button(edit_actions, text="💾 Appliquer Modifications", command=self._apply_edit,
                  style='TButton').pack(side='left', padx=5)
    
    def _build_validation_tab(self):
        """Onglet de validation et tests."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔬 Valider")
        
        scroll = ScrollableFrame(tab)
        scroll.pack(fill='both', expand=True)
        val_frame = scroll.inner_frame
        
        ttk.Label(val_frame, text="🔬 Atelier de validation", style='Header.TLabel').pack(anchor='w', pady=(0, 5))
        ttk.Label(val_frame, text="Vérifiez la cohérence et la structure de vos packs.",
                 style='SubHeader.TLabel').pack(anchor='w', pady=(0, 20))
        
        pack_select_frame = ttk.Frame(val_frame)
        pack_select_frame.pack(fill='x', pady=5)
        
        ttk.Label(pack_select_frame, text="Pack à valider :").pack(side='left', padx=5)
        self.validate_pack_var = tk.StringVar()
        self.validate_combo = ttk.Combobox(pack_select_frame, textvariable=self.validate_pack_var,
                                          state='readonly', width=40)
        self.validate_combo.pack(side='left', padx=5)
        ttk.Button(pack_select_frame, text="🔍 Valider", command=self._validate_pack).pack(side='left', padx=5)
        
        ttk.Label(val_frame, text="📊 Résultats de la validation", 
                 style='Accent.TLabelframe.Label').pack(anchor='w', pady=(20, 10))
        
        self.validation_result = scrolledtext.ScrolledText(
            val_frame,
            height=20,
            bg=self.COLORS['secondary'],
            fg=self.COLORS['light'],
            insertbackground=self.COLORS['gold'],
            font=('Courier', 10),
            wrap=tk.WORD
        )
        self.validation_result.pack(fill='both', expand=True)
        self.validation_result.configure(state='disabled')
    
    def _build_insights_tab(self):
        """Onglet d'analyses et insights."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔮 Insights")
        
        scroll = ScrollableFrame(tab)
        scroll.pack(fill='both', expand=True)
        insights = scroll.inner_frame
        
        ttk.Label(insights, text="🔮 Insights du Codex", style='Header.TLabel').pack(anchor='w', pady=(0, 5))
        ttk.Label(insights, text="Analyse globale des packs chargés.",
                 style='SubHeader.TLabel').pack(anchor='w', pady=(0, 20))
        
        metrics_frame = ttk.LabelFrame(insights, text="📈 Métriques globales", style='Accent.TLabelframe')
        metrics_frame.pack(fill='x', pady=10)
        
        self.metrics_text = tk.Text(metrics_frame, height=8, bg=self.COLORS['secondary'],
                                   fg=self.COLORS['light'], font=('Courier', 10))
        self.metrics_text.pack(fill='x', padx=10, pady=10)
        self.metrics_text.configure(state='disabled')
        
        ttk.Label(insights, text="🔄 Relations entre entités", 
                 style='Accent.TLabelframe.Label').pack(anchor='w', pady=(20, 10))
        
        self.relations_text = tk.Text(insights, height=10, bg=self.COLORS['secondary'],
                                     fg=self.COLORS['light'], font=('Courier', 9))
        self.relations_text.pack(fill='x', pady=10)
        self.relations_text.configure(state='disabled')
        
        ttk.Button(insights, text="🔄 Rafraîchir les insights", 
                  command=self._update_insights).pack(pady=10)
    
    def _build_profile_tab(self):
        """Onglet de génération automatique de profils."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🧬 Générer Profils")
        
        scroll = ScrollableFrame(tab)
        scroll.pack(fill='both', expand=True)
        pf = scroll.inner_frame
        
        ttk.Label(pf, text="🧬 Alchimie des profils", style='Header.TLabel').pack(anchor='w', pady=(0, 5))
        ttk.Label(pf, text="Génération automatique de profils à partir des glitches et intentions existants.",
                 style='SubHeader.TLabel').pack(anchor='w', pady=(0, 20))
        
        options_frame = ttk.Frame(pf)
        options_frame.pack(fill='x', pady=10)
        
        ttk.Label(options_frame, text="Nombre de profils :").pack(side='left', padx=5)
        self.profile_count = ttk.Spinbox(options_frame, from_=1, to=20, width=5)
        self.profile_count.pack(side='left', padx=5)
        self.profile_count.set(5)
        
        ttk.Label(options_frame, text="Source :").pack(side='left', padx=(20, 5))
        self.profile_source = ttk.Combobox(options_frame, values=['Glitches', 'Intentions', 'Mixte'], state='readonly')
        self.profile_source.pack(side='left', padx=5)
        self.profile_source.set('Glitches')
        
        ttk.Button(options_frame, text="🔮 Générer", command=self._generate_profiles,
                  style='Success.TButton').pack(side='left', padx=20)
        
        ttk.Label(pf, text="📋 Profils générés", style='Accent.TLabelframe.Label').pack(anchor='w', pady=(20, 10))
        
        self.profile_results = scrolledtext.ScrolledText(
            pf,
            height=15,
            bg=self.COLORS['secondary'],
            fg=self.COLORS['light'],
            insertbackground=self.COLORS['gold'],
            font=('Courier', 10)
        )
        self.profile_results.pack(fill='both', expand=True)
        self.profile_results.configure(state='disabled')
    
    def _build_codex_vivant_tab(self):
        """Onglet Codex Vivant — visualisation animée avec génération d'invocations."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🌀 Codex Vivant")
        
        self.vivant_canvas = CodexVivantCanvas(tab, self.forge)
        self.vivant_canvas.pack(fill='both', expand=True)
        
        controls = ttk.Frame(tab)
        controls.pack(fill='x', pady=5)
        
        anim_group = ttk.Frame(controls)
        anim_group.pack(side='left', padx=10)
        ttk.Label(anim_group, text="Animation :").pack(side='left')
        ttk.Button(anim_group, text="▶️ Démarrer", command=self._start_vivant,
                  style='Success.TButton').pack(side='left', padx=5)
        ttk.Button(anim_group, text="⏹️ Arrêter", command=self._stop_vivant,
                  style='Danger.TButton').pack(side='left', padx=5)
        
        org_group = ttk.Frame(controls)
        org_group.pack(side='left', padx=10)
        ttk.Label(org_group, text="Organisation :").pack(side='left')
        ttk.Button(org_group, text="🔄 Cercle", command=self._reorganize_vivant,
                  style='TButton').pack(side='left', padx=5)
        ttk.Button(org_group, text="📥 Recharger", command=self._reload_vivant,
                  style='TButton').pack(side='left', padx=5)
        
        gen_group = ttk.Frame(controls)
        gen_group.pack(side='left', padx=10)
        ttk.Label(gen_group, text="Invocation :").pack(side='left')
        ttk.Button(gen_group, text="🎯 Clic droit sur une entité",
                  style='Warning.TButton').pack(side='left', padx=5)
        ttk.Button(gen_group, text="🎲 Aléatoire", 
                  command=self._generate_random_invocation,
                  style='TButton').pack(side='left', padx=5)
        
        self.vivant_info = ttk.Label(tab, text="Chargement des entités...", style='Mono.TLabel')
        self.vivant_info.pack(pady=5)
        
        ttk.Label(tab, text="💡 Clic gauche : info | Clic droit : générer invocation | Molette : zoom",
                 style='Mono.TLabel').pack()
    
    def _build_status_bar(self, parent):
        """Construit la barre de statut."""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill='x', pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Prêt", style='Mono.TLabel')
        self.status_label.pack(side='left')
        
        self.modified_indicator = ttk.Label(status_frame, text="⚪", foreground=self.COLORS['muted'])
        self.modified_indicator.pack(side='right', padx=5)
        
        self.entity_counter = ttk.Label(status_frame, text="", style='Mono.TLabel')
        self.entity_counter.pack(side='right', padx=20)
    
    def _show_editor_placeholder(self):
        """Affiche un message dans l'éditeur quand aucun pack n'est sélectionné."""
        for widget in self.editor_container.winfo_children():
            widget.destroy()
        
        ttk.Label(self.editor_container, text="🔮 Sélectionnez un pack dans l'onglet 'Packs'",
                 style='SubHeader.TLabel').pack(pady=50)
        ttk.Label(self.editor_container, text="Les entrées apparaîtront ici pour édition.",
                 style='Mono.TLabel').pack()
        
        self.editor_status.config(text="Aucun pack sélectionné")
    
    def _load_default_pack(self):
        """Tente de charger un pack par défaut."""
        default_files = ['anchors.json', 'profiles.json', 'templates.json']
        for filename in default_files:
            if os.path.exists(filename):
                success, msg = self.forge.load_pack(filename)
                if success:
                    self._refresh_pack_list()
                    self._update_status(f"Pack chargé par défaut : {filename}")
                    self._update_insights()
                    self._reload_vivant()
                    return
        
        self._update_status("Aucun pack trouvé. Utilisez 'Charger Pack' pour commencer.")
    
    def _load_pack(self):
        """Charge un pack JSON via un dialogue."""
        filepath = filedialog.askopenfilename(
            title="Charger un pack JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not filepath:
            return
        
        success, msg = self.forge.load_pack(filepath)
        if success:
            self._refresh_pack_list()
            self._update_status(msg)
            self._update_insights()
            self._reload_vivant()
            messagebox.showinfo("Succès", msg)
        else:
            messagebox.showerror("Erreur", msg)
            self._update_status(f"Erreur : {msg}")
    
    def _save_pack(self):
        """Sauvegarde le pack sélectionné."""
        if not self.current_pack_path:
            messagebox.showwarning("Avertissement", "Aucun pack sélectionné.")
            return
        
        success, msg = self.forge.save_pack(self.current_pack_path)
        if success:
            self._refresh_pack_list()
            self._update_status(msg)
            self._update_insights()
            self._update_modified_indicator()
            messagebox.showinfo("Succès", msg)
        else:
            messagebox.showerror("Erreur", msg)
            self._update_status(f"Erreur : {msg}")
    
    def _revert_pack(self):
        """Rétablit le pack sélectionné à sa dernière sauvegarde."""
        if not self.current_pack_path:
            messagebox.showwarning("Avertissement", "Aucun pack sélectionné.")
            return
        
        if messagebox.askyesno("Confirmer", 
                              "Rétablir ce pack à la dernière sauvegarde ?\nToutes les modifications non sauvegardées seront perdues."):
            self.forge.revert_all()
            self._refresh_pack_list()
            self._update_status("Pack rétabli à la dernière sauvegarde.")
            self._update_modified_indicator()
            self._update_editor_for_current_pack()
            self._reload_vivant()
    
    def _new_pack(self):
        """Crée un nouveau pack JSON."""
        filepath = filedialog.asksaveasfilename(
            title="Créer un nouveau pack",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not filepath:
            return
        
        basename = os.path.basename(filepath)
        default_data = {}
        
        if 'anchors' in basename or 'incantations' in basename:
            default_data = {"exemple_catégorie": ["exemple phrase"]}
        elif 'glitches' in basename or 'effects' in basename:
            default_data = {"exemple_catégorie": ["exemple effet"]}
        elif 'locations' in basename:
            default_data = {"exemple_lieu": "Description du lieu"}
        elif 'profiles' in basename:
            default_data = {"exemple_profil": {
                "bias_intensity": 0.5,
                "bias_danger": 0.3,
                "preferred_glitch_categories": ["exemple"],
                "style": "exemple"
            }}
        elif 'templates' in basename:
            default_data = {"exemple_template": {
                "header": "{{header}}",
                "pass_template": "{{pass}}",
                "footer": "{{footer}}"
            }}
        elif 'incompatible_pairs' in basename:
            default_data = [["exemple1", "exemple2"]]
        else:
            default_data = {}
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, indent=2, ensure_ascii=False)
            
            success, msg = self.forge.load_pack(filepath)
            if success:
                self._refresh_pack_list()
                self._update_status(f"Pack créé : {basename}")
                self._update_insights()
                self._reload_vivant()
                messagebox.showinfo("Succès", f"Pack créé : {basename}")
            else:
                messagebox.showerror("Erreur", msg)
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de créer le pack : {e}")
    
    def _remove_pack(self):
        """Retire le pack sélectionné de la session."""
        selection = self.pack_list.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Sélectionnez un pack à retirer.")
            return
        
        filepath = self.pack_list.item(selection[0])['values'][0] if selection[0] else None
        if not filepath:
            return
        
        if messagebox.askyesno("Confirmer", f"Retirer le pack {os.path.basename(filepath)} de la session ?"):
            if filepath in self.forge.packs:
                del self.forge.packs[filepath]
                if filepath in self.forge.modified:
                    del self.forge.modified[filepath]
                if filepath in self.forge.backup:
                    del self.forge.backup[filepath]
            
            if self.current_pack_path == filepath:
                self.current_pack_path = None
                self._show_editor_placeholder()
            
            self._refresh_pack_list()
            self._update_status(f"Pack retiré : {os.path.basename(filepath)}")
            self._update_modified_indicator()
            self._reload_vivant()
    
    def _on_pack_select(self, event):
        """Gère la sélection d'un pack dans la liste."""
        selection = self.pack_list.selection()
        if not selection:
            return
        
        item = selection[0]
        filepath = self.pack_list.item(item)['values'][0]
        if filepath and filepath in self.forge.packs:
            self.current_pack_path = filepath
            self._update_editor_for_current_pack()
            self._update_pack_details()
            self._update_status(f"Pack sélectionné : {os.path.basename(filepath)}")
            self._update_validate_combo()
    
    def _update_pack_details(self):
        """Met à jour l'affichage des détails du pack sélectionné."""
        if not self.current_pack_path or self.current_pack_path not in self.forge.packs:
            self.pack_details.configure(state='normal')
            self.pack_details.delete('1.0', tk.END)
            self.pack_details.insert('1.0', "Aucun pack sélectionné")
            self.pack_details.configure(state='disabled')
            return
        
        data = self.forge.packs[self.current_pack_path]
        self.pack_details.configure(state='normal')
        self.pack_details.delete('1.0', tk.END)
        
        try:
            formatted = json.dumps(data, indent=2, ensure_ascii=False)
            self.pack_details.insert('1.0', formatted)
        except:
            self.pack_details.insert('1.0', str(data))
        
        self.pack_details.configure(state='disabled')
    
    def _update_editor_for_current_pack(self):
        """Met à jour l'interface d'édition pour le pack sélectionné."""
        for widget in self.editor_container.winfo_children():
            widget.destroy()
        
        if not self.current_pack_path or self.current_pack_path not in self.forge.packs:
            self._show_editor_placeholder()
            return
        
        data = self.forge.packs[self.current_pack_path]
        basename = os.path.basename(self.current_pack_path)
        
        self.editor_status.config(text=f"Édition de : {basename} — {type(data).__name__}")
        
        tree_frame = ttk.Frame(self.editor_container)
        tree_frame.pack(fill='both', expand=True)
        
        self.entry_tree = ttk.Treeview(tree_frame, columns=('value',), show='tree')
        self.entry_tree.pack(side='left', fill='both', expand=True)
        self.entry_tree.heading('#0', text='Clé / Index')
        self.entry_tree.heading('value', text='Valeur')
        self.entry_tree.column('#0', width=300)
        self.entry_tree.column('value', width=500)
        
        tree_scroll = ttk.Scrollbar(tree_frame, orient='vertical', command=self.entry_tree.yview)
        tree_scroll.pack(side='right', fill='y')
        self.entry_tree.configure(yscrollcommand=tree_scroll.set)
        
        self._populate_entry_tree(self.entry_tree, data)
        
        edit_entry_frame = ttk.LabelFrame(self.editor_container, text="✏️ Éditeur d'entrée", style='Accent.TLabelframe')
        edit_entry_frame.pack(fill='x', pady=10)
        
        key_frame = ttk.Frame(edit_entry_frame)
        key_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(key_frame, text="Clé/Index :").pack(side='left', padx=5)
        self.edit_key = ttk.Entry(key_frame, width=30)
        self.edit_key.pack(side='left', padx=5)
        
        value_frame = ttk.Frame(edit_entry_frame)
        value_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(value_frame, text="Valeur (JSON) :").pack(anchor='w', padx=5)
        
        self.edit_value = scrolledtext.ScrolledText(
            value_frame,
            height=6,
            bg=self.COLORS['secondary'],
            fg=self.COLORS['light'],
            insertbackground=self.COLORS['gold'],
            font=('Courier', 10)
        )
        self.edit_value.pack(fill='x', padx=5, pady=5)
        
        edit_buttons = ttk.Frame(edit_entry_frame)
        edit_buttons.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(edit_buttons, text="📥 Charger sélection", 
                  command=self._load_selection_to_editor).pack(side='left', padx=5)
        ttk.Button(edit_buttons, text="💾 Mettre à jour", 
                  command=self._update_selected_entry,
                  style='Success.TButton').pack(side='left', padx=5)
        
        self.entry_tree.bind('<<TreeviewSelect>>', self._on_entry_select)
        
        self.entity_counter.config(text=f"Entités : {len(data) if isinstance(data, (dict, list)) else 0}")
    
    def _populate_entry_tree(self, tree, data, parent=''):
        """Remplit le treeview avec les données."""
        if isinstance(data, dict):
            for key, value in data.items():
                item_id = f"{parent}.{key}" if parent else key
                value_str = self._format_value_preview(value)
                tree.insert(parent, 'end', iid=item_id, text=str(key), values=(value_str,))
                if isinstance(value, (dict, list)):
                    self._populate_entry_tree(tree, value, item_id)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                item_id = f"{parent}[{i}]" if parent else f"[{i}]"
                value_str = self._format_value_preview(item)
                tree.insert(parent, 'end', iid=item_id, text=f"[{i}]", values=(value_str,))
                if isinstance(item, (dict, list)):
                    self._populate_entry_tree(tree, item, item_id)
    
    def _format_value_preview(self, value, max_len=80):
        """Formate une valeur pour un aperçu."""
        if isinstance(value, str):
            if len(value) > max_len:
                return value[:max_len] + "..."
            return value
        elif isinstance(value, (dict, list)):
            return f"{type(value).__name__} ({len(value)} éléments)"
        else:
            return str(value)
    
    def _on_entry_select(self, event):
        """Gère la sélection d'une entrée dans l'arbre."""
        selection = self.entry_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        key = self.entry_tree.item(item)['text']
        value_str = self.entry_tree.item(item)['values'][0]
        
        self.edit_key.delete(0, tk.END)
        self.edit_key.insert(0, key)
        
        data = self.forge.packs.get(self.current_pack_path, {})
        real_value = self._get_value_by_path(data, item)
        if real_value is not None:
            self.edit_value.delete('1.0', tk.END)
            try:
                self.edit_value.insert('1.0', json.dumps(real_value, indent=2, ensure_ascii=False))
            except:
                self.edit_value.insert('1.0', str(real_value))
    
    def _get_value_by_path(self, data, path):
        """Récupère une valeur par son chemin dans l'arbre."""
        if not path:
            return data
        
        parts = []
        current = ""
        in_bracket = False
        
        for char in path:
            if char == '[':
                if current:
                    parts.append(current)
                    current = ""
                in_bracket = True
            elif char == ']':
                if current:
                    parts.append(f"[{current}]")
                    current = ""
                in_bracket = False
            elif char == '.' and not in_bracket:
                if current:
                    parts.append(current)
                    current = ""
            else:
                current += char
        
        if current:
            parts.append(current)
        
        result = data
        try:
            for part in parts:
                if part.startswith('[') and part.endswith(']'):
                    idx = int(part[1:-1])
                    if isinstance(result, list) and idx < len(result):
                        result = result[idx]
                    else:
                        return None
                else:
                    if isinstance(result, dict) and part in result:
                        result = result[part]
                    else:
                        return None
            return result
        except:
            return None
    
    def _load_selection_to_editor(self):
        """Charge la sélection dans l'éditeur."""
        self._on_entry_select(None)
    
    def _update_selected_entry(self):
        """Met à jour l'entrée sélectionnée avec les valeurs de l'éditeur."""
        if not self.current_pack_path:
            messagebox.showwarning("Avertissement", "Aucun pack sélectionné.")
            return
        
        selection = self.entry_tree.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Sélectionnez une entrée à modifier.")
            return
        
        key = self.edit_key.get().strip()
        if not key:
            messagebox.showwarning("Avertissement", "La clé ne peut pas être vide.")
            return
        
        try:
            value_str = self.edit_value.get('1.0', tk.END).strip()
            if value_str:
                new_value = json.loads(value_str)
            else:
                new_value = None
        except json.JSONDecodeError as e:
            messagebox.showerror("Erreur", f"JSON invalide : {e}")
            return
        
        data = self.forge.packs[self.current_pack_path]
        
        try:
            if isinstance(data, dict):
                data[key] = new_value
            elif isinstance(data, list):
                try:
                    idx = int(key.replace('[', '').replace(']', ''))
                    if 0 <= idx < len(data):
                        data[idx] = new_value
                    else:
                        messagebox.showerror("Erreur", "Index hors limites.")
                        return
                except:
                    messagebox.showerror("Erreur", "Pour une liste, utilisez [index] comme clé.")
                    return
            
            self.forge.modified[self.current_pack_path] = True
            self._refresh_pack_list()
            self._update_editor_for_current_pack()
            self._update_pack_details()
            self._update_status("Entrée mise à jour.")
            self._update_modified_indicator()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la mise à jour : {e}")
    
    def _add_entry(self):
        """Ajoute une nouvelle entrée au pack."""
        if not self.current_pack_path:
            messagebox.showwarning("Avertissement", "Aucun pack sélectionné.")
            return
        
        data = self.forge.packs[self.current_pack_path]
        
        add_dialog = tk.Toplevel(self.root)
        add_dialog.title("Ajouter une entrée")
        add_dialog.geometry("500x300")
        add_dialog.configure(bg=self.COLORS['background'])
        add_dialog.transient(self.root)
        add_dialog.grab_set()
        
        ttk.Label(add_dialog, text="➕ Ajouter une entrée", style='Header.TLabel').pack(pady=10)
        
        struct_frame = ttk.Frame(add_dialog)
        struct_frame.pack(fill='x', padx=20, pady=5)
        
        ttk.Label(struct_frame, text="Type de structure :").pack(side='left', padx=5)
        struct_type = ttk.Combobox(struct_frame, values=['Clé → Valeur', 'Valeur seule'], state='readonly')
        struct_type.pack(side='left', padx=5)
        struct_type.current(0 if isinstance(data, dict) else 1)
        
        key_frame = ttk.Frame(add_dialog)
        key_frame.pack(fill='x', padx=20, pady=5)
        ttk.Label(key_frame, text="Clé :").pack(side='left', padx=5)
        key_entry = ttk.Entry(key_frame, width=30)
        key_entry.pack(side='left', padx=5)
        
        value_frame = ttk.Frame(add_dialog)
        value_frame.pack(fill='both', expand=True, padx=20, pady=5)
        ttk.Label(value_frame, text="Valeur (JSON) :").pack(anchor='w', padx=5)
        value_text = scrolledtext.ScrolledText(
            value_frame,
            height=6,
            bg=self.COLORS['secondary'],
            fg=self.COLORS['light'],
            insertbackground=self.COLORS['gold'],
            font=('Courier', 10)
        )
        value_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        btn_frame = ttk.Frame(add_dialog)
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        def do_add():
            key = key_entry.get().strip()
            if not key and isinstance(data, dict):
                messagebox.showwarning("Avertissement", "La clé est obligatoire pour un dictionnaire.")
                return
            
            try:
                value = json.loads(value_text.get('1.0', tk.END).strip()) if value_text.get('1.0', tk.END).strip() else None
            except json.JSONDecodeError as e:
                messagebox.showerror("Erreur", f"JSON invalide : {e}")
                return
            
            if isinstance(data, dict) and key:
                data[key] = value
            elif isinstance(data, list):
                data.append(value if value is not None else {})
            else:
                messagebox.showerror("Erreur", "Type de pack non supporté.")
                return
            
            self.forge.modified[self.current_pack_path] = True
            self._refresh_pack_list()
            self._update_editor_for_current_pack()
            self._update_pack_details()
            self._update_status("Entrée ajoutée.")
            self._update_modified_indicator()
            add_dialog.destroy()
        
        ttk.Button(btn_frame, text="✅ Ajouter", command=do_add,
                  style='Success.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text="❌ Annuler", command=add_dialog.destroy,
                  style='Danger.TButton').pack(side='left', padx=5)
    
    def _delete_entry(self):
        """Supprime l'entrée sélectionnée."""
        if not self.current_pack_path:
            messagebox.showwarning("Avertissement", "Aucun pack sélectionné.")
            return
        
        selection = self.entry_tree.selection()
        if not selection:
            messagebox.showwarning("Avertissement", "Sélectionnez une entrée à supprimer.")
            return
        
        item = selection[0]
        key = self.entry_tree.item(item)['text']
        
        if messagebox.askyesno("Confirmer", f"Supprimer l'entrée '{key}' ?"):
            data = self.forge.packs[self.current_pack_path]
            
            try:
                if isinstance(data, dict) and key in data:
                    del data[key]
                elif isinstance(data, list):
                    try:
                        idx = int(key.replace('[', '').replace(']', ''))
                        if 0 <= idx < len(data):
                            del data[idx]
                        else:
                            messagebox.showerror("Erreur", "Index hors limites.")
                            return
                    except:
                        messagebox.showerror("Erreur", "Suppression non supportée.")
                        return
                else:
                    messagebox.showerror("Erreur", "Type de pack non supporté.")
                    return
                
                self.forge.modified[self.current_pack_path] = True
                self._refresh_pack_list()
                self._update_editor_for_current_pack()
                self._update_pack_details()
                self._update_status(f"Entrée supprimée : {key}")
                self._update_modified_indicator()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression : {e}")
    
    def _apply_edit(self):
        """Appliquer les modifications (sauvegarde dans le pack)."""
        self._save_pack()
    
    def _validate_pack(self):
        """Valide le pack sélectionné."""
        pack_name = self.validate_pack_var.get()
        if not pack_name:
            messagebox.showwarning("Avertissement", "Sélectionnez un pack à valider.")
            return
        
        filepath = None
        for path in self.forge.packs.keys():
            if os.path.basename(path) == pack_name:
                filepath = path
                break
        
        if not filepath:
            messagebox.showerror("Erreur", "Pack non trouvé.")
            return
        
        data = self.forge.packs[filepath]
        
        results = []
        results.append(f"🔍 Validation de : {pack_name}")
        results.append(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        results.append("=" * 60)
        
        if isinstance(data, dict):
            results.append(f"✅ Structure : Dictionnaire ({len(data)} entrées)")
            for key in data.keys():
                if not isinstance(key, str):
                    results.append(f"⚠️  Clé non string : {key}")
        elif isinstance(data, list):
            results.append(f"✅ Structure : Liste ({len(data)} entrées)")
        else:
            results.append(f"❌ Structure invalide : {type(data).__name__}")
            self._display_validation_results("\n".join(results))
            return
        
        basename = os.path.basename(filepath)
        if basename in self.forge.FILE_TYPES:
            info = self.forge.FILE_TYPES[basename]
            results.append(f"📋 Type attendu : {info['description']}")
            
            if basename == 'profiles.json' and isinstance(data, dict):
                for name, profile in data.items():
                    if 'bias_intensity' not in profile:
                        results.append(f"⚠️  Profil '{name}' : manque 'bias_intensity'")
                    if 'bias_danger' not in profile:
                        results.append(f"⚠️  Profil '{name}' : manque 'bias_danger'")
            elif basename == 'templates.json' and isinstance(data, dict):
                for name, template in data.items():
                    if 'header' not in template:
                        results.append(f"⚠️  Template '{name}' : manque 'header'")
                    if 'pass_template' not in template:
                        results.append(f"⚠️  Template '{name}' : manque 'pass_template'")
                    if 'footer' not in template:
                        results.append(f"⚠️  Template '{name}' : manque 'footer'")
        
        try:
            json_str = json.dumps(data)
            results.append(f"📊 Taille : {len(json_str)} caractères")
        except:
            results.append("⚠️  Erreur lors de la sérialisation JSON")
        
        results.append("\n🔮 Insights détectés :")
        insights = self._generate_pack_insights(data)
        if insights:
            results.extend([f"  {insight}" for insight in insights])
        else:
            results.append("  ✅ Aucun problème détecté.")
        
        self._display_validation_results("\n".join(results))
    
    def _display_validation_results(self, text):
        """Affiche les résultats de validation."""
        self.validation_result.configure(state='normal')
        self.validation_result.delete('1.0', tk.END)
        self.validation_result.insert('1.0', text)
        self.validation_result.configure(state='disabled')
    
    def _generate_pack_insights(self, data):
        """Génère des insights sur un pack."""
        insights = []
        
        if isinstance(data, dict):
            empty_keys = [k for k, v in data.items() if not v]
            if empty_keys:
                insights.append(f"⚠️  Clés vides détectées : {', '.join(empty_keys[:3])}{'...' if len(empty_keys) > 3 else ''}")
            
            keys_lower = {k.lower(): k for k in data.keys()}
            if len(keys_lower) < len(data):
                insights.append("🔄 Des clés pourraient être en doublon (insensible à la casse)")
        
        elif isinstance(data, list):
            empty_items = [i for i, item in enumerate(data) if not item]
            if empty_items:
                insights.append(f"⚠️  Éléments vides aux indices : {empty_items[:3]}{'...' if len(empty_items) > 3 else ''}")
        
        try:
            json_str = json.dumps(data)
            if any(c in json_str for c in ['\x00', '\x01', '\x02']):
                insights.append("⚠️  Caractères de contrôle détectés dans le JSON")
        except:
            insights.append("❌ Impossible de sérialiser le JSON")
        
        return insights
    
    def _update_validate_combo(self):
        """Met à jour le combobox de validation."""
        pack_names = [os.path.basename(p) for p in self.forge.packs.keys()]
        self.validate_combo['values'] = pack_names
        if pack_names and not self.validate_pack_var.get():
            self.validate_pack_var.set(pack_names[0])
    
    def _update_insights(self):
        """Met à jour l'onglet Insights."""
        self.metrics_text.configure(state='normal')
        self.metrics_text.delete('1.0', tk.END)
        
        metrics = []
        metrics.append(f"📦 Packs chargés : {len(self.forge.packs)}")
        
        total_entries = 0
        total_size = 0
        
        for path, data in self.forge.packs.items():
            basename = os.path.basename(path)
            size = len(json.dumps(data))
            total_size += size
            entries = len(data) if isinstance(data, (dict, list)) else 0
            total_entries += entries
            metrics.append(f"  • {basename} : {entries} entrées, {size} octets")
        
        metrics.append(f"\n📊 Total : {total_entries} entrées, {total_size} octets")
        
        types = {}
        for path in self.forge.packs.keys():
            basename = os.path.basename(path)
            if basename in self.forge.FILE_TYPES:
                t = self.forge.FILE_TYPES[basename]['entity_type']
                types[t] = types.get(t, 0) + 1
        
        if types:
            metrics.append("\n📂 Répartition par type :")
            for t, count in types.items():
                metrics.append(f"  • {t} : {count}")
        
        self.metrics_text.insert('1.0', "\n".join(metrics))
        self.metrics_text.configure(state='disabled')
        
        self.relations_text.configure(state='normal')
        self.relations_text.delete('1.0', tk.END)
        
        relations = ["🔄 Relations entre packs :\n"]
        
        if 'profiles.json' in self.forge.packs and 'templates.json' in self.forge.packs:
            relations.append("  • Profils ↔ Templates : Des profils peuvent être utilisés avec des templates")
        
        if 'glitches.json' in self.forge.packs and 'effects.json' in self.forge.packs:
            relations.append("  • Glitches ↔ Effets : Les glitches peuvent moduler les effets")
        
        if 'anchors.json' in self.forge.packs and 'incantations.json' in self.forge.packs:
            relations.append("  • Ancrages ↔ Incantations : Les ancrages peuvent renforcer les incantations")
        
        if len(relations) == 1:
            relations.append("  Aucune relation évidente détectée.")
        
        relations.append("\n💡 Suggestions d'extensions :")
        base_types = [os.path.basename(p).replace('.json', '') for p in self.forge.packs.keys()]
        
        if 'profiles' in base_types and 'glitches' not in base_types:
            relations.append("  • Ajoutez des glitches pour enrichir vos profils")
        
        if 'templates' in base_types and 'profiles' not in base_types:
            relations.append("  • Ajoutez des profils pour personnaliser vos templates")
        
        if 'incompatible_pairs' not in base_types:
            relations.append("  • Créez des paires incompatibles pour éviter des combinaisons absurdes")
        
        self.relations_text.insert('1.0', "\n".join(relations))
        self.relations_text.configure(state='disabled')
    
    def _refresh_pack_list(self):
        """Rafraîchit la liste des packs."""
        for item in self.pack_list.get_children():
            self.pack_list.delete(item)
        
        for path, data in self.forge.packs.items():
            basename = os.path.basename(path)
            info = self.forge.FILE_TYPES.get(basename, {})
            icon = info.get('icon', '📄')
            
            status = "⚪ Non modifié"
            if self.forge.modified.get(path, False):
                status = "🔵 Modifié"
            
            entries = len(data) if isinstance(data, (dict, list)) else 0
            self.pack_list.insert('', 'end', text=f"{icon} {basename}", 
                                 values=(path, f"{entries} entrées", status))
        
        total = sum(len(d) if isinstance(d, (dict, list)) else 0 for d in self.forge.packs.values())
        self.entity_counter.config(text=f"Total : {total} entités")
        
        self._update_validate_combo()
    
    def _update_modified_indicator(self):
        """Met à jour l'indicateur de modifications."""
        if self.forge.has_modifications():
            self.modified_indicator.config(text="🔵", foreground=self.COLORS['gold'])
        else:
            self.modified_indicator.config(text="⚪", foreground=self.COLORS['muted'])
    
    def _update_status(self, message):
        """Met à jour la barre de statut."""
        self.status_label.config(text=f"⏳ {message}")
        self.root.update_idletasks()
    
    def _bind_keys(self):
        """Bind les touches pour les actions rapides."""
        self.root.bind('<Control-o>', lambda e: self._load_pack())
        self.root.bind('<Control-s>', lambda e: self._save_pack())
        self.root.bind('<Control-n>', lambda e: self._new_pack())
        self.root.bind('<Control-r>', lambda e: self._revert_pack())
        self.root.bind('<F5>', lambda e: self._update_insights())
        self.root.bind('<Escape>', lambda e: self.root.quit())
    
    # === Profils ===
    
    def _generate_profiles(self):
        """Génère des profils et affiche les résultats."""
        count = int(self.profile_count.get())
        source = self.profile_source.get()
        
        generator = ProfileGenerator(self.forge)
        
        if 'Glitches' in source:
            profiles = generator.generate_profiles_from_glitches(count)
        elif 'Intentions' in source:
            profiles = generator.generate_profiles_from_intentions(count)
        else:
            glitch_profiles = generator.generate_profiles_from_glitches(count // 2 + 1)
            intention_profiles = generator.generate_profiles_from_intentions(count // 2)
            profiles = {**glitch_profiles, **intention_profiles}
        
        self.profile_results.configure(state='normal')
        self.profile_results.delete('1.0', tk.END)
        
        if "error" in profiles:
            self.profile_results.insert('1.0', f"❌ {profiles['error']}")
        else:
            output = []
            for name, profile in profiles.items():
                output.append(f"🔮 {name}")
                output.append("=" * 50)
                for key, value in profile.items():
                    output.append(f"  {key}: {value}")
                output.append("")
            
            self.profile_results.insert('1.0', "\n".join(output))
            
            if messagebox.askyesno("Ajouter au pack", 
                                  "Voulez-vous ajouter ces profils à votre pack profiles.json ?"):
                self._add_profiles_to_pack(profiles)
        
        self.profile_results.configure(state='disabled')
    
    def _add_profiles_to_pack(self, profiles):
        """Ajoute les profils générés au pack profiles.json."""
        profiles_path = None
        for path in self.forge.packs.keys():
            if 'profiles' in os.path.basename(path):
                profiles_path = path
                break
        
        if not profiles_path:
            profiles_path = filedialog.asksaveasfilename(
                title="Sauvegarder les profils",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")],
                initialfile="profiles_generated.json"
            )
            if not profiles_path:
                return
        
        if profiles_path in self.forge.packs:
            data = self.forge.packs[profiles_path]
        else:
            data = {}
        
        data.update(profiles)
        
        self.forge.packs[profiles_path] = data
        self.forge.modified[profiles_path] = True
        self._refresh_pack_list()
        self._update_status(f"{len(profiles)} profils ajoutés au pack.")
        self._update_modified_indicator()
        self._reload_vivant()
    
    # === Codex Vivant ===
    
    def _start_vivant(self):
        """Démarre l'animation du Codex Vivant."""
        self.vivant_canvas.start_animation()
        self.vivant_info.config(text="🌀 Codex Vivant actif")
    
    def _stop_vivant(self):
        """Arrête l'animation du Codex Vivant."""
        self.vivant_canvas.stop_animation()
        self.vivant_info.config(text="⏸️ Codex Vivant en pause")
    
    def _reorganize_vivant(self):
        """Réorganise les entités dans le Codex Vivant."""
        self.vivant_canvas._arrange_in_circle()
        self.vivant_canvas.redraw()
    
    def _reload_vivant(self):
        """Recharge les entités dans le Codex Vivant."""
        self.vivant_canvas.load_entities()
        self.vivant_info.config(text=f"📊 {len(self.vivant_canvas.entities)} entités chargées")
    
    def _generate_random_invocation(self):
        """Génère une invocation aléatoire et l'affiche."""
        if not self.vivant_canvas.entities:
            messagebox.showwarning("Avertissement", "Aucune entité chargée dans le Codex Vivant.")
            return
        
        entity = random.choice(self.vivant_canvas.entities)
        self.vivant_canvas._generate_invocation_for_entity(entity)


# ============================================================================
# POINT D'ENTRÉE — L'INVOCATION DU CODEX
# ============================================================================

def main():
    """Point d'entrée principal pour Codex Forge."""
    root = tk.Tk()
    
    try:
        root.iconbitmap(default='codex.ico')
    except:
        pass
    
    app = CodexForgeApp(root)
    
    def on_closing():
        if app.forge.has_modifications():
            if messagebox.askyesno("Quitter", 
                                  "Des modifications sont en attente.\nVoulez-vous vraiment quitter sans sauvegarder ?"):
                if app.vivant_canvas.animation_running:
                    app.vivant_canvas.stop_animation()
                root.destroy()
        else:
            if app.vivant_canvas.animation_running:
                app.vivant_canvas.stop_animation()
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
