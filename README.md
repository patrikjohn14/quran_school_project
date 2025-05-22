

# 📘 Quran School Management System

## 🛠️ Description du projet

Un logiciel de gestion pour une école coranique, développé en **Python** avec **PyQt5** pour l'interface graphique et **MySQL** pour la base de données.

Fonctionnalités principales :
- Inscription et connexion d'utilisateurs (admin, enseignant, élève)
- Gestion des élèves, enseignants et cours
- Gestion de l'assiduité et des notes
- Interface utilisateur simple, moderne et fonctionnelle

---

## 📂 Structure du projet

```
quran_school_project/
│
├── backend/                   # Connexion base de données et logique métier
│   ├── db_connection.py
│   ├── auth.py
│
├── frontend/                   # Interface utilisateur PyQt5
│   ├── login_window.py
│   ├── register_window.py
│   ├── main_window.py
│   └── components/             # Widgets réutilisables (facultatif)
│
├── assets/                     # Images et icônes
│
├── main.py                     # Lancement de l'application
└── requirements.txt            # Bibliothèques Python nécessaires
```

---

## 💻 Technologies utilisées

- **Python 3**
- **PyQt5** (interfaces graphiques)
- **MySQL** (base de données)
- **bcrypt** (hachage des mots de passe pour la sécurité)
- **dotenv** (gestion des variables d'environnement)

---

## 📦 Installation

1. Cloner ce projet :

```bash
git clone [lien-du-dépôt]
```

2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

3. Configurer la connexion MySQL :
   - Créer un fichier `.env` pour stocker l'host, user, mot de passe et nom de base de données.

4. Lancer l'application :

```bash
python main.py
```

---

## 📈 Progression (Checkpoints)

| Checkpoint | Statut | Description |
|:-----------|:------|:------------|
| Checkpoint 1 | ✅ Terminé | Installation, structure de projet, fichier main.py |
| Checkpoint 2 | 🔜 En cours | Création de la fenêtre de connexion |
| Checkpoint 3 | ⏳ | Création de la fenêtre d'inscription |
| Checkpoint 4 | ⏳ | Création de la page d'accueil |
| Checkpoint 5 | ⏳ | Authentification MySQL |
| Checkpoint 6 | ⏳ | Gestion élèves, enseignants, cours |
| Checkpoint 7 | ⏳ | Présence et notes |
| Checkpoint 8 | ⏳ | Finitions et polish UX |

---

## ✨ Auteurs

- Projet guidé et développé étape par étape
