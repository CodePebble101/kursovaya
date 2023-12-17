db = db.getSiblingDB('test_db')
db.users.remove({});
db.createCollection('users');
db.users.insert(
        {
            "username": "admin",
            "password":"admin",
        });
