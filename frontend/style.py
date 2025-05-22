# frontend/style.py

# 🌟 Styles généraux pour tout le logiciel

# Couleurs principales
PRIMARY_COLOR = "#5DADE2"      # Bleu doux
SECONDARY_COLOR = "#2980B9"    # Bleu foncé
TEXT_COLOR = "#2C3E50"         # Gris foncé pour le texte
BACKGROUND_COLOR = "#ECF0F1"   # Gris clair de fond
SUCCESS_COLOR = "#27AE60"      # Vert succès
ERROR_COLOR = "#E74C3C"        # Rouge erreur

# Styles pour les boutons principaux
BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {PRIMARY_COLOR};
        color: white;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {SECONDARY_COLOR};
    }}
"""

# Style pour les champs de saisie
INPUT_STYLE = """
    QLineEdit {
        padding: 8px;
        border: 1px solid #bdc3c7;
        border-radius: 5px;
    }
"""

# Style pour les titres
TITLE_STYLE = """
    QLabel {
        font-size: 22px;
        font-weight: bold;
        color: #2C3E50;
    }
"""

# Style pour les liens
LINK_BUTTON_STYLE = f"""
    QPushButton {{
        background: transparent;
        color: {SECONDARY_COLOR};
        text-decoration: underline;
        border: none;
        font-weight: bold;
    }}
    QPushButton:hover {{
        color: {PRIMARY_COLOR};
    }}
"""


# frontend/style.py

TITLE_STYLE = """
    font-size: 24px;
    font-weight: bold;
    padding: 10px;
    color: #2c3e50;
"""

BUTTON_STYLE = """
    font-size: 16px;
    padding: 8px;
    background-color: #3498db;
    color: white;
    border-radius: 8px;
"""

INPUT_STYLE = """
    font-size: 16px;
    padding: 6px;
"""

LABEL_STYLE = """
    font-size: 18px;
    padding: 8px;
    color: #333;
"""
