# 📊 Big Data Anomaly Dashboard — JIRA-like Test Tracker

> **Big Data Testing Project** | Python · SQLite · HTML Dashboard · Test Management

---

## 🇫🇷 Description

Dashboard de suivi des anomalies de test Big Data, style **JIRA/XRAY**.  
Permet de créer, filtrer, mettre à jour et visualiser les anomalies détectées durant les campagnes de test.
Génère un rapport HTML interactif avec KPIs, distribution par statut, sévérité et composant.

## 🇬🇧 Description

Big Data test anomaly tracking dashboard in the style of **JIRA/XRAY**.  
Create, filter, update, and visualize anomalies detected during test campaigns.  
Generates an interactive HTML report with KPIs, status distribution, severity, and component breakdown.

---

## 🗂️ Structure du projet

```
04_anomaly_dashboard/
├── src/
│   ├── anomaly_tracker.py    # CRUD SQLite — tickets d'anomalie
│   ├── dashboard.py          # Générateur HTML dashboard
│   └── run_dashboard.py      # Entry point — seed + génère le dashboard
├── tests/
│   └── test_anomaly_tracker.py   # TC-DASH-001 → TC-DASH-010
├── data/
│   ├── anomalies.db          # Base SQLite (générée)
│   └── dashboard.html        # Dashboard HTML (généré)
└── docs/
```

---

## 🎯 Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| Création d'anomalie | Titre, description, sévérité, statut, sprint, tags |
| Mise à jour de statut | OPEN → IN_PROGRESS → RESOLVED → CLOSED |
| Commentaires | Fil de discussion par anomalie |
| Filtres | Par statut, sévérité, composant |
| KPIs | Total, Open, In Progress, Resolved, Open Critical |
| Distribution | Barre de progression colorée par statut |
| Rapport HTML | Dashboard interactif généré en local |

---

## 🏷️ Sévérités & Statuts

| Sévérité | Couleur | Exemples |
|---|---|---|
| CRITICAL | 🔴 Rouge | Données corrompues, réconciliation impossible |
| HIGH | 🟠 Orange | FK orpheline, NULL sur clé obligatoire |
| MEDIUM | 🟡 Jaune | Filtre manquant, format incorrect |
| LOW | 🔵 Bleu | Colonne inattendue, dérive statistique mineure |

| Statut | Description |
|---|---|
| OPEN | Anomalie détectée, non traitée |
| IN_PROGRESS | Analyse ou correction en cours |
| RESOLVED | Fix déployé, en attente de validation |
| CLOSED | Validé et fermé |
| WONT_FIX | Décision de ne pas corriger |

---

## ⚙️ Installation & Exécution

```bash
pip install -r requirements.txt

# Générer le dashboard avec données d'exemple
cd src
python run_dashboard.py

# Ouvrir le dashboard (macOS)
open ../data/dashboard.html

# Tests unitaires
pytest tests/ -v
```

---

## 📸 Anomalies d'exemple pré-chargées

10 anomalies réalistes issues des 3 autres projets :

| ID | Titre | Sévérité | Statut | Projet |
|---|---|---|---|---|
| ANO-... | NULL customer_id in fact_sales | HIGH | OPEN | DataMart-Q1 |
| ANO-... | Negative total_amount in S011 | CRITICAL | IN_PROGRESS | DataMart-Q1 |
| ANO-... | Orphan FK C999 | HIGH | OPEN | DataMart-Q1 |
| ANO-... | CANCELLED status not filtered | MEDIUM | RESOLVED | Datalake |
| ANO-... | Gold reconciliation drift 1.8% | HIGH | OPEN | Datalake |

---

## 👩‍💻 Auteure

**Imane Moussafir** — Ingénieure Data & BI  
*Projet réalisé dans le cadre d'une candidature Testeur Big Data / Datalake.*
