# Coderr Backend

Django REST Framework Backend für die Coderr Plattform.


### Voraussetzungen
- Python 3.8+
- pip

### Installation

1. **Repository klonen**
```bash
git clone https://github.com/mneisens/Coderr_Backend.git
cd Coderr_Backend
```

2. **Virtuelle Umgebung erstellen**
```bash
python3 -m venv env
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
#Bei type: "customer" oder "busines" eingeben
```

6. **Server starten**
```bash
python manage.py runserver
```

Der Server läuft dann unter: `http://localhost:8000`

## API Endpunkte

- **Admin:** `http://localhost:8000/admin/`
- **API Base:** `http://localhost:8000/api/`
- **Dokumentation:** Siehe separate API-Dokumentation


## Projektstruktur

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

## Support

Bei Problemen:
1. Logs prüfen
2. Django Debug-Toolbar verwenden
3. Issue im Repository erstellen
