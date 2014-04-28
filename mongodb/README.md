# Install 

    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
    echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
    cat /etc/apt/sources.list.d/mongodb.list 
    apt-get update
    apt-get install mongodb-org
    apt-get install mongodb-org mongodb-org-server mongodb-org-shell mongodb-org-mongos mongodb-org-tools

# Start mongodb

    service mongod start 

# Getting start with mongodb
connect to a mongod

    mongo
    db
    show dbs
    use mydb
    help

insert j, k document 

    j = { name : "mongo" }
    k = { x : 3 }
    db.testData.insert( j )
    db.testData.insert( k )

    show collections
    db.testData.find()

    var c = db.testData.find()
    printjson( c[0] )
    printjson( c[1] )
    db.testData.find( {"name" :"mongo"})

Generate Test Data

    for (var i = 1; i <= 25; i++) db.testData.insert( { x : i } )

    function insertData(dbName, colName, num) {

          var col = db.getSiblingDB(dbName).getCollection(colName);

            for (i = 0; i < num; i++) {
                    col.insert({x:i});
                      }

                        print(col.count());

    }

