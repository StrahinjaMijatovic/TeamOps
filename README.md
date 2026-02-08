# TeamOps

Alat za upravljanje projektima i zadacima inspirisan Jira/Trello sistemima. Izgradjen sa Django framework-om, PostgreSQL bazom podataka i Docker kontejnerima.

## Tech Stack

- **Backend:** Django 5.0, Python 3.11
- **Baza podataka:** PostgreSQL 14
- **Frontend:** Django Templates, Bootstrap 5, Crispy Forms
- **Kontejnerizacija:** Docker, Docker Compose
- **Sigurnost:** django-axes (brute-force zastita)

## Funkcionalnosti

### Korisnici i uloge
- Registracija i prijava korisnika
- Tri uloge: **Admin**, **Team Member**, **Viewer**
- Admin panel za upravljanje ulogama korisnika (`/accounts/users/`)
- Password reset putem email-a
- Zastita od brute-force napada (zakljucavanje nakon 5 neuspesnih pokusaja)

### Projekti
- Kreiranje, uredjivanje i brisanje projekata
- Svaki projekat ima unikatni kljuc (npr. `TEAM`)
- Status projekta: Active, Archived
- Upravljanje clanovima projekta (dodavanje/uklanjanje)
- Paginacija liste projekata

### Kanban Board
- Svaki projekat automatski dobija Board sa kolonama (To Do, In Progress, Done)
- Drag-and-drop premjestanje zadataka izmedju kolona
- Kreiranje, uredivanje i brisanje zadataka
- Prioriteti zadataka: Low, Medium, High, Critical
- Labele za kategorizaciju (Bug, Feature, Enhancement, Documentation, Urgent)
- Dodela zadataka clanovima projekta
- Due date za rokove

### Audit Log
- Automatsko pracenje svih promena na projektima i zadacima
- Beleske o kreiranju, azuriranju i brisanju
- Pracenje specificnih izmjena polja (stara vs nova vriednost)
- Pregled audit log-a na stranici projekta

### Kontrola pristupa
- **Admin** - pun pristup, upravljanje ulogama korisnika
- **Team Member** - kreiranje/uredjivanje projekata i zadataka
- **Viewer** - samo pregled, bez mogucnosti kreiranja ili uredivanja

## Struktura projekta

```
TeamOps/
├── accounts/          # Custom User model, registracija, upravljanje ulogama
├── projects/          # Projekti, Boardovi, Kolone
├── tasks/             # Zadaci, Labele
├── audit/             # Audit logovi (signals)
├── config/            # Django settings, root URLs
├── templates/         # HTML templejti (Bootstrap 5)
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
└── manage.py
```

## API Endpoints

| URL | Opis |
|-----|------|
| `/` | Pocetna stranica |
| `/accounts/register/` | Registracija |
| `/accounts/login/` | Prijava |
| `/accounts/logout/` | Odjava |
| `/accounts/users/` | Upravljanje korisnicima (admin) |
| `/accounts/password_reset/` | Reset lozinke |
| `/projects/` | Lista projekata |
| `/projects/new/` | Novi projekat |
| `/projects/<id>/` | Detalji projekta (kanban board) |
| `/projects/<id>/edit/` | Uredivanje projekta |
| `/projects/<id>/delete/` | Brisanje projekta |
| `/projects/<id>/members/` | Upravljanje clanovima |
| `/tasks/project/<id>/create/` | Novi zadatak |
| `/tasks/<id>/update/` | Uredivanje zadatka |
| `/tasks/<id>/delete/` | Brisanje zadatka |
| `/tasks/<id>/move/` | Premjestanje zadatka (kolona) |
| `/admin/` | Django admin panel |

## Modeli baze podataka

```
User (AbstractUser)
├── username, email (unique), password
├── role: ADMIN | TEAM_MEMBER | VIEWER
└── avatar (opciono)

Project
├── name, key (unique), description
├── owner (FK -> User)
├── members (M2M -> User)
├── status: ACTIVE | ARCHIVED
└── Board (OneToOne)
    └── Column (FK -> Board)
        ├── name (To Do, In Progress, Done)
        └── order

Task
├── title, description
├── project (FK -> Project)
├── column (FK -> Column)
├── assignee (FK -> User, opciono)
├── created_by (FK -> User)
├── priority: LOW | MEDIUM | HIGH | CRITICAL
├── due_date (opciono)
└── labels (M2M -> Label)

Label
├── name
└── color (HEX)

AuditLog
├── user (FK -> User)
├── action: CREATED | UPDATED | DELETED
├── content_type + object_id (GenericForeignKey)
├── extra_data (JSON - pracenje promjena polja)
└── timestamp
```

## Dodavanje labele

``
http://localhost:8000/admin/tasks/label/add/

```