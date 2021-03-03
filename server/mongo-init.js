db.apps.createIndex( { uid: 1 }, { unique: true } );

// Expire inactive documents after 24h
db.apps.createIndex( { "createdAt": 1 }, { expireAfterSeconds: 24*60*60, partialFilterExpression: { active: false } } );
