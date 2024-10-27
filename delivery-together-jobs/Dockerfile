# Extender de la versión 16 de Node
FROM node:18

# Establecer el directorio de trabajo
WORKDIR /usr/src/app

# Copiar solo los archivos necesarios para instalar dependencias
COPY package.json package-lock.json ./

# Instalar paquetes necesarios en fase de build
RUN npm install
# Copiar la aplicación
COPY . .


# Etiqueta de metadata
LABEL author="Fabio Castagnola <f.castagnola@uniandes.edu.co>, Pedro Capriles <p.caprilespe@uniandes.edu.co>"

# Comando a ejecutar en fase de runtime
CMD ["npm", "start"]
