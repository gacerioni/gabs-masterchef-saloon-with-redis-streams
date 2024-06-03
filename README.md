# Running the Stream Application Docker Container

To run the Stream Application Docker container, follow these steps and use the provided command. This command sets the necessary environment variables and specifies the role (producer, consumer, or supervisor) along with any required arguments.

## Command Syntax

```shell
docker run -it --name <container_name>
-e REDIS_HOST=<your_redis_host>
-e REDIS_PORT=<your_redis_port>
-e REDIS_PASSWORD=<your_redis_password>
gacerioni/gabs-redis-stream-demo:1.0.0 <role> <optional_arguments>
```

- `--name <container_name>`: Assigns a name to the container for easier management.
- `-e REDIS_HOST=<your_redis_host>`: Sets the Redis host environment variable.
- `-e REDIS_PORT=<your_redis_port>`: Sets the Redis port environment variable.
- `-e REDIS_PASSWORD=<your_redis_password>`: Sets the Redis password environment variable.
- `<your_image_name>:<tag>`: Specifies the Docker image and tag to use.
- `<role>`: Specifies the role to run (`producer`, `consumer`, or `supervisor`).
- `<arguments>`: Additional arguments required for the consumer role.

## Example Command

Here’s an example command to run the container as a consumer with the name `stream_consumer` and a consumer name `gabsthewaiter`:

```shell
docker run -it --name stream_consumer \
-e REDIS_HOST=redis-18884.c98.us-east-1-4.ec2.redns.redis-cloud.com \
-e REDIS_PORT=18884 \
-e REDIS_PASSWORD=blablabla \
gacerioni/gabs-redis-stream-demo:1.0.0 consumer gabsthewaiter
```

## Possible Roles and Arguments

- **Producer**: Runs the producer script.

```shell
docker run -it --name stream_producer
-e REDIS_HOST=<your_redis_host>
-e REDIS_PORT=<your_redis_port>
-e REDIS_PASSWORD=<your_redis_password>
gacerioni/gabs-redis-stream-demo:1.0.0 producer
```


- **Consumer**: Runs the consumer script. Requires a consumer name as an additional argument.

```shell
docker run -it --name stream_producer
-e REDIS_HOST=<your_redis_host>
-e REDIS_PORT=<your_redis_port>
-e REDIS_PASSWORD=<your_redis_password>
gacerioni/gabs-redis-stream-demo:1.0.0 consumer <consumer_name>
```

- **Supervisor**: Runs the supervisor script. Not doing much, just pointing who is forgetting to do their job.

```shell
docker run -it --name stream_supervisor
-e REDIS_HOST=<your_redis_host>
-e REDIS_PORT=<your_redis_port>
-e REDIS_PASSWORD=<your_redis_password>
gacerioni/gabs-redis-stream-demo:1.0.0 supervisor
```