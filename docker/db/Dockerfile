# FROM minyichen666/cinefusion-central-mysql
# COPY setup.sh /mysql/setup.sh
# COPY build.sql /mysql/build.sql
# CMD ["", ""]

FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=movie_db
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=user


COPY ./new_netflix_titles.csv /var/lib/mysql-files/
COPY ./new_tv_shows.csv /var/lib/mysql-files/
COPY ./build.sql /docker-entrypoint-initdb.d/