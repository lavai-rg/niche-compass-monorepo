# Gunakan base image Node.js untuk build
FROM node:20-alpine as build

WORKDIR /app

# Copy package.json dan install dependencies
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install --frozen-lockfile

# Copy kode frontend dan build aplikasi
COPY . .
RUN pnpm run build

# Gunakan base image Nginx untuk menyajikan file statis
FROM nginx:stable-alpine

# Copy hasil build dari tahap sebelumnya ke Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port Nginx
EXPOSE 80

# Jalankan Nginx
CMD ["nginx", "-g", "daemon off;"]


