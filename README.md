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

## Usage

### Create an account

To create an account, you must go to the `/register` page. You will then have to enter your Minecraft username, your email address and your password.

### Login to your account

To login to your account, you must go to the `/login` page. You will then have to enter your email address and your password.

### See your servers

To see your servers, you must go to the `/dashboard` page.

### Create a server

To create a server, you must go to the `/createServer` page. You will then have to enter the name of your server and the version of Minecraft you want to use.

### Delete a server

To delete a server, you must go to the `/server/<id>` page. You will then have to click on the `Delete` button.

### Start a server

To start a server, you must go to the `/server/<id>` page. You will then have to click on the `Start` button.

### Stop a server

To stop a server, you must go to the `/server/<id>` page. You will then have to click on the `Stop` button.

### See the logs the web server

To see the logs of a server, you must go on your server in the `/srv/hathermos_data/` directory. You will then have to open the `logs.log` file.

### Modify the database 

To modify the database, you must go on your server in the `/srv/hathermos_data/` directory. You will then have to open the `hathermos.db` file. (with sqlite3)

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
