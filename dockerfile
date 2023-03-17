FROM openjdk:11

WORKDIR /minecraft

RUN curl -o paper.jar https://papermc.io/api/v1/paper/1.19.3/latest/download

CMD ["java", "-Xms1G", "-Xmx1G", "-jar", "paper.jar"]

EXPOSE 25565

