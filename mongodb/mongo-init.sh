set -e

mongo -- "$MONGO_INITDB_DATABASE" <<EOF
    let res = [
        db.createCollection("$MONGO_COLLECTION_NAME"),
        db["$MONGO_COLLECTION_NAME"].createIndex( { uid: 1 }, { unique: true } ),
        db["$MONGO_COLLECTION_NAME"].createIndex( { uid: 1, user: 1 }, { unique: true } )
    ]

    const error = !res.map((ret) => ret['ok']).every(Boolean)

    if (error) {
        print('An error occured ', res)
        quit(1)
    }

EOF
