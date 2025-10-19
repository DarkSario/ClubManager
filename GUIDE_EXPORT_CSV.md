# Guide d'Export CSV - ClubManager

## Nouvelle fonctionnalité : Export CSV amélioré

### Qu'est-ce qui a changé ?

L'export CSV a été amélioré pour résoudre les problèmes d'affichage où toutes les données apparaissaient dans une seule colonne lors de l'ouverture dans Excel ou LibreOffice.

### Caractéristiques principales

#### 1. Choix du séparateur de colonnes

Lors de chaque export CSV, vous pouvez maintenant choisir le séparateur :

- **Point-virgule (;)** - Recommandé pour Excel France et LibreOffice en France
  - C'est le séparateur par défaut en France
  - Idéal si vous utilisez Excel configuré en français
  
- **Virgule (,)** - Standard international
  - Recommandé pour Excel anglais ou applications internationales
  - Utilisé par défaut dans les pays anglo-saxons
  
- **Tabulation** - Pour import avancé
  - Utile pour importer dans des outils techniques
  - Garantit la compatibilité avec la plupart des outils

#### 2. Gestion automatique des caractères spéciaux

Le système gère maintenant automatiquement :

- **Virgules dans les données** : Les champs contenant des virgules sont automatiquement protégés par des guillemets
- **Guillemets dans les données** : Les guillemets sont doublés selon la norme CSV (un guillemet `"` devient deux guillemets `""`)
- **Retours à la ligne** : Les champs contenant des retours à la ligne sont préservés
- **Caractères accentués** : Support complet de l'UTF-8 (é, è, ê, ô, ü, etc.)

#### 3. Option BOM UTF-8 pour Excel Windows

Si vous utilisez Excel sur Windows et que les accents ne s'affichent pas correctement :

1. Cochez l'option **"Ajouter BOM UTF-8"** lors de l'export
2. Cette option ajoute un marqueur au début du fichier qui aide Excel Windows à détecter l'encodage UTF-8
3. Idéal pour la compatibilité avec Excel 2010-2019 sur Windows

#### 4. En-têtes en français

Tous les exports CSV incluent maintenant des en-têtes traduits en français :
- `last_name` → `Nom`
- `first_name` → `Prénom`
- `mail` → `Email`
- `rgpd` → `Consentement RGPD`
- etc.

### Comment utiliser la nouvelle fonctionnalité

1. **Accéder à l'export** : Cliquez sur le bouton "Exporter CSV" dans l'onglet approprié (Membres, Postes, Cotisations, etc.)

2. **Choisir le type de données** : Sélectionnez ce que vous souhaitez exporter

3. **Configurer l'export** : Une fenêtre de dialogue s'ouvre avec les options :
   - Sélectionnez le séparateur approprié pour votre usage
   - Cochez "Ajouter BOM UTF-8" si nécessaire (pour Excel Windows)

4. **Sauvegarder** : Choisissez l'emplacement et le nom du fichier CSV

5. **Ouvrir dans Excel/LibreOffice** : Le fichier s'ouvre maintenant correctement avec chaque donnée dans sa colonne

### Recommandations

#### Pour Excel France / LibreOffice France
- Utilisez le séparateur **point-virgule (;)**
- Pas besoin d'activer le BOM sauf si les accents ne s'affichent pas

#### Pour Excel Windows (version ancienne)
- Utilisez le séparateur **point-virgule (;)**
- **Activez l'option BOM UTF-8** si les caractères accentués ne s'affichent pas correctement

#### Pour Excel anglais / international
- Utilisez le séparateur **virgule (,)**
- Le BOM n'est généralement pas nécessaire

#### Pour import dans d'autres outils
- Commencez avec **point-virgule (;)**
- Si cela ne fonctionne pas, essayez **tabulation (\t)**

### Dépannage

**Problème** : Les données sont toujours dans une seule colonne
- **Solution** : Essayez un autre séparateur. Excel français utilise le point-virgule (;), Excel anglais utilise la virgule (,)

**Problème** : Les accents s'affichent mal (é → Ã©)
- **Solution** : Réexportez le fichier avec l'option "Ajouter BOM UTF-8" activée

**Problème** : Les guillemets ou virgules cassent la structure
- **Solution** : Ce problème est maintenant résolu automatiquement. Si vous rencontrez toujours ce problème, contactez le support.

### Support

Si vous rencontrez des problèmes avec l'export CSV :
1. Vérifiez que vous utilisez le bon séparateur pour votre logiciel
2. Essayez l'option BOM UTF-8 pour Excel Windows
3. Ouvrez le fichier avec un éditeur de texte pour vérifier son contenu
4. Contactez le support technique si le problème persiste
