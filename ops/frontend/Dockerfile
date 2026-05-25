FROM node:25-alpine

WORKDIR /app

COPY srcs/frontend/package*.json ./
RUN npm install

COPY srcs/frontend .

CMD ["npm", "run", "dev", "--", "--host"]