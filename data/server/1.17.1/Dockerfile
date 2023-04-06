FROM openjdk-11

WORKDIR /minecraft

COPY vanilla-1.17.1.jar .
COPY data/eula.txt .

CMD ["java", "-Xms1G", "-Xmx1G", "-jar", "vanilla-1.17.1.jar", "nogui"]

EXPOSE 25565
