FROM openjdk-11

WORKDIR /minecraft

COPY vanilla-1.15.2.jar .
COPY data/eula.txt .

CMD ["java", "-Xms1G", "-Xmx1G", "-jar", "vanilla-1.15.2.jar", "nogui"]

EXPOSE 25565
