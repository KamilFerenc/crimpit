FROM node:13.7

WORKDIR /app/frontend

# Install dependencies
COPY package.json yarn.lock /app/frontend/

RUN npm install

# Add rest of the client code
COPY ./ /app/frontend/

EXPOSE 3000

CMD ["npm", "start"]