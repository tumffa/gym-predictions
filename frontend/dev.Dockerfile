FROM node:18

WORKDIR /app

COPY . .

RUN npm install

# Ensure node_modules/.bin is in the PATH
ENV PATH=/app/node_modules/.bin:$PATH

CMD ["npm", "run", "dev", "--", "--host"]