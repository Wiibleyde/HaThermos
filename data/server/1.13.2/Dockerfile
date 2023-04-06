FROM openjdk-8-jre

WORKDIR /minecraft

COPY vanilla-1.13.2.jar .
COPY data/eula.txt .

CMD ["java", "-Xms1G", "-Xmx1G", "-jar", "vanilla-1.13.2.jar", "nogui"]

EXPOSE 25565
