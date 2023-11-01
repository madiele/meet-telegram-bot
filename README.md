# meet-telegram-bot
this is a bot i use to manage a telegram group, it has a django /admin page where you can edit varius options

This project uses Docker Compose to build and run the application. It provides a convenient way to manage the necessary services and dependencies required for the project.

## Prerequisites

Before getting started, please ensure you have the following installed on your machine:

- Docker: [Download and Install Docker](https://docs.docker.com/get-docker/)

## Getting Started

To get started with this project, follow the steps below:

1. Clone the repository to your local machine:

   ```shell
   git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```shell
   cd project-directory
   ```

3. Set the required environment variables in the `docker-compose.yml` file. These variables are usually used for configuring the application.

4. Build and start the project using Docker Compose:

   ```shell
   sudo docker compose up -d
   ```

   The `-d` flag runs the containers in detached mode, allowing them to run in the background.

5. Access the running application by opening a web browser and navigating to the appropriate URL.

## Contributing

If you would like to contribute to this project, please follow these guidelines:

1. Fork the repository and clone it to your local machine.
2. Create a new branch for your contribution.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your forked repository.
5. Submit a pull request, explaining the changes you have made.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify it as per your needs.
