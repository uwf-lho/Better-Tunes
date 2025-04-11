FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and lock
COPY package*.json ./

# Ensure devDependencies are installed
ENV NODE_ENV=development

# Install ALL dependencies (prod + dev)
RUN npm install

# Install TypeScript globally (optional, since you have it locally)
RUN npm install -g typescript

# Copy the rest of the app
COPY . .

# Build the TypeScript app
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
