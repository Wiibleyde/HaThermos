FROM openjdk-8

WORKDIR /minecraft

COPY vanilla-1.8.8.jar .
COPY data/eula.txt .

CMD ["java", "-Xms1G", "-Xmx1G", "-jar", "vanilla-1.8.8.jar", "nogui"]

EXPOSE 25565
