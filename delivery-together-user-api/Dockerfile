# Extender de la versión 16 de Node
FROM node:16

# Exponer el puerto 3000
EXPOSE 3000

# Establecer el directorio de trabajo
WORKDIR /usr/src/app

# Copiar solo los archivos necesarios para instalar dependencias
COPY package.json package-lock.json ./

# Instalar paquetes necesarios en fase de build
RUN npm install

# Instalar node-gyp y bcrypt localmente
RUN npm uninstall bcrypt
RUN npm i bcrypt

# Copiar la aplicación
COPY . .

EXPOSE 3000


# Etiqueta de metadata
LABEL author="Fabio Castagnola <f.castagnola@uniandes.edu.co>"

# Comando a ejecutar en fase de runtime
CMD ["npm", "start"]
