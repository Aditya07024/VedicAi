FROM node:18-alpine

WORKDIR /app

# Copy and install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy source
COPY . .

# Build
RUN npm run build

# Expose port
EXPOSE 3000

# Serve
CMD ["npm", "run", "dev"]
