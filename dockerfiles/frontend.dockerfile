FROM node:gallium-slim
WORKDIR /react
COPY ./frontend/license-plate-camera .
RUN npm run build