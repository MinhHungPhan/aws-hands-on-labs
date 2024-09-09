# Use the official Node.js 20 image as the base
FROM node:20

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire project (ensure to create a .dockerignore to exclude unnecessary files)
COPY . .

# Your application's default port
EXPOSE 3000

# Command to run your application
CMD ["npm", "start"]