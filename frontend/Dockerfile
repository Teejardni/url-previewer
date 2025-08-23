# Stage 1: Builder
FROM node:22-slim AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install --frozen-lockfile

# Copy source files
COPY . .

# Build the React app
RUN npm run build

# Stage 2: Runtime
FROM nginx:alpine

# Copy build output to Nginx public directory
COPY --from=builder /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]