# DevSecOps Pipeline with Infrastructure as Code (IaC), Automated Security Scanning, Database Migrations, and Monitoring (one or more requirements)

This project involves building a fully automated DevSecOps pipeline that integrates security scanning, infrastructure provisioning via Infrastructure as Code (IaC), database migrations, and automated monitoring. The system is designed for containerized microservices and aims to ensure secure, scalable, and efficient deployment across cloud environments.

## Key Features


### CI/CD Pipeline with GitHub Actions:
- Set up a CI/CD pipeline using GitHub Actions to automatically build, test, and deploy containerized microservices.
- The pipeline should also manage infrastructure deployment using Terraform for Infrastructure as Code (IaC).
### Infrastructure as Code (IaC) with Terraform:
- Use Terraform to provision and manage cloud infrastructure across multiple environments (development, staging, production).
- Define all infrastructure as code, including load balancers, VPCs, and databases.
- Integrate Terraform into the GitHub Actions pipeline for fully automated deployments.
### DevSecOps with Security Scanning and Vulnerability Management:
- Integrate SonarCloud into the pipeline for continuous security scanning of code and containers.
- Use Snyk for container security scanning to detect vulnerabilities in dependencies and container images.
- Ensure that each build stage includes security checks to enforce compliance and vulnerability management before deployment.
### Automated Database Migrations with Flyway:
- Integrate Flyway to handle database migrations as part of the CI/CD process.
- Ensure database changes are applied automatically during each deployment, with proper version control and rollback mechanisms in case of failures.
- Use Flyway’s migration scripts to manage schema changes for containerized databases like PostgreSQL.
### Automated Monitoring and Logging with Prometheus and Grafana:
- Set up Prometheus for monitoring the health of microservices and infrastructure. Track performance metrics such as CPU usage, memory consumption, and response times.
- Use Grafana to visualize metrics on dashboards for real-time monitoring of system performance.
- Set up alerting in Prometheus to notify when metrics exceed predefined thresholds (e.g., high CPU usage, memory leaks, etc.).

Project proposals for DevOps side:
- Smart City Traffic Management System
- Intelligent Secured Banking System
- Logistics and Fleet Management System
- Employee Management and Payroll System
- Financial Trading Platform

## Team

| Nume                                                       | E-Mail                       |              |
|------------------------------------------------------------|------------------------------|-------------|
| [Stoica Tedy](https://github.com/Tedyst)                   | stoicatedy@gmail.com         | Scrum Master |
| [Ignat Vlad](https://github.com/ignatrovino12)             | ignatrovino12@gmail.com      |              |
| [Dan Frunza](https://github.com/DanFrunza)                 | dani.frunza@yahoo.com        |              |
| [Teodorescu Calin](https://github.com/TeodorescuCalin)     | calin.teodorescu24@gmail.com |              |
| [Artur-Augustin Bejenari](https://github.com/mikeesnipess) | artur.bejenari00@gmail.com   |              |
| [Nastase Valentin](https://github.com/nastasevalentin)     | nastasevalentin20@gmail.com  |              |

## Useful Links

The main repository is available [here](https://github.com/Tedyst/FII-ASET).
The project board can be found [here](https://github.com/users/Tedyst/projects/1/views/2)
The technologies used and related work can be found [here](https://docs.google.com/document/d/11urzU0jny9UJrOsGFh4iA7sewAFm6s6af9LfTdxIBcA/edit)


# Using the app

## Installing the app

In order to install the app, you need to use Python 3.12 or higher. You can install it from [here](https://www.python.org/downloads/).
After you have installed Python, you can install the required packages by running the following command in the root directory of the project:

```bash
poetry install --with dev
pre-commit install
```

If you need to also modify the HTML templates, you also need to install NPM and run the following command in the `backend` directory of the project:

```bash
python manage.py tailwind install
```

After you have installed the required packages, you need to start the virtual environment by running the following command in the `backend` directory of the project:

```bash
poetry shell
```

If you also want to modify the translations made like this: _("text"), you need to run the following command in the `backend` directory of the project, after which you modify the translations in the `backend/locale/{lang}/LC_MESSAGES/django.po` files:

```bash
django-admin makemessages --all
```

After you have modified the translations, you need to compile them by running the following command in the `backend` directory of the project:

```bash
django-admin compilemessages
```

## Running the app

In order to run the app, you need to run the following command in the `backend` directory of the project:

```bash
python manage.py migrate
python manage.py runserver
```

In case you want to modify the HTML templates, you also need to run the following command IN PARALLEL:

```bash
python manage.py tailwind start
```

## Making migrations

In order to make migrations (when you change any Model), you need to run the following command in the `backend` directory of the project:

```bash
python manage.py makemigrations
```

Be warned that Celery tasks will run in eager mode, meaning that they will run synchronously. If you want to run them asynchronously, you need to install and run a message broker like RabbitMQ or Redis. You can find more information about this [here](https://docs.celeryproject.org/en/stable/getting-started/brokers/).
