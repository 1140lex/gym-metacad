FROM nikolaik/python-nodejs 
COPY . /app
WORKDIR /app
RUN \
 apt update -y && \
 apt upgrade -y && \
 apt install golang-go gfortran libopenblas-dev liblapack-dev gconf-service libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 \
 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 \ 
 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget-y && \
 pip install cython numpy && \
 pip install gym universe
WORKDIR /app/metacad
RUN rm -r node_modules package-lock.json && npm install
ENTRYPOINT ["npm", "run", "dev"]
EXPOSE 3000/TCP 3001/TCP 5558/TCP