FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

# Create the .cache directory and fix all permissions
#RUN mkdir -p /app/node_modules/.cache && chown -R node:node /app

# Copy code with ownership set
COPY package.json public src .

RUN mkdir -p /app/node_modules/.cache && chown -R 777 /app

EXPOSE 3000

CMD ["npm", "start"]
