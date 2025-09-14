FROM node:20-alpine AS builder 

WORKDIR /app

COPY package.json .
COPY pnpm-lock.yaml .

RUN npm install 

COPY . .

EXPOSE 3000

CMD ["npm","run","dev"]

