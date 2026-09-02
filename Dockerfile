FROM node:20-alpine

WORKDIR /app

# Install git
RUN apk add --no-cache git

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application files
COPY jarvis-oracle.js .
COPY .env* ./

# Clone/pull latest from GitHub
RUN git clone https://github.com/AiTenetAgency101/atmospheric-truth-layer.git . || git pull origin master

# Expose port
EXPOSE 3001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3001', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})"

# Start JARVIS
CMD ["node", "jarvis-oracle.js"]
