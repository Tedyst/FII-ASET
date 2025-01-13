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

## Problem presentation

In today's fast-paced digital world, the need for secure, scalable, and efficient deployment of containerized microservices across cloud environments is paramount. Traditional deployment methods often fall short in addressing the complexities and security challenges associated with modern applications. This project aims to solve these issues by building a fully automated DevSecOps pipeline that integrates security scanning, infrastructure provisioning via Infrastructure as Code (IaC), database migrations, and automated monitoring.

## State-of-the-art

Current solutions for DevSecOps pipelines often involve a combination of various tools and practices. Some of the popular tools and practices include:
- **CI/CD Pipelines**: Tools like Jenkins, GitHub Actions, and GitLab CI/CD are widely used to automate the build, test, and deployment processes.
- **Infrastructure as Code (IaC)**: Tools like Terraform, AWS CloudFormation, and Ansible are used to define and manage infrastructure as code.
- **Security Scanning**: Tools like SonarCloud, Snyk, and OWASP Dependency-Check are used to perform continuous security scanning of code and containers.
- **Database Migrations**: Tools like Flyway and Liquibase are used to handle database migrations as part of the CI/CD process.
- **Monitoring and Logging**: Tools like Prometheus, Grafana, and ELK Stack (Elasticsearch, Logstash, Kibana) are used for monitoring and logging the health and performance of microservices and infrastructure.

## Your solution

Our solution involves integrating the following components into a fully automated DevSecOps pipeline:
- **CI/CD Pipeline with GitHub Actions**: We set up a CI/CD pipeline using GitHub Actions to automatically build, test, and deploy containerized microservices. The pipeline also manages infrastructure deployment using Terraform for Infrastructure as Code (IaC).
- **Infrastructure as Code (IaC) with Terraform**: We use Terraform to provision and manage cloud infrastructure across multiple environments (development, staging, production). All infrastructure is defined as code, including load balancers, VPCs, and databases. Terraform is integrated into the GitHub Actions pipeline for fully automated deployments.
- **DevSecOps with Security Scanning and Vulnerability Management**: We integrate SonarCloud into the pipeline for continuous security scanning of code and containers. Snyk is used for container security scanning to detect vulnerabilities in dependencies and container images. Each build stage includes security checks to enforce compliance and vulnerability management before deployment.
- **Automated Database Migrations with Flyway**: We integrate Flyway to handle database migrations as part of the CI/CD process. Database changes are applied automatically during each deployment, with proper version control and rollback mechanisms in case of failures. Flyway’s migration scripts are used to manage schema changes for containerized databases like PostgreSQL.
- **Automated Monitoring and Logging with Prometheus and Grafana**: We set up Prometheus for monitoring the health of microservices and infrastructure. Performance metrics such as CPU usage, memory consumption, and response times are tracked. Grafana is used to visualize metrics on dashboards for real-time monitoring of system performance. Alerting is set up in Prometheus to notify when metrics exceed predefined thresholds (e.g., high CPU usage, memory leaks, etc.).

## Results, Evaluation

The implementation of our DevSecOps pipeline has yielded significant improvements in the deployment process. Key results and evaluations include:
- **Improved Deployment Speed**: The automated CI/CD pipeline has reduced the time required for building, testing, and deploying microservices. This has resulted in faster release cycles and quicker time-to-market for new features.
- **Enhanced Security**: The integration of security scanning tools like SonarCloud and Snyk has helped identify and mitigate vulnerabilities early in the development process. This has improved the overall security posture of the application.
- **Scalability and Reliability**: The use of Infrastructure as Code (IaC) with Terraform has enabled consistent and repeatable infrastructure deployments across multiple environments. This has improved the scalability and reliability of the application.
- **Efficient Database Management**: The integration of Flyway for automated database migrations has ensured that database changes are applied consistently and reliably during each deployment. This has reduced the risk of database-related issues and improved the overall stability of the application.
- **Proactive Monitoring and Alerting**: The use of Prometheus and Grafana for monitoring and alerting has provided real-time insights into the health and performance of microservices and infrastructure. This has enabled proactive identification and resolution of issues before they impact end-users.

## Comparison with other solutions

Compared to traditional deployment methods, our DevSecOps pipeline offers several advantages:
- **Automation**: The fully automated CI/CD pipeline reduces manual intervention and minimizes the risk of human errors. This results in faster and more reliable deployments.
- **Security**: The integration of security scanning tools ensures that vulnerabilities are identified and addressed early in the development process. This improves the overall security of the application.
- **Scalability**: The use of Infrastructure as Code (IaC) with Terraform enables consistent and repeatable infrastructure deployments across multiple environments. This improves the scalability and reliability of the application.
- **Efficiency**: The automated database migrations with Flyway ensure that database changes are applied consistently and reliably during each deployment. This reduces the risk of database-related issues and improves the overall stability of the application.
- **Monitoring and Alerting**: The use of Prometheus and Grafana for monitoring and alerting provides real-time insights into the health and performance of microservices and infrastructure. This enables proactive identification and resolution of issues before they impact end-users.

## Future work

There are several potential future improvements that can be made to our DevSecOps pipeline:
- **Enhanced Security Measures**: Implement additional security measures such as automated penetration testing and runtime security monitoring to further improve the security posture of the application.
- **Advanced Analytics**: Integrate advanced analytics tools to gain deeper insights into the performance and behavior of microservices and infrastructure. This can help identify potential bottlenecks and optimize the overall system performance.
- **AI/ML Integration**: Explore the use of AI/ML techniques to automate anomaly detection and predictive maintenance. This can help proactively identify and resolve issues before they impact end-users.
- **Multi-Cloud Support**: Extend the pipeline to support multi-cloud deployments, enabling the application to be deployed across multiple cloud providers for improved redundancy and resilience.
- **Continuous Improvement**: Continuously monitor and evaluate the performance of the DevSecOps pipeline, and make iterative improvements to enhance its efficiency, security, and reliability.

## Conclusions

In conclusion, our fully automated DevSecOps pipeline has successfully addressed the challenges associated with secure, scalable, and efficient deployment of containerized microservices across cloud environments. The integration of CI/CD, Infrastructure as Code (IaC), security scanning, automated database migrations, and monitoring has resulted in significant improvements in deployment speed, security, scalability, and reliability. The proactive monitoring and alerting capabilities have enabled real-time insights into the health and performance of microservices and infrastructure, allowing for timely identification and resolution of issues. Overall, our DevSecOps pipeline has proven to be a valuable solution for modern application deployment.

## Bibliography

- "Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation" by Jez Humble and David Farley
- "Infrastructure as Code: Managing Servers in the Cloud" by Kief Morris
- "The DevOps Handbook: How to Create World-Class Agility, Reliability, & Security in Technology Organizations" by Gene Kim, Patrick Debois, John Willis, and Jez Humble
- "Site Reliability Engineering: How Google Runs Production Systems" by Niall Richard Murphy, Betsy Beyer, Chris Jones, and Jennifer Petoff
- "Prometheus: Up & Running: Infrastructure and Application Performance Monitoring" by Brian Brazil
- "Terraform: Up & Running: Writing Infrastructure as Code" by Yevgeniy Brikman

## Links

- [GitHub Repository](https://github.com/Tedyst/FII-ASET)
- [Project Board](https://github.com/users/Tedyst/projects/1/views/2)
- [Technologies and Related Work](https://docs.google.com/document/d/11urzU0jny9UJrOsGFh4iA7sewAFm6s6af9LfTdxIBcA/edit)
