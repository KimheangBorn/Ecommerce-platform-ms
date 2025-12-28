#!/bin/bash
# Helper script to initialize MongoDB Replica Set

echo "Initializing MongoDB Replica Set..."

docker exec -it ecommerce-platform-ms-mongo1-1 mongosh --eval '
rs.initiate({
  _id: "rs-users",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
})
'

echo "Replica Set Initialized!"
