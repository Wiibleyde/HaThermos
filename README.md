# HaThermos <img src="./static/assets/HaThermos.png" width="35"></img>

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/4af34b6cf53e414b92851d98d49566b1)](https://app.codacy.com/gh/Wiibleyde/HaThermos/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade) ![Release](https://img.shields.io/github/v/release/Wiibleyde/HaThermos) ![License](https://img.shields.io/github/license/Wiibleyde/HaThermos)

## Description

HaThermos is a simple parodies of the famous [Aternos](https://aternos.org/) website. It is a web application that allows you to create a Minecraft server in a few clicks. It is a project that I started to learn the basics of web development. It is not intended to be used in production (but it is possible).

## Features

-   Create a Vanilla Minecraft server in a few clicks

## Installation

Simply clone the repository and run the following command:

```bash
docker-compose up -d
```

## Manage HaThermos

### See the logs the web server

To see the logs of a server, you must go on your server in the `/var/hathermos/hathermos-data/` directory. You will then have to open the `logs.log` file.

### Modify the database 

To modify the database, you must go on your server in the `/var/hathermos/hathermos-data/` directory. You will then have to open the `database.db` file.

### Get the minecraft servers data

To get the minecraft servers data, you must go on your server in the `/var/hathermos/minecraft-data/` directory. You will see some folder named has the id of the server. In each folder, you will have the minecraft server data.

### Get the backups of the minecraft servers and the HaThermos data

To get the backups of the minecraft servers and the HaThermos data, you must go on your server in the `/var/hathermos/hathermos-backup/` directory. You will see some folder named has the date, the hour and the minute of the backup. In each folder, you will have the `minecraft` folder and the `data` folder. The `minecraft` folder contains the minecraft server data and the `data` folder contains the HaThermos data.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Author

-   **Wiibleyde** - _Initial work_ - [Wiibleyde](https://github.com/wiibleyde)
-   **Aternos** - _Inspiration_ - [Aternos](https://aternos.org/)
-   **itzg** - _Docker Minecraft server_ - [itzg](https://github.com/itzg/docker-minecraft-server)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

-   [Aternos](https://aternos.org/)
-   [itzg](https://github.com/itzg/docker-minecraft-server)

<img src="./static/assets/HaThermos.png" width="500"></img>