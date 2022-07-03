![Tests status](https://github.com/lorenzocesconetto/fastapi-postgresql/actions/workflows/actions.yml/badge.svg)

# FastAPI and PostgreSQL - Base Project Generator

This repo creates a basic FastAPI backend using cookiecutter.

## Why?

I've based my work on Tiangolo's [cookiecutter project](https://github.com/tiangolo/full-stack-fastapi-postgresql) project generator. But Tiangolo's project seems to be unmaintained for two years now. There's some code that I've ported from his project that still looks the same. Despite that, I've made some major changes.

I decided to create my own boilerplate in order to address some issues:
- Create a very simple and intuitive codebase.
- Update python and the packages to the latest version.
- Make some design changes that provide higher cohesion and lower coupling.

## Usage

Navigate with your terminal to the path where you'd like to create the new project.
Then run cookiecutter:
```
pip install cookiecutter
cookiecutter https://github.com/lorenzocesconetto/fastapi-postgresql
```

Provide input as you're prompted by cookiecutter and you're all set!

You can run the project with this single command (of course you need docker installed and the docker daemon must be up and running)
```
docker-compose -f "docker-compose.dev.yml" up -d --build
```

You can connect to the database from your terminal running the following command:
```
./scripts/psql-connect.sh
```

## Make this project better

This is what I see for the next steps of this project, feel free to jump in and open a PR:

- Implement authorization based on scopes
- Send confirmation email upon register
    - Keep an email available for new registrations until someone has confirmed it
- Implement deployment code:
    - Google App Engine
    - AWS Elastic Beanstalk
    - Kubernetes
- Gather the messages that the API sends to the frontend into a single file
    - Also implement support for multiple languages / internationalization

