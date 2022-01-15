use admin
db.createUser({ user: "admin", pwd: "1234", roles: [{ role: "dbAdmin", db: "admin" }] })

use videos
db.createUser({ user: "root", pwd: "1234", roles: [{ role: "dbAdmin", db: "videos" }] })