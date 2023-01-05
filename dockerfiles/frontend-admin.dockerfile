FROM node:gallium-slim
WORKDIR /react
COPY ./frontend/admin/package.json .
RUN npm i
COPY ./frontend/admin .
RUN npm run build