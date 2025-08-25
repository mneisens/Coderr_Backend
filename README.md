# Coderr Backend

Django REST Framework Backend für die Coderr Plattform.


### Voraussetzungen
- Python 3.8+
- pip

### Installation

1. **Repository klonen**
```bash
git clone <repository-url>
cd Coderr_Backend
```

2. **Virtuelle Umgebung erstellen**
```bash
python -m venv env
source env/bin/activate  # macOS/Linux
# env\Scripts\activate   # Windows
```

3. **Abhängigkeiten installieren**
```bash
pip install -r requirements.txt
```

4. **Datenbank einrichten**
```bash
python manage.py migrate
```

5. **Superuser erstellen (optional)**
```bash
python manage.py createsuperuser
```

6. **Server starten**
```bash
python manage.py runserver
```

Der Server läuft dann unter: `http://localhost:8000`

## 📚 API Endpunkte

- **Admin:** `http://localhost:8000/admin/`
- **API Base:** `http://localhost:8000/api/`
- **Dokumentation:** Siehe separate API-Dokumentation

## 🔧 Entwicklung

### Code-Qualität prüfen
```bash
pip install flake8 autopep8
flake8 . --exclude=env,__pycache__,.git --max-line-length=120
```

### Code automatisch formatieren
```bash
autopep8 --in-place --recursive --aggressive --max-line-length=120 .
```

## 📁 Projektstruktur

```
Coderr_Backend/
├── auth_app/           # Authentifizierung
├── core/              # Django-Konfiguration
├── offers_app/        # Angebote
├── orders_app/        # Bestellungen
├── profiles_app/      # Benutzerprofile
├── reviews_app/       # Bewertungen
├── requirements.txt   # Abhängigkeiten
└── manage.py         # Django-Management
```

## 🛠️ Troubleshooting

### Port bereits in Verwendung
```bash
python manage.py runserver 8001  # Anderer Port
```

### Datenbank-Reset
```bash
python manage.py flush  # Daten löschen
python manage.py migrate  # Migrationen anwenden
```

## 📞 Support

Bei Problemen:
1. Logs prüfen
2. Django Debug-Toolbar verwenden
3. Issue im Repository erstellen
