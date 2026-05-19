# 🐄 AgroControl API

API REST con **FastAPI + MySQL** para el sistema de gestión ganadera AgroControl.

## Estructura del proyecto

```
agrocontrol-api/
├── app/
│   ├── main.py              ← Punto de entrada FastAPI
│   ├── config.py             ← Variables de entorno
│   ├── database.py           ← Conexión SQLAlchemy
│   ├── auth.py               ← JWT + hashing + dependencia de auth
│   ├── models/
│   │   └── models.py         ← Modelos SQLAlchemy (usuarios, fincas, animales, vacunaciones)
│   ├── schemas/
│   │   └── schemas.py        ← Esquemas Pydantic (request/response)
│   └── routers/
│       ├── auth.py           ← POST /registro, /login, GET /me
│       ├── fincas.py         ← CRUD /api/fincas
│       ├── animales.py       ← CRUD /api/animales (filtros por finca, tipo, estado)
│       ├── vacunaciones.py   ← CRUD /api/vacunaciones
│       └── dashboard.py      ← GET /api/dashboard/stats
├── requirements.txt
├── .env.example
└── README.md
```

## Instalación

### 1. Crear la base de datos

Ejecuta el archivo `bse_de_dats.sql` en tu servidor MySQL:

```bash
mysql -u root -p < bse_de_dats.sql
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
# Edita .env con tus credenciales de MySQL
```

### 3. Instalar dependencias

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 4. Ejecutar el servidor

```bash
uvicorn app.main:app --reload --port 8000
```

La documentación interactiva estará en: **http://localhost:8000/docs**

---

## Endpoints

### Autenticación

| Método | Ruta               | Descripción        | Auth |
|--------|--------------------|--------------------|------|
| POST   | `/api/auth/registro` | Crear cuenta       | ❌   |
| POST   | `/api/auth/login`    | Iniciar sesión     | ❌   |
| GET    | `/api/auth/me`       | Perfil del usuario | ✅   |

### Fincas

| Método | Ruta                  | Descripción          | Auth |
|--------|-----------------------|----------------------|------|
| GET    | `/api/fincas/`        | Listar mis fincas    | ✅   |
| GET    | `/api/fincas/{id}`    | Detalle de finca     | ✅   |
| POST   | `/api/fincas/`        | Crear finca          | ✅   |
| PUT    | `/api/fincas/{id}`    | Actualizar finca     | ✅   |
| DELETE | `/api/fincas/{id}`    | Eliminar finca       | ✅   |

### Animales

| Método | Ruta                           | Descripción           | Auth |
|--------|--------------------------------|-----------------------|------|
| GET    | `/api/animales/`               | Listar (filtros: finca_id, tipo, estado) | ✅ |
| GET    | `/api/animales/{id}`           | Por ID                | ✅   |
| GET    | `/api/animales/codigo/{codigo}`| Por código            | ✅   |
| POST   | `/api/animales/`               | Registrar animal      | ✅   |
| PUT    | `/api/animales/{id}`           | Actualizar            | ✅   |
| DELETE | `/api/animales/{id}`           | Eliminar              | ✅   |

### Vacunaciones

| Método | Ruta                        | Descripción            | Auth |
|--------|-----------------------------|------------------------|------|
| GET    | `/api/vacunaciones/`        | Listar (filtros: animal_codigo, estado) | ✅ |
| GET    | `/api/vacunaciones/{id}`    | Detalle                | ✅   |
| POST   | `/api/vacunaciones/`        | Registrar vacuna       | ✅   |
| PUT    | `/api/vacunaciones/{id}`    | Actualizar             | ✅   |
| DELETE | `/api/vacunaciones/{id}`    | Eliminar               | ✅   |

### Dashboard

| Método | Ruta                    | Descripción           | Auth |
|--------|-------------------------|-----------------------|------|
| GET    | `/api/dashboard/stats`  | Estadísticas del hato | ✅   |

---

## Usuario de prueba

El SQL incluye un usuario demo:

- **Email:** `ganadero@agro.co`
- **Contraseña:** `12345678`

---

## Ejemplo de uso

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "ganadero@agro.co", "password": "12345678"}'

# Listar fincas (con token)
curl http://localhost:8000/api/fincas/ \
  -H "Authorization: Bearer <tu_token>"

# Crear animal
curl -X POST http://localhost:8000/api/animales/ \
  -H "Authorization: Bearer <tu_token>" \
  -H "Content-Type: application/json" \
  -d '{"codigo": "BOV-050", "tipo": "Bovino", "raza": "Gyr", "peso": 280, "edad_meses": 14, "finca_id": 1}'
```
