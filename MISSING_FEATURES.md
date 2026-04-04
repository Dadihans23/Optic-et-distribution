# Fonctionnalités manquantes — Web vs Mobile Admin

> Recensement des fonctionnalités présentes dans l'app mobile admin
> qui ne sont **pas encore** implémentées dans le panneau admin web.
> Date : 2026-03-22

---

## 1. Écran Identifiants boutiques (`admin_credentials_screen.dart`)

> Pas d'équivalent côté web.

| Fonctionnalité | Description |
|---|---|
| Liste des identifiants | Affiche toutes les boutiques avec leur numéro de téléphone et leur mot de passe |
| Afficher/masquer le mot de passe | Icône œil pour révéler le mot de passe en clair |
| Copier le téléphone | Bouton copie dans le presse-papier |
| Copier le mot de passe | Bouton copie (uniquement quand le mot de passe est visible) |
| Recherche | Filtrer par nom de boutique ou numéro de téléphone |
| Archiver une boutique | Bouton archivage avec confirmation → masque la boutique |

---

## 2. Modification d'une commande (`admin_detail_order.dart`)

> Le web affiche le détail mais ne permet **pas l'édition**.

| Fonctionnalité | Description |
|---|---|
| Mode édition | Bouton bascule pour passer en mode édition |
| Modifier le porteur | Champ éditable pour le nom du porteur |
| Modifier la prescription | Champs éditables OD/OG (Sph, Cyl, Axe, Add) |
| Modifier type de verre | Champ éditable |
| Modifier le traitement | Champ éditable |
| Archiver une commande | Bouton archivage avec confirmation |

---

## 3. Export PDF "Fiche Finale" — Commandes (`all_orders_screen_admin.dart`)

> Le web ne génère aucun rapport global sur les commandes.

| Fonctionnalité | Description |
|---|---|
| Recherche texte | Filtrer par nom boutique, nom porteur ou numéro de commande |
| Filtre par date | Sélecteur de plage de dates (début / fin) |
| Génération PDF "Fiche Finale" | Rapport PDF de toutes les commandes de la période avec : en-tête entreprise, total commandes, tableau complet (boutique, porteur, prescription OD/OG, type verre, traitement) |
| Partage du PDF | Export via la feuille de partage système (email, messagerie…) |

---

## 4. Export PDF "Fiche Finale" — Bons de livraison (`admin_delivery_requests_screen.dart`)

> Le web génère un bon individuel mais pas de rapport global sur une période.

| Fonctionnalité | Description |
|---|---|
| Filtre par date | Sélecteur de plage de dates (début / fin) |
| Effacer les filtres | Bouton reset |
| Génération PDF "Fiche Finale" | Rapport PDF de tous les bons de la période avec : logo entreprise, en-tête avec RCCM/NCC, total bons, tableau détaillé par bon (prescription, type verre, traitement) |
| Partage du PDF | Export via la feuille de partage système |

---

## 5. Notifications push (`admin_detail_order.dart`)

> Pas d'équivalent côté web.

| Fonctionnalité | Description |
|---|---|
| Notification au changement de statut | Quand l'admin change le statut d'une commande, une notification push est envoyée automatiquement à la boutique concernée via OneSignal |
| Contenu de la notification | Inclut le nouveau statut et le numéro de commande |

---

## 6. Gestion des informations entreprise

> Probablement un écran dédié dans le mobile (company_info ou similaire). Non implémenté côté web.

| Fonctionnalité | Description |
|---|---|
| Modifier le nom de l'entreprise | Champ éditable |
| Modifier l'adresse | Champ éditable |
| Modifier le téléphone | Champ éditable |
| Modifier le RCCM / NCC | Champ éditable |
| Modifier la description (sous-titre PDF) | Champ éditable |
| Sauvegarder dans Firestore | Mise à jour du document `company_info/company_info` |

---

## Récapitulatif par priorité suggérée

| Priorité | Fonctionnalité | Effort estimé |
|---|---|---|
| 🔴 Haute | Export PDF "Fiche Finale" commandes + livraisons | Moyen |
| 🔴 Haute | Modification d'une commande (prescription, porteur) | Moyen |
| 🟠 Moyenne | Identifiants boutiques (liste + copie + archivage) | Faible |
| 🟠 Moyenne | Infos entreprise modifiables | Faible |
| 🟡 Basse | Notifications push (nécessite intégration OneSignal) | Élevé |
| 🟡 Basse | Archivage commandes | Faible |
