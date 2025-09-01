
### 📤 **2. SUBIR A GITHUB DESDE ANDROID:**

```bash
# Instalar git en Termux si no está
pkg install git

# Configurar git
git config --global user.name "Tu Nombre"
git config --global user.email "ia.mechmind@gmail.com"

# Inicializar repositorio
git init
git add .
git commit -m "🚀 Initial commit: Sistema de Alertas Tempranas Golfo de Cádiz"

# Crear repositorio en GitHub (desde navegador o termux)
# Ve a: https://github.com/new
# Crea repositorio: "sistema-alertas-golfo-cadiz"

# Conectar y subir
git remote add origin https://github.com/tuusuario/sistema-alertas-golfo-cadiz.git
git branch -M main
git push -u origin main

# Si pide credenciales, usar token de acceso:
echo "🔑 Si pide usuario/contraseña:"
echo "   Usuario: tu_usuario_github"
echo "   Contraseña: token_de_acceso_github (desde settings)"
