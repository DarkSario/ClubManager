# SMTP Configuration and Mailing Workflow

## UI Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      Club Manager Main Window                    │
├─────────────────────────────────────────────────────────────────┤
│  Tabs: [Membres] [Postes] [Clubs MJC] [Exports] [Mailing] ...  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────┐                    ┌──────────────────────┐
│   Membres Tab       │                    │    Mailing Tab       │
├─────────────────────┤                    ├──────────────────────┤
│                     │                    │ [⚙ Configuration     │
│ [Ajouter]           │                    │  SMTP]               │
│ [Modifier]          │                    │                      │
│ [Supprimer]         │   Click "Ouvrir"   │ Help text: 📧 Mail   │
│ [Exporter]          │   ───────────────► │ groupé avec batch    │
│ [Ouvrir Mailing] ───┘                    │                      │
│                     │                    │ [Sélection           │
│ Member list...      │                    │  destinataires]      │
│                     │                    │                      │
└─────────────────────┘                    │ Objet: [________]    │
                                           │                      │
                                           │ Corps:               │
                                           │ ┌─────────────────┐ │
                                           │ │                 │ │
                                           │ │                 │ │
                                           │ └─────────────────┘ │
                                           │                      │
                                           │ [Prévisualiser]      │
                                           │ [Envoyer]            │
                                           │                      │
                                           │ Progress: [======   ]│
                                           └──────────────────────┘
                                                     │
                                                     │ Click ⚙
                                                     ▼
                                           ┌──────────────────────┐
                                           │ SMTP Settings Dialog │
                                           ├──────────────────────┤
                                           │ Serveur SMTP         │
                                           │ ├─ Hôte: [______]    │
                                           │ ├─ Port: [587   ]    │
                                           │ └─ Sécurité: [▼]     │
                                           │                      │
                                           │ Authentification     │
                                           │ ├─ User: [______]    │
                                           │ └─ Pass: [••••••]    │
                                           │                      │
                                           │ Expéditeur           │
                                           │ ├─ Email: [_____]    │
                                           │ ├─ Nom: [______]     │
                                           │ └─ Reply: [_____]    │
                                           │                      │
                                           │ Paramètres d'envoi   │
                                           │ ├─ Lot: [10    ]     │
                                           │ ├─ Délai: [1000]ms   │
                                           │ ├─ Retry: [2   ]     │
                                           │ └─ [✓] Logs          │
                                           │                      │
                                           │ ⚠️ Sécurité:          │
                                           │ APP_SECRET_KEY...    │
                                           │                      │
                                           │ [Tester connexion]   │
                                           │ [Envoyer test]       │
                                           │                      │
                                           │     [OK] [Annuler]   │
                                           └──────────────────────┘
```

## Database Schema

```
┌─────────────────────────────────┐
│          settings               │
├─────────────────────────────────┤
│ key TEXT PRIMARY KEY            │
│ value TEXT                      │
│ updated_at TEXT                 │
├─────────────────────────────────┤
│ smtp_host                       │
│ smtp_port                       │
│ smtp_security                   │
│ smtp_username                   │
│ smtp_password (encrypted)       │
│ smtp_from                       │
│ smtp_reply_to                   │
│ smtp_sender_name                │
│ smtp_batch_size                 │
│ smtp_batch_delay                │
│ smtp_max_retries                │
│ smtp_enable_logging             │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│        mailing_logs             │
├─────────────────────────────────┤
│ id INTEGER PRIMARY KEY          │
│ recipient_id INTEGER FK         │
│ recipient_email TEXT            │
│ subject TEXT                    │
│ status TEXT (sent/failed)       │
│ message_id TEXT                 │
│ error TEXT                      │
│ timestamp TEXT                  │
└─────────────────────────────────┘
```

## Sending Workflow

```
User clicks "Envoyer"
    │
    ▼
┌─────────────────────────┐
│ Validate form fields    │
│ - Subject not empty     │
│ - Body not empty        │
│ - Recipients selected   │
└───────┬─────────────────┘
        │
        ▼
┌─────────────────────────┐
│ Check SMTP config       │
│ - Load from database    │
│ - Decrypt password      │
└───────┬─────────────────┘
        │
        │ No config? ──────► Show error + link to settings
        │
        ▼ Config OK
┌─────────────────────────┐
│ Confirmation dialog     │
│ "Send to X recipients?" │
└───────┬─────────────────┘
        │
        ▼ User confirms
