FROM node:13.7

WORKDIR /app/

# Install dependencies
COPY package.json yarn.lock /app/

RUN npm install

# Add rest of the client code
COPY ./ /app/

EXPOSE 3000

CMD ["npm", "start"]