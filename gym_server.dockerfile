FROM nikolaik/python-nodejs 
COPY . /app
WORKDIR /app
RUN apt install golang 
RUN pip install numpy gym universe -y 
RUN npm install
ENTRYPOINT ["npm", "run", "dev"]
EXPOSE 3000/TCP