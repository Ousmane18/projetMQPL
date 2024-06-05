import unittest
from datetime import datetime
from gestion_projet import (
    Projet,
    Membre,
    Tache,
    Risque,
    Jalon,
    Changement,
    EmailNotificationStrategy,
    SMSNotificationStrategy,
    PushNotificationStrategy,
)


class TestProjet(unittest.TestCase):
    def setUp(self):
        self.projet = Projet(
            "FRAISEN",
            "LA CRÉATION DU RÉSEAU FRAISEN A COMME BUT D'UNIFIER ET D'ACCOMPAGNER LES PRODUCTEURS DE FRAISES EN AFRIQUE SOUS UN LABEL DE QUALITÉ UNIQUE",
            datetime(2024, 1, 1),
            datetime(2024, 12, 31),
        )
        self.membre1 = Membre("Ousmane Mbathie", "Manager")
        self.membre2 = Membre("Oumar boune Khatabe Thiam", "Développeur")
        self.membre3 = Membre("Mouhamed Koné", "Designer")

    def test_ajouter_membre_equipe(self):
        self.projet.ajouter_membre_equipe("Ousmane Mbathie")
        self.assertIn("Ousmane Mbathie", self.projet.equipe)

    def test_ajouter_tache(self):
        tache = Tache(
            "Analyse des besoins",
            "Analyse complète",
            datetime(2024, 1, 1),
            datetime(2024, 1, 15),
            self.membre1,
            "Non commencée",
        )
        self.projet.ajouter_tache(tache)
        self.assertIn(tache, self.projet.taches)

    def test_definir_budget(self):
        self.projet.definir_budget(700000)
        self.assertEqual(self.projet.budget, 700000)

    def test_ajouter_risque(self):
        risque = Risque("Retard de livraison", 0.3, "Moyen")
        self.projet.ajouter_risque(risque)
        self.assertIn(risque, self.projet.risques)

    def test_ajouter_jalon(self):
        jalon = Jalon("Phase 1 terminée", datetime(2024, 6, 1))
        self.projet.ajouter_jalon(jalon)
        self.assertIn(jalon, self.projet.jalons)

    def test_enregistrer_changement(self):
        self.projet.enregistrer_changement("Changement de la portée du projet", 2)
        self.assertIn(
            "Changement de la portée du projet (version 2)", self.projet.changements
        )

    def test_generer_rapport_performance(self):
        rapport = self.projet.generer_rapport_performance()
        self.assertIn("Rapport d'activité du projet", rapport)

    def test_set_notification_strategy(self):
        self.projet.set_notification_strategy(SMSNotificationStrategy())
        self.assertIsInstance(
            self.projet.notification_context._strategy, SMSNotificationStrategy
        )
        self.projet.set_notification_strategy(PushNotificationStrategy())
        self.assertIsInstance(
            self.projet.notification_context._strategy, PushNotificationStrategy
        )

    def test_calculer_chemin_critique(self):
        tache1 = Tache(
            "Tâche 1",
            "Description de la tâche 1",
            datetime(2024, 2, 1),
            datetime(2024, 3, 1),
            self.membre1,
            "Non commencée",
        )
        tache2 = Tache(
            "Tâche 2",
            "Description de la tâche 2",
            datetime(2024, 3, 2),
            datetime(2024, 4, 2),
            self.membre2,
            "Non commencée",
        )
        tache3 = Tache(
            "Tâche 3",
            "Description de la tâche 3",
            datetime(2024, 4, 3),
            datetime(2024, 5, 3),
            self.membre3,
            "Non commencée",
        )
        tache2.ajouter_dependance(tache1)
        tache3.ajouter_dependance(tache2)
        self.projet.ajouter_tache(tache1)
        self.projet.ajouter_tache(tache2)
        self.projet.ajouter_tache(tache3)
        chemin_critique = self.projet.calculer_chemin_critique()
        self.assertEqual(chemin_critique, ["Tâche 1", "Tâche 2", "Tâche 3"])


if __name__ == "__main__":
    unittest.main()
