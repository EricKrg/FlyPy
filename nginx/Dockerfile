FROM node:alpine as node
RUN  apk update && apk add git
RUN git clone https://github.com/EricKrg/FlyPy.git && cd FlyPy && ls
RUN cd FlyPy/frontend/FlyPyApp && npm install && npm run build --prod

FROM nginx:alpine
WORKDIR /usr/share/nginx/html
COPY --from=node /FlyPy/frontend/FlyPyApp/dist/* .
# Copy custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80 443
