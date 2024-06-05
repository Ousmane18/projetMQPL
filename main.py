from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

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
    def __init__(self, nom: str, description: str, date_debut: datetime, date_fin: datetime, responsable: Membre, statut: str):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.responsable = responsable
        self.statut = statut
        self.dependances: List[Tache] = []

    def ajouter_dependance(self, tache: 'Tache'):
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
    def __init__(self, nom: str, description: str, date_debut: datetime, date_fin: datetime):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.taches: List[Tache] = []
        self.equipe = Equipe()
        self.budget = 0.0
        self.risques: List[Risque] = []
        self.jalons: List[Jalon] = []
        self.version = 1
        self.changements: List[Changement] = []
        self.chemin_critique: List[Tache] = []
        self.notification_context: NotificationContext = None

    def set_notification_strategy(self, strategy: NotificationStrategy):
        self.notification_context = NotificationContext(strategy)

    def ajouter_tache(self, tache: Tache):
        self.taches.append(tache)
        self.notifier(f"Nouvelle tâche ajoutée: {tache.nom}", self.equipe.obtenir_membres())

    def ajouter_membre_equipe(self, membre: Membre):
        self.equipe.ajouter_membre(membre)
        self.notifier(f"{membre.nom} a été ajouté à l'équipe", [membre])

    def definir_budget(self, budget: float):
        self.budget = budget
        self.notifier(f"Le budget du projet a été défini à {budget} Unité Monétaire", self.equipe.obtenir_membres())

    def ajouter_risque(self, risque: Risque):
        self.risques.append(risque)
        self.notifier(f"Nouveau risque ajouté: {risque.description}", self.equipe.obtenir_membres())

    def ajouter_jalon(self, jalon: Jalon):
        self.jalons.append(jalon)
        self.notifier(f"Nouveau jalon ajouté: {jalon.nom}", self.equipe.obtenir_membres())

    def enregistrer_changement(self, description: str):
        changement = Changement(description, self.version, datetime.now())
        self.changements.append(changement)
        self.version += 1
        self.notifier(f"Changement enregistré: {description} (version {self.version})", self.equipe.obtenir_membres())

    def calculer_chemin_critique(self):
        # Initialiser les temps au plus tôt et au plus tard
        for tache in self.taches:
            tache.early_start = 0
            tache.early_finish = 0
            tache.late_start = float('inf')
            tache.late_finish = float('inf')

        # Calcul des temps au plus tôt
        for tache in self.taches:
            if not tache.dependances:
                tache.early_finish = (tache.date_fin - tache.date_debut).days
            else:
                tache.early_start = max([dep.early_finish for dep in tache.dependances])
                tache.early_finish = tache.early_start + (tache.date_fin - tache.date_debut).days

        # Calcul des temps au plus tard (on commence par la fin du projet)
        project_duration = max(tache.early_finish for tache in self.taches)
        for tache in reversed(self.taches):
            if tache.late_finish == float('inf'):
                tache.late_finish = project_duration
            tache.late_start = tache.late_finish - (tache.date_fin - tache.date_debut).days
            for dep in tache.dependances:
                dep.late_finish = min(dep.late_finish, tache.late_start)

        # Identifier le chemin critique
        self.chemin_critique = [tache for tache in self.taches if tache.early_start == tache.late_start]

        # Afficher le chemin critique
        print("Chemin critique :")
        for tache in self.chemin_critique:
            print(f"{tache.nom} (début : {tache.early_start}, fin : {tache.early_finish})")

    def generer_rapport_performance(self):
        rapport = f"Rapport de performance du projet '{self.nom}':\n"
        rapport += f"Description: {self.description}\n"
        rapport += f"Dates: {self.date_debut} - {self.date_fin}\n"
        rapport += f"Budget: {self.budget} EUR\n"
        rapport += f"Version: {self.version}\n"
        rapport += f"Équipe: {[membre.nom for membre in self.equipe.obtenir_membres()]}\n"

        # Détails des tâches
        rapport += "\nTâches:\n"
        for tache in self.taches:
            rapport += f"- {tache.nom}: {tache.statut} (Début: {tache.date_debut}, Fin: {tache.date_fin}, Responsable: {tache.responsable.nom})\n"

        # Détails des risques
        rapport += "\nRisques:\n"
        for risque in self.risques:
            rapport += f"- {risque.description}: Probabilité {risque.probabilite}, Impact {risque.impact}\n"

        # Détails des jalons
        rapport += "\nJalons:\n"
        for jalon in self.jalons:
            rapport += f"- {jalon.nom}: {jalon.date}\n"

        # Détails des changements
        rapport += "\nChangements:\n"
        for changement in self.changements:
            rapport += f"- {changement.description}: Version {changement.version}, Date {changement.date}\n"

        print(rapport)

    def notifier(self, message: str, destinataires: List[Membre]):
        if self.notification_context:
            self.notification_context.notifier(message, [membre.nom for membre in destinataires])

# Créer des membres de l'équipe
membre1 = Membre("Ousmane", "Développeur")
membre2 = Membre("Oumar", "Chef de projet")
membre3 = Membre("Mouhamed", "Testeur")

# Créer une équipe et ajouter des membres
equipe = Equipe()
equipe.ajouter_membre(membre1)
equipe.ajouter_membre(membre2)
equipe.ajouter_membre(membre3)




# Créer un projet
projet = Projet("Nouveau Projet", "Description du projet", datetime(2024, 1, 1), datetime(2024, 12, 31))

# Définir une stratégie de notification par email
projet.set_notification_strategy(EmailNotificationStrategy())

# Ajouter des tâches au projet
tache1 = Tache("Tâche 1", "Description de la tâche 1", datetime(2024, 2, 1), datetime(2024, 3, 1), membre1, "Non commencée")
projet.ajouter_tache(tache1)

# Ajouter un risque
risque = Risque("Risque 1", 0.5, "Impact élevé")
projet.ajouter_risque(risque)

# Enregistrer un changement
projet.enregistrer_changement("Changement de version")

# Calculer le chemin critique
projet.calculer_chemin_critique()

# Générer un rapport de performance
projet.generer_rapport_performance()

# Afficher la liste des membres de l'équipe
print("\nListe des membres de l'équipe :")
for membre in projet.equipe.obtenir_membres():
    print(f"- {membre.nom}, {membre.role}")


# Enregistrer un changement
projet.enregistrer_changement("Changement de version")

# Calculer le chemin critique
projet.calculer_chemin_critique()

# Générer un rapport de performance
projet.generer_rapport_performance()


