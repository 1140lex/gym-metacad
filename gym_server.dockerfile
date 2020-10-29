FROM nikolaik/python-nodejs 
COPY . /app
WORKDIR /app
RUN \
 apt update -y && \
 apt upgrade -y && \
 apt install golang-go gfortran libopenblas-dev liblapack-dev -y && \
 pip install cython numpy && \
 pip install gym universe
WORKDIR /app/metacad
RUN npm install
ENTRYPOINT ["npm", "run", "dev"]
EXPOSE 3000/TCP 5558/TCP