#!/usr/bin/env bash

echo ""
echo "+--------------+"
echo "| Setup Worker |"
echo "+--------------+"
echo ""
rabbitmq-plugins enable rabbitmq_management
service rabbitmq-server restart