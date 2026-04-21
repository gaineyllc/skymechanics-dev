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

# Build the app for production
RUN npm run build

# Serve with Vite preview
CMD ["npx", "vite", "preview", "--host", "0.0.0.0", "--port", "3000"]
