#!/bin/bash

echo "Actualizando paquetes..."
sudo yum update -y

echo "Instalando Docker..."
sudo yum install docker -y

echo "Añadiendo el usuario ec2-user al grupo docker para permitir la ejecución de Docker sin sudo..."
sudo usermod -aG docker $USER

echo "Iniciar y habilitar Docker..."
sudo systemctl start docker
sudo systemctl enable docker

echo "Instalando Python3 y pip..."
sudo yum install python3 -y
sudo yum install python3-pip -y

echo "Instalando Docker Compose..."
sudo pip3 install docker-compose

echo "Instalando dependencias Python para tus scripts de productor/consumidor..."
pip3 install kafka-python

echo "Por favor, reinicia tu sesión para que los cambios tengan efecto."
echo "Instalación completada!"

