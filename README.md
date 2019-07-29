Attack Proof - Detect Attack in a Real Time
===========================================================
# Author

Nazli Ansari

# Table of Contents
1. [Project Overview](README.md#Project_overview)
2. [Architecture](README.md#Architecture)
3. [Running Instruction](README.md#Running_Instruction)
4. [Files in Repo](README.md#repo-directory-structure)
5. [Future Work](README.md#Furure_work)
6. [Questions](README.md#Questions)

## Project Overview
[Back to Table of Contents](README.md#Project_overview)

Days by Days we hear a lot about cybersecurity attacks and how much expensive and time consumin it is. Therefore, it is necessary to have an automated an accurate system to monitor live traffic through web servers and alert engineers or admins of the potential risks.

In this project I deployed my machine learning model to large scale real time network data and I tried to monitor web server traffic and predict potential attacks in real time. This tool can detect 6 different kind of attacks (DDoS, Botnet, Brute Force, Infilteration, Web-based and port scan)

## Architecture
[Back to Table of Contents](README.md#Architecture)
![Capture](https://user-images.githubusercontent.com/27971359/61181582-8b5a4e80-a5f6-11e9-9b74-24d3bafeeee9.PNG)

## Running Instruction
[Back to Table of Contents](README.md#Running_Instruction)
To gain a copy of this project and test this project: git clone https://github.com/nazlians/Insight_Project

"Attack Proof" runs a pipeline on the AWS cloud, using the following cluster configurations:

*  four m4.large EC2 instances for Kafka
*  three m4.large EC2 instances for Docker and deploying model
*  One m4.large EC2 instances to run MySQL and the Dash front-end application

Using Kafka to ingest traffic stream simulated from a file on S3, Docker to predicted potential attacks in 5 second intervals using a pre-trained model by Random Forest and MySQL to store the processed data to be queried, the data is then rendered in Dash to show real-time updates to server traffic or attack predictions every second.

To replicate my pipeline follow the following steps:

1) Install zookeeper v3.4.13 and kafka v 1.10 on kafka Cluster and start zookeeper and kafka
2) Build Consumer Docker Image
3) Install MySQl
4) Install Dash, Dash-core-components, and Dash-html-components python packages on Dash node

## Files in Repo
[Back to Table of Contents](README.md#repo-directory-structure)
