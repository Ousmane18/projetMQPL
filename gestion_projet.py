from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict, Callable, Any


class NotificationStrategy(ABC):
    @abstractmethod
    def envoyer(self, message: str, destinataire: str) -> None:
        pass


class EmailNotificationStrategy(NotificationStrategy):
    def envoyer(self, message: str, destinataire: str) -> None:
        print(f"Notification envoyée à {destinataire} par email: {message}")


class SMSNotificationStrategy(NotificationStrategy):
    def envoyer(self, message: str, destinataire: str) -> None:
        print(f"Notification envoyée à {destinataire} par SMS: {message}")


class PushNotificationStrategy(NotificationStrategy):
    def envoyer(self, message: str, destinataire: str) -> None:
        print(f"Notification envoyée à {destinataire} par push notification: {message}")


class NotificationContext:
    def __init__(self, strategy: NotificationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: NotificationStrategy):
        self._strategy = strategy

    def notifier(self, message: str, destinataires: List[str]) -> None:
        for destinataire in destinataires:
            self._strategy.envoyer(message, destinataire)


class Membre:
    def __init__(self, nom: str, role: str):
        self.nom = nom
        self.role = role


class Tache:
    def __init__(
        self,
        nom: str,
        description: str,
        date_debut: datetime,
        date_fin: datetime,
        responsable: Membre,
        statut: str,
    ):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.responsable = responsable
        self.statut = statut
        self.dependances: List[Tache] = []

    def ajouter_dependance(self, tache: "Tache"):
        self.dependances.append(tache)

    def mettre_a_jour_statut(self, statut: str):
        self.statut = statut


class Equipe:
    def __init__(self):
        self.membres: List[Membre] = []

    def ajouter_membre(self, membre: Membre):
        self.membres.append(membre)

    def obtenir_membres(self) -> List[Membre]:
        return self.membres


class Risque:
    def __init__(self, description: str, probabilite: float, impact: str):
        self.description = description
        self.probabilite = probabilite
        self.impact = impact


class Jalon:
    def __init__(self, nom: str, date: datetime):
        self.nom = nom
        self.date = date


class Changement:
    def __init__(self, description: str, version: int, date: datetime):
        self.description = description
        self.version = version
        self.date = date


class Projet:
    def __init__(
        self, nom: str, description: str, date_debut: datetime, date_fin: datetime
    ):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.taches: List[Tache] = []
        self.equipe: List[str] = []
        self.risques: List[Risque] = []
        self.jalons: List[Jalon] = []
        self.changements: List[str] = []
        self.notification_context = NotificationContext(EmailNotificationStrategy())
        self.activites: List[str] = []

    def set_notification_strategy(self, strategy: NotificationStrategy) -> None:
        self.notification_context = NotificationContext(strategy)

    def ajouter_membre_equipe(self, membre: str) -> None:
        self.equipe.append(membre)
        self.activites.append(f"Membre ajouté: {membre}")
        self.notification_context.notifier(
            f"{membre} a été ajouté à l'équipe", self.equipe
        )

    def ajouter_tache(self, tache: str) -> None:
        self.taches.append(tache)
        self.activites.append(f"Tâche ajoutée: {tache}")
        self.notification_context.notifier(
            f"Nouvelle tâche ajoutée: {tache}", self.equipe
        )

    def definir_budget(self, budget: float) -> None:
        self.budget = budget
        self.activites.append(f"Budget défini: {budget} Unité Monétaire")
        self.notification_context.notifier(
            f"Le budget du projet a été défini à {budget} Unité Monétaire", self.equipe
        )

    def ajouter_risque(self, risque: str) -> None:
        self.risques.append(risque)
        self.activites.append(f"Risque ajouté: {risque}")
        self.notification_context.notifier(
            f"Nouveau risque ajouté: {risque}", self.equipe
        )

    def ajouter_jalon(self, jalon: str) -> None:
        self.jalons.append(jalon)
        self.activites.append(f"Jalon ajouté: {jalon}")
        self.notification_context.notifier(
            f"Nouveau jalon ajouté: {jalon}", self.equipe
        )

    def enregistrer_changement(self, description: str, version: int) -> None:
        changement = f"{description} (version {version})"
        self.changements.append(changement)
        self.activites.append(f"Changement enregistré: {changement}")
        self.notification_context.notifier(
            f"Changement enregistré: {changement}", self.equipe
        )

    def calculer_chemin_critique(self) -> List[str]:
        # Utilisation de l'algorithme CPM pour calculer le chemin critique
        chemins: Dict[str, int] = (
            {}
        )  # Dictionnaire pour stocker les chemins avec leurs durées

        def dfs(tache: Tache, chemin: List[str], duree: int) -> None:
            chemin.append(tache.nom)
            duree += (tache.date_fin - tache.date_debut).days

            if not tache.dependances:
                chemins[" -> ".join(chemin)] = duree
            else:
                for dependance in tache.dependances:
                    dfs(dependance, chemin.copy(), duree)

        for tache in self.taches:
            if not tache.dependances:  # Si la tâche n'a pas de dépendances
                dfs(tache, [], 0)

        chemin_critique = max(chemins, key=lambda k: chemins[k])
        duree_critique = chemins[chemin_critique]

        print(
            f"Chemin critique: {chemin_critique} avec une durée de {duree_critique} jours"
        )
        return chemin_critique.split(" -> ")

    def generer_rapport_performance(self) -> str:
        rapport = f"Rapport d'activité du projet '{self.nom}':\n\n"
        rapport += f"Description: {self.description}\n"
        rapport += f"Date de début: {self.date_debut}\n"
        rapport += f"Date de fin: {self.date_fin}\n\n"
        rapport += "Activités:\n"
        for activite in self.activites:
            rapport += f"- {activite}\n"
        return rapport


projet = Projet(
    "FRAISEN",
    "LA CRÉATION DU RÉSEAU FRAISEN A COMME BUT D'UNIFIER ET D'ACCOMPAGNER LES PRODUCTEURS DE FRAISES EN AFRIQUE SOUS UN LABEL DE QUALITÉ UNIQUE",
    datetime(2024, 1, 1),
    datetime(2024, 12, 31),
)

# Ajouter des membres
projet.ajouter_membre_equipe("Ousmane Mbathie")
projet.ajouter_membre_equipe("Oumar boune Khatabe Thiam")
projet.ajouter_membre_equipe("Mouhamed Koné")

# Ajouter des tâches
projet.ajouter_tache("Analyse des besoins")
projet.ajouter_tache("Développement")

# Définir le budget
projet.definir_budget(700000)

# Ajouter des risques
projet.ajouter_risque("Retard de livraison")

# Ajouter des jalons
projet.ajouter_jalon("Phase 1 terminée")

# Enregistrer des changements
projet.enregistrer_changement("Changement de la portée du projet", 2)


# Générer le rapport de performance
rapport = projet.generer_rapport_performance()
print(rapport)
