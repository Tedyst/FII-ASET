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