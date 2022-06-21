mysql -u root -e "CREATE DATABASE videos_dev;  CREATE DATABASE videos_test; CREATE USER userapp@localhost identified by '1234';  GRANT ALL privileges ON *.* TO userapp@localhost;"
