# Cómo subir este repositorio a GitHub

El repositorio ya está inicializado, con los 13 commits en formato
[Conventional Commits](https://www.conventionalcommits.org/) y la rama `main`.
Solo falta conectarlo con GitHub.

## 1. Crear el repositorio vacío

En https://github.com/new:

- **Repository name:** `staydata-airbnb-eda`
- **Visibility:** Public (para que tu profesor pueda abrirlo)
- **NO** marques "Add a README file", "Add .gitignore" ni "Choose a license"
  — el repositorio local ya los trae y crearlos allá provoca un conflicto.

## 2. Conectar y subir

Desde la carpeta del proyecto:

```bash
cd staydata-airbnb-eda

# Confirma que el historial está completo (deben aparecer 13 commits)
git log --oneline

# Sustituye <usuario> por tu nombre de usuario de GitHub
git remote add origin https://github.com/<usuario>/staydata-airbnb-eda.git
git push -u origin main
```

Si GitHub te pide contraseña, usa un **Personal Access Token** (Settings →
Developer settings → Personal access tokens → Tokens (classic) → scope `repo`),
no tu contraseña de la cuenta.

Con SSH configurado, el remoto sería:

```bash
git remote add origin git@github.com:<usuario>/staydata-airbnb-eda.git
```

## 3. Después del push

1. Copia la URL del repositorio.
2. Sustitúyela en la última línea del reporte
   `reports/Actividad2_Reporte_EDA.docx`, donde dice
   `https://github.com/<usuario>/staydata-airbnb-eda`.
3. Vuelve a exportar el PDF si tu entrega lo incluye.

## Nota sobre la base de datos

El archivo `data/raw/airbnb_price_prediction.xlsx` pesa 37 MB y está en
`.gitignore` a propósito: GitHub advierte a partir de 50 MB y el archivo no
aporta nada al historial. El README explica dónde colocarlo para ejecutar el
proyecto.

## Nota sobre la autoría de los commits

Los commits están firmados con tu nombre y tu correo, y llevan un pie
`Co-Authored-By` que declara la asistencia de la herramienta de IA. Si tu
profesor pide únicamente autoría propia, o si prefieres quitarlo, puedes
reescribir el historial antes del push:

```bash
git filter-branch -f --msg-filter 'sed "/^Co-Authored-By: Claude/d; /^Claude-Session:/d"' -- --all
```
