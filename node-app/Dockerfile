FROM node:12-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY app.js .
ENTRYPOINT [ "node" ]
CMD [ "app.js" ]