┌─────────────────────────┐
│ Initialize SMTPSender   │
│ - Connect to server     │
│ - Authenticate          │
└───────┬─────────────────┘
        │
        ▼
┌─────────────────────────────────┐
│ Send in batches                 │
│ For each batch (size N):        │
│   For each recipient:           │
│     - Create EmailMessage       │
│     - Try to send (with retry)  │
│     - Log result                │
│     - Update progress bar       │
│   Sleep delay_ms between batches│
└───────┬─────────────────────────┘
        │
        ▼
┌─────────────────────────┐
│ Show results dialog     │
│ - X sent successfully   │
│ - Y failed              │
│ - Details of failures   │
└─────────────────────────┘
```

## Security Flow

```
User enters password
    │
    ▼
┌──────────────────────────┐
│ SMTPConfig.encrypt()     │
│ - Get APP_SECRET_KEY     │
│ - Derive Fernet key      │
│ - Encrypt password       │
└───────┬──────────────────┘
        │
        ▼
┌──────────────────────────┐
│ Save to database         │
│ INSERT INTO settings     │
│ (key, value)             │
│ ('smtp_password',        │
│  'gAAAAAB...')           │
└───────┬──────────────────┘
        │
        ▼ Later when sending...
┌──────────────────────────┐
│ Load from database       │
│ SELECT value FROM        │
│ settings WHERE           │
│ key='smtp_password'      │
└───────┬──────────────────┘
        │
        ▼
┌──────────────────────────┐
│ SMTPConfig.decrypt()     │
│ - Get APP_SECRET_KEY     │
│ - Derive Fernet key      │
│ - Decrypt password       │
└───────┬──────────────────┘
        │
        ▼
    Use for SMTP auth
```

## Error Handling

```
┌────────────────────────────────────────┐
│ Possible Errors & Handling             │
├────────────────────────────────────────┤
│                                        │
│ 1. SMTP Not Configured                 │
│    ├─► Show warning dialog             │
│    └─► Offer to open settings          │
│                                        │
│ 2. Connection Failed                   │
│    ├─► Show error message              │
│    ├─► Display error details           │
│    └─► Suggest checking settings       │
│                                        │
│ 3. Authentication Failed               │
│    ├─► Show clear error                │
│    └─► Suggest password update         │
│                                        │
│ 4. Send Failure (per recipient)        │
│    ├─► Retry up to max_retries         │
│    ├─► Log to mailing_logs             │
│    └─► Include in failure report       │
│                                        │
│ 5. Partial Batch Failure               │
│    ├─► Continue with next batch        │
│    └─► Report all results at end       │
│                                        │
└────────────────────────────────────────┘
```

## Component Architecture

```
┌──────────────────────────────────────────────────────┐
│                  club_manager/                       │
├──────────────────────────────────────────────────────┤
│                                                      │
│  core/                                               │
│  ├─ smtp_util.py                                     │
│  │  ├─ SMTPConfig (encryption, config mgmt)         │
│  │  ├─ SMTPSender (sending logic, batching, retry)  │
│  │  ├─ get_smtp_config_from_db()                    │
│  │  └─ save_smtp_config_to_db()                     │
│  │                                                   │
│  ├─ database.py                                      │
│  │  ├─ setup_schema() [+settings, +mailing_logs]    │
│  │  └─ migrate_schema()                             │
│  │                                                   │
│  └─ [other core modules...]                         │
│                                                      │
│  ui/                                                 │
│  ├─ smtp_settings_dialog.py                         │
│  │  └─ SMTPSettingsDialog (UI for SMTP config)     │
│  │                                                   │
│  ├─ mailing_tab.py                                   │
│  │  └─ MailingTab [+SMTP button, +progress bar]    │
│  │                                                   │
│  ├─ members_tab.py                                   │
│  │  └─ MembersTab [modified mailing button]        │
│  │                                                   │
│  └─ [other UI modules...]                           │
│                                                      │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│                     tests/                           │
├──────────────────────────────────────────────────────┤
│  test_smtp_util.py                                   │
│  ├─ TestSMTPConfig (encryption tests)                │
│  ├─ TestSMTPSender (connection, sending tests)       │
│  └─ TestSMTPConfigDatabase (persistence tests)       │
└──────────────────────────────────────────────────────┘
```
