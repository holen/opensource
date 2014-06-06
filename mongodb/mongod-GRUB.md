# mongodb GRUD
Query 

    db.inventory.find( {} )
    db.inventory.find() 
    db.inventory.find( { type: "snacks" } ) 
    db.inventory.find( { type: { $in: [ 'food', 'snacks' ] } } )
    db.inventory.find( { type: 'food', price: { $lt: 9.95 } } ) 
    db.inventory.find(
                   { $or: [
                            { qty: { $gt: 100 } },
                            { price: { $lt: 9.95 } }
                          ]
                   }
                 ) 
    db.inventory.find( { type: 'food', $or: [ { qty: { $gt: 100 } },
                                            { price: { $lt: 9.95 } } ]
                   } ) 
    db.inventory.find(
    {
      producer: {
                  company: 'ABC123',
                  address: '123 Street'
                }
    }) 
    db.inventory.find( { 'producer.company': 'ABC123' } )
    db.inventory.find( { tags: [ 'fruit', 'food', 'citrus' ] } )
    
insert 

    db.inventory.insert( { _id: 10, type: "misc", item: "card", qty: 15 } )
    db.inventory.update(
                     { type: "book", item : "journal" },
                     { $set : { qty: 10 } },
                     { upsert : true }
                   ) 
    db.inventory.save( { type: "book", item: "notebook", qty: 40 } ) 
    db.foo.insert({"bar":"baz"}) 
    db.foo.remove("bar":"baz"})
    db.drop_collection("bar")
    
remove 

    db.users.remove()  # 删除文档，不删除集合和索引
    
$set 指定一个健的值

    db.users.findOne()
    { "_id" : ObjectId("535dfb2e963e41a7f6e2d9e2"), "name" : "ken" }
    db.users.update({"_id": ObjectId("535dfb2e963e41a7f6e2d9e2")},{"$set":{"favorite book":"war and peace"}}) 
    rs1:PRIMARY> db.users.find()
    id" : ObjectId("535dfb2e963e41a7f6e2d9e2"), "name" : "ken", "favorite book" : "war and peace" } 
    db.users.update({"name":"joe"},{"$unset":"favorite book":1}})
    
$inc 增加已有键的值,只能用于整数、长整数和双精度浮点数

    rs1:PRIMARY> db.games.insert({"game":"pinball","user":"joe"})
    WriteResult({ "nInserted" : 1 })
    rs1:PRIMARY> db.games.findOne()
    {
            "_id" : ObjectId("535f553d0464ae1a7515f9f2"),
            "game" : "pinball",
            "user" : "joe"
    }
    rs1:PRIMARY> db.games.update({"game":"pinball","user":"joe"},{"$inc":{"score":50}})
    WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
    rs1:PRIMARY> db.games.find()
    { "_id" : ObjectId("535f553d0464ae1a7515f9f2"), "game" : "pinball", "user" : "joe", "score" : 50 } 
    

