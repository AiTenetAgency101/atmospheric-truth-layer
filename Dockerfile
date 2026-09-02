FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY server.js overlay.html .env* ./

EXPOSE 9099

CMD ["npm", "start"]
