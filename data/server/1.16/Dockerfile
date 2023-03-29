FROM openjdk-11

WORKDIR /minecraft

COPY vanilla-1.16.5.jar .
COPY data/eula.txt .

CMD ["java", "-Xms1G", "-Xmx1G", "-jar", "vanilla-1.16.5.jar", "nogui"]

EXPOSE 25565
