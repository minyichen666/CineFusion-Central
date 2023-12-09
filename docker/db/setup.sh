#!/bin/bash
set -e
systemctl mysql start
mysql < /mysql/build.sql
systemctl mysql stop