# wireless-app-assignment-backend

## How to create database?
```
rm db.sqlite
python db.py
```

## How to run the server?
```
python main.py
```

## How to test?
### Login
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"email":"john@gmail.com", "password": "1234"}' \
  http://localhost:5000/api/login
```


### retrieve_task
```
curl http://localhost:5000/api/task/john@gmail.com
```

### Create task
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"user_id":"1","title":"new","content":"oop","pinned":0}' \
  http://localhost:5000/api/task
```

### Delete task
```
curl --header "Content-Type: application/json" \
  --request DELETE \
  --data '{"task_id": 1}' \
  http://localhost:5000/api/task
```

### Update task
```
curl --header "Content-Type: application/json" \
  --request PUT \
  --data '{"task_id":"2","title":"update","content":"hoho","pinned":1}' \
  http://localhost:5000/api/task
```


## How to view tables
```
http://localhost:5000/api/admin/see_table/user
http://localhost:5000/api/admin/see_table/task
http://localhost:5000/api/admin/see_table/reminder
```