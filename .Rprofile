Sys.setenv(MallocStackLogging = "0")

# Automatiquement "activer" le .venv pour Quarto/reticulate à l'ouverture du projet dans RStudio
venv_path <- file.path(getwd(), ".venv")

if (dir.exists(venv_path)) {
  Sys.setenv(VIRTUAL_ENV = venv_path)
  Sys.setenv(PATH = paste(
    file.path(venv_path, "bin"),
    Sys.getenv("PATH"),
    sep = .Platform$path.sep
  ))
  message("Environnement virtuel activé pour le projet: ", venv_path)
}
