"""
Système de calcul des notes pour les modules de génie logiciel
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from modules_config import MODULES_DATA, CALCUL_COEFFICIENTS, SEUIL_VALIDATION


@dataclass
class NoteMatiere:
    """Notes d'une matière"""
    cc: float
    examen: float
    tp: Optional[float] = None
    
    def calculer_moyenne(self, avec_tp: bool) -> float:
        """Calcule la moyenne de la matière selon les coefficients"""
        if avec_tp:
            if self.tp is None:
                raise ValueError("TP requis pour cette matière")
            coeffs = CALCUL_COEFFICIENTS["avec_tp"]
            total_weight = coeffs["cc"] + coeffs["examen"] + coeffs["tp"]
            return (self.cc * coeffs["cc"] + 
                    self.examen * coeffs["examen"] + 
                    self.tp * coeffs["tp"]) / total_weight
        else:
            coeffs = CALCUL_COEFFICIENTS["sans_tp"]
            total_weight = coeffs["cc"] + coeffs["examen"] + coeffs["tp"]
            return (self.cc * coeffs["cc"] + 
                    self.examen * coeffs["examen"]) / total_weight


@dataclass
class ResultatMatiere:
    """Résultat d'une matière"""
    nom: str
    notes: NoteMatiere
    moyenne: float
    coefficient: int
    valide: bool


@dataclass
class ResultatModule:
    """Résultat d'un module"""
    nom: str
    matieres: List[ResultatMatiere]
    moyenne: float
    valide: bool
    niveau: str
    semestre: str


class CalculateurNotes:
    """Calculateur de notes pour les modules"""
    
    def __init__(self):
        self.modules_data = MODULES_DATA
    
    def calculer_matiere(self, nom_matiere: str, notes: NoteMatiere, 
                        avec_tp: bool, coefficient: int) -> ResultatMatiere:
        """Calcule le résultat d'une matière"""
        moyenne = notes.calculer_moyenne(avec_tp)
        return ResultatMatiere(
            nom=nom_matiere,
            notes=notes,
            moyenne=round(moyenne, 2),
            coefficient=coefficient,
            valide=moyenne >= SEUIL_VALIDATION
        )
    
    def calculer_module(self, niveau: str, semestre: str, module_id: str,
                       notes_matieres: Dict[str, NoteMatiere]) -> ResultatModule:
        """Calcule le résultat d'un module complet"""
        module_data = self.modules_data[niveau][semestre][module_id]
        resultats_matieres = []
        
        total_coeff = 0
        somme_ponderee = 0
        
        for matiere in module_data["matieres"]:
            nom_matiere = matiere["nom"]
            if nom_matiere in notes_matieres:
                resultat = self.calculer_matiere(
                    nom_matiere,
                    notes_matieres[nom_matiere],
                    matiere["avec_tp"],
                    matiere["coefficient"]
                )
                resultats_matieres.append(resultat)
                total_coeff += resultat.coefficient
                somme_ponderee += resultat.moyenne * resultat.coefficient
        
        moyenne_module = somme_ponderee / total_coeff if total_coeff > 0 else 0
        
        return ResultatModule(
            nom=module_data["nom"],
            matieres=resultats_matieres,
            moyenne=round(moyenne_module, 2),
            valide=moyenne_module >= SEUIL_VALIDATION,
            niveau=niveau,
            semestre=semestre
        )
    
    def calculer_module_with_parcours(self, niveau: str, semestre: str, parcours: Optional[str],
                                      module_id: str, notes_matieres: Dict[str, NoteMatiere]) -> ResultatModule:
        """Calcule le résultat d'un module avec support des parcours (Niveau 3)"""
        # Accéder aux données du module selon la structure
        if parcours and niveau == "Niveau 3":
            module_data = self.modules_data[niveau][semestre][parcours][module_id]
        else:
            module_data = self.modules_data[niveau][semestre][module_id]
        
        resultats_matieres = []
        
        total_coeff = 0
        somme_ponderee = 0
        
        for matiere in module_data["matieres"]:
            nom_matiere = matiere["nom"]
            if nom_matiere in notes_matieres:
                resultat = self.calculer_matiere(
                    nom_matiere,
                    notes_matieres[nom_matiere],
                    matiere["avec_tp"],
                    matiere["coefficient"]
                )
                resultats_matieres.append(resultat)
                total_coeff += resultat.coefficient
                somme_ponderee += resultat.moyenne * resultat.coefficient
        
        moyenne_module = somme_ponderee / total_coeff if total_coeff > 0 else 0
        
        return ResultatModule(
            nom=module_data["nom"],
            matieres=resultats_matieres,
            moyenne=round(moyenne_module, 2),
            valide=moyenne_module >= SEUIL_VALIDATION,
            niveau=niveau,
            semestre=semestre
        )
    
    def calculer_tous_modules(self, notes_par_module: Dict[str, Dict[str, NoteMatiere]]) -> Dict[str, List[ResultatModule]]:
        """Calcule tous les modules pour un étudiant"""
        resultats = {}
        
        for niveau, semestres in self.modules_data.items():
            resultats[niveau] = []
            for semestre, content in semestres.items():
                # On vérifie si ce semestre contient des parcours (comme Niveau 3)
                # ou s'il s'agit directement de modules
                has_parcours = False
                first_key = list(content.keys())[0] if content else None
                if first_key and "matieres" not in content[first_key]:
                    has_parcours = True

                if has_parcours:
                    for parcours, modules in content.items():
                        for module_id in modules:
                            if module_id in notes_par_module:
                                resultat = self.calculer_module_with_parcours(
                                    niveau,
                                    semestre,
                                    parcours,
                                    module_id,
                                    notes_par_module[module_id]
                                )
                                resultats[niveau].append(resultat)
                else:
                    for module_id in content:
                        if module_id in notes_par_module:
                            resultat = self.calculer_module(
                                niveau,
                                semestre,
                                module_id,
                                notes_par_module[module_id]
                            )
                            resultats[niveau].append(resultat)
        
        return resultats
    
    def obtenir_liste_matieres(self, niveau: str, semestre: str, module_id: str) -> List[Dict]:
        """Retourne la liste des matières d'un module"""
        return self.modules_data[niveau][semestre][module_id]["matieres"]
    
    def obtenir_tous_modules(self) -> Dict[str, Dict[str, Dict[str, Dict]]]:
        """Retourne tous les modules disponibles"""
        return self.modules_data


def generer_rapport(resultats: Dict[str, List[ResultatModule]]) -> str:
    """Génère un rapport texte des résultats"""
    rapport = []
    
    for niveau, modules in resultats.items():
        rapport.append(f"\n{'='*60}")
        rapport.append(f"{niveau}")
        rapport.append(f"{'='*60}")
        
        for module in modules:
            rapport.append(f"\n📚 {module.nom} ({module.semestre})")
            rapport.append(f"   Moyenne: {module.moyenne}/20")
            rapport.append(f"   Statut: {'✅ VALIDÉ' if module.valide else '❌ NON VALIDÉ'}")
            rapport.append(f"\n   Matières:")
            
            for matiere in module.matieres:
                rapport.append(f"   • {matiere.nom}")
                rapport.append(f"     CC: {matiere.notes.cc}/20")
                if matiere.notes.tp is not None:
                    rapport.append(f"     TP: {matiere.notes.tp}/20")
                rapport.append(f"     Examen: {matiere.notes.examen}/20")
                rapport.append(f"     Moyenne: {matiere.moyenne}/20 (Coef: {matiere.coefficient})")
                rapport.append(f"     Statut: {'✅' if matiere.valide else '❌'}")
    
    return "\n".join(rapport)
