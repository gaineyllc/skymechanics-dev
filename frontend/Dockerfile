# Frontend Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files first for layer caching
COPY package*.json ./

# Install dependencies once
RUN npm install --legacy-peer-deps

# Copy source code
COPY . .

EXPOSE 3000

# Start dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
