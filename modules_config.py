"""
Configuration des modules de génie logiciel
Structure des modules, matières et coefficients de calcul
Basé sur les listes officielles de l'INSTA
"""

MODULES_DATA = {
    "Niveau 1": {
        "Semestre 1": {
            "Module 1": {
                "nom": "Architecture et Technologie des Ordinateurs",
                "matieres": [
                    {"nom": "Architecture et Techno des Ordinateurs", "avec_tp": True, "coefficient": 3},
                    {"nom": "Logique des Systèmes Numériques", "avec_tp": True, "coefficient": 2}
                ]
            },
            "Module 2": {
                "nom": "Systèmes d'Exploitation",
                "matieres": [
                    {"nom": "Systèmes d'exploitation 1 (Initiation)", "avec_tp": True, "coefficient": 3}
                ]
            },
            "Module 3": {
                "nom": "Algorithmique et Programmation",
                "matieres": [
                    {"nom": "Algorithmique 1", "avec_tp": True, "coefficient": 3},
                    {"nom": "Outils logiciels pour micro-ordinateur", "avec_tp": True, "coefficient": 2}
                ]
            },
            "Module 4": {
                "nom": "Mathématiques",
                "matieres": [
                    {"nom": "Analyse I", "avec_tp": False, "coefficient": 3},
                    {"nom": "Statistique descriptive", "avec_tp": False, "coefficient": 2}
                ]
            },
            "Module 5": {
                "nom": "Physique",
                "matieres": [
                    {"nom": "Électricité générale", "avec_tp": True, "coefficient": 3},
                    {"nom": "Mécanique générale", "avec_tp": True, "coefficient": 3},
                    {"nom": "Optique Géométrique", "avec_tp": False, "coefficient": 2}
                ]
            },
            "Module 6": {
                "nom": "Langues et Gestion",
                "matieres": [
                    {"nom": "Anglais 1", "avec_tp": False, "coefficient": 2},
                    {"nom": "Arabe 1", "avec_tp": False, "coefficient": 2},
                    {"nom": "Comptabilité Générale", "avec_tp": False, "coefficient": 2}
                ]
            }
        },
        "Semestre 2": {
            "Module 7": {
                "nom": "Systèmes d'Exploitation Avancés",
                "matieres": [
                    {"nom": "Systèmes d'exploitation II", "avec_tp": True, "coefficient": 3},
                    {"nom": "Archi interne ordi (Maintenance)", "avec_tp": True, "coefficient": 3}
                ]
            },
            "Module 8": {
                "nom": "Programmation et Structures de Données",
                "matieres": [
                    {"nom": "Structure des données", "avec_tp": True, "coefficient": 3},
                    {"nom": "Programmation modulaire en C", "avec_tp": True, "coefficient": 4},
                    {"nom": "Atelier de programmation 1", "avec_tp": True, "coefficient": 2}
                ]
            },
            "Module 9": {
                "nom": "Bases de Données",
                "matieres": [
                    {"nom": "Systèmes d'Information I", "avec_tp": True, "coefficient": 2},
                    {"nom": "Modèles et langages des bases de données", "avec_tp": True, "coefficient": 3}
                ]
            },
            "Module 10": {
                "nom": "Mathématiques",
                "matieres": [
                    {"nom": "Analyse II", "avec_tp": False, "coefficient": 3},
                    {"nom": "Algèbre", "avec_tp": False, "coefficient": 3}
                ]
            },
            "Module 11": {
                "nom": "Langues et Économie",
                "matieres": [
                    {"nom": "Anglais II", "avec_tp": False, "coefficient": 2},
                    {"nom": "Arabe II", "avec_tp": False, "coefficient": 2},
                    {"nom": "Économie Générale", "avec_tp": False, "coefficient": 2}
                ]
            }
        }
    },
    "Niveau 2": {
        "Semestre 3": {
            "Module 12": {
                "nom": "Systèmes d'Information",
                "matieres": [
                    {"nom": "Systèmes d'Information II - Analyse et conception", "avec_tp": False, "coefficient": 3},
                    {"nom": "Exploitation de bases de données relationnelles", "avec_tp": False, "coefficient": 3},
                    {"nom": "Génie logiciel", "avec_tp": False, "coefficient": 3}
                ]
            },
            "Module 13": {
                "nom": "Programmation Orientée Objet",
                "matieres": [
                    {"nom": "Programmation orientée objet en Java", "avec_tp": True, "coefficient": 4}
                ]
            },
            "Module 14": {
                "nom": "Réseaux et Web",
                "matieres": [
                    {"nom": "Réseaux informatiques I", "avec_tp": True, "coefficient": 3},
                    {"nom": "Développement web I", "avec_tp": True, "coefficient": 3}
                ]
            },
            "Module 15": {
                "nom": "Mathématiques",
                "matieres": [
                    {"nom": "Programmation Linéaire", "avec_tp": False, "coefficient": 2},
                    {"nom": "Probabilité/Statistique", "avec_tp": False, "coefficient": 3}
                ]
            },
            "Module 16": {
                "nom": "Électronique",
                "matieres": [
                    {"nom": "Électronique", "avec_tp": True, "coefficient": 3},
                    {"nom": "Électronique numérique", "avec_tp": True, "coefficient": 2}
                ]
            },
            "Module 17": {
                "nom": "Langues",
                "matieres": [
                    {"nom": "Technique d'Expression 1", "avec_tp": False, "coefficient": 2},
                    {"nom": "Anglais 3", "avec_tp": False, "coefficient": 2}
                ]
            }
        },
        "Semestre 4": {
            "Module 18": {
                "nom": "Bases de Données Avancées",
                "matieres": [
                    {"nom": "Modélisation et conception de Base de Données objets", "avec_tp": True, "coefficient": 3},
                    {"nom": "Cryptographie et sécurité des Systèmes d'information", "avec_tp": False, "coefficient": 3}
                ]
            },
            "Module 19": {
                "nom": "Génie Logiciel",
                "matieres": [
                    {"nom": "Atelier de génie logiciel", "avec_tp": True, "coefficient": 3}
                ]
            },
            "Module 20": {
                "nom": "Algorithmes et Mathématiques",
                "matieres": [
                    {"nom": "Programmation sur appareils mobiles", "avec_tp": False, "coefficient": 3},
                    {"nom": "Analyse et complexité des algorithmes", "avec_tp": False, "coefficient": 3},
                    {"nom": "Théorie des Graphes", "avec_tp": True, "coefficient": 2},
                    {"nom": "Analyse Numérique", "avec_tp": True, "coefficient": 3}
                ]
            },
            "Module 21": {
                "nom": "Réseaux et Web",
                "matieres": [
                    {"nom": "Développement web II", "avec_tp": True, "coefficient": 3},
                    {"nom": "Gestion et Administration Réseaux", "avec_tp": True, "coefficient": 3}
                ]
            },
            "Module 22": {
                "nom": "Gestion et Expression",
                "matieres": [
                    {"nom": "Technique d'Expression 2", "avec_tp": False, "coefficient": 2},
                    {"nom": "Organisation et gestion des Entreprises", "avec_tp": False, "coefficient": 2}
                ]
            },
            "Module 23": {
                "nom": "Stage",
                "matieres": [
                    {"nom": "Mini Projet d'intégration / Stage Ouvrier", "avec_tp": True, "coefficient": 5}
                ]
            }
        }
    },
    "Niveau 3": {
        "Semestre 5": {
            "Parcours Génie Logiciel": {
                "UE15": {
                    "nom": "Architecture et Système",
                    "matieres": [
                        {"nom": "Interfaces et multimédia", "avec_tp": True, "coefficient": 3},
                        {"nom": "Systèmes Distribués", "avec_tp": True, "coefficient": 3}
                    ]
                },
                "UE65": {
                    "nom": "Systèmes d'information",
                    "matieres": [
                        {"nom": "Base de Données Avancées", "avec_tp": True, "coefficient": 3},
                        {"nom": "Introduction à l'Analyse des Données (Datamining)", "avec_tp": True, "coefficient": 3}
                    ]
                },
                "UE25": {
                    "nom": "Algorithme et Programmation",
                    "matieres": [
                        {"nom": "Programmation système et réseaux", "avec_tp": True, "coefficient": 3},
                        {"nom": "Conception et implémentation d'applications objets", "avec_tp": True, "coefficient": 3}
                    ]
                },
                "UE75": {
                    "nom": "Génie Logiciel et Internet",
                    "matieres": [
                        {"nom": "Analyse des besoins et spécifications logiciels", "avec_tp": True, "coefficient": 3},
                        {"nom": "Laboratoire d'Internet", "avec_tp": True, "coefficient": 3}
                    ]
                },
                "UE55": {
                    "nom": "Socio-économique",
                    "matieres": [
                        {"nom": "Droit de Travail", "avec_tp": False, "coefficient": 2},
                        {"nom": "Entrepreneuriat", "avec_tp": False, "coefficient": 2},
                        {"nom": "Gestion de Projet", "avec_tp": False, "coefficient": 2}
                    ]
                }
            },
            "Parcours Réseaux et Internet": {
                "UE15": {
                    "nom": "Architecture et Système",
                    "matieres": [
                        {"nom": "Interfaces et multimédia", "avec_tp": True, "coefficient": 3},
                        {"nom": "Systèmes informatiques répartis (Système distribué)", "avec_tp": True, "coefficient": 3}
                    ]
                },
                "UE65": {
                    "nom": "Systèmes d'information",
                    "matieres": [
                        {"nom": "Base de Données Avancées", "avec_tp": True, "coefficient": 3},
                        {"nom": "Analyse des Données (Datamining)", "avec_tp": True, "coefficient": 3}
                    ]
                },
                "UE25": {
                    "nom": "Algorithme et Programmation",
                    "matieres": [
                        {"nom": "Programmation système et réseaux", "avec_tp": True, "coefficient": 3},
                        {"nom": "Conception et implémentation d'applications objets", "avec_tp": True, "coefficient": 3}
                    ]
                },
                "UE75": {
                    "nom": "Réseaux et Internet",
                    "matieres": [
                        {"nom": "Sécurité des réseaux Informatiques", "avec_tp": True, "coefficient": 3},
                        {"nom": "Laboratoire d'Internet", "avec_tp": True, "coefficient": 3}
                    ]
                },
                "UE55": {
                    "nom": "Socio-économique",
                    "matieres": [
                        {"nom": "Droit de Travail", "avec_tp": False, "coefficient": 2},
                        {"nom": "Compétences en Entrepreneuriales", "avec_tp": False, "coefficient": 2},
                        {"nom": "Gestion de Projet", "avec_tp": False, "coefficient": 2}
                    ]
                }
            }
        },
        "Semestre 6": {
            "Parcours Génie Logiciel": {
                "UE86": {
                    "nom": "Génie logiciel",
                    "matieres": [
                        {"nom": "Contrôle qualité et métrique du logiciel", "avec_tp": True, "coefficient": 3},
                        {"nom": "Génie logiciel orienté objet", "avec_tp": True, "coefficient": 3},
                        {"nom": "Développement web avancé (web services)", "avec_tp": True, "coefficient": 3}
                    ]
                },
                "UE96": {
                    "nom": "Projet Etudiant et Stage",
                    "matieres": [
                        {"nom": "Projet professionnel et Personnel", "avec_tp": True, "coefficient": 9},
                        {"nom": "Stage de fin de formation", "avec_tp": False, "coefficient": 12}
                    ]
                }
            },
            "Parcours Réseaux et Internet": {
                "Module 36": {
                    "nom": "Réseaux Avancés",
                    "matieres": [
                        {"nom": "Sécurité avancée des réseaux", "avec_tp": True, "coefficient": 3},
                        {"nom": "Administration avancée réseaux", "avec_tp": True, "coefficient": 3},
                        {"nom": "Cloud Computing", "avec_tp": True, "coefficient": 3}
                    ]
                },
                "Module 37": {
                    "nom": "Stage de Fin de Formation",
                    "matieres": [
                        {"nom": "Projet professionnel et Personnel / Stage de fin de formation", "avec_tp": True, "coefficient": 10}
                    ]
                }
            }
        }
    }
}

# Coefficients de calcul
CALCUL_COEFFICIENTS = {
    "avec_tp": {
        "cc": 0.30,
        "examen": 0.60,
        "tp": 0.40
    },
    "sans_tp": {
        "cc": 0.40,
        "examen": 0.60,
        "tp": 0.0
    }
}

# Seuil de validation
SEUIL_VALIDATION = 10.0
