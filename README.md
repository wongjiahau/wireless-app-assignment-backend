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
### retrieve_task
```
curl http://localhost:5000/api/retrieve_task/john@gmail.com
```

### create_task
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"user_id":"1","title":"new","content":"oop","pinned":0}' \
  http://localhost:5000/api/create_task
```

### delete_task
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"task_id": 1}' \
  http://localhost:5000/api/delete_task
```

### update_task
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"task_id":"2","title":"update","content":"hoho","pinned":1}' \
  http://localhost:5000/api/update_task
```


## How to view tables
```
http://localhost:5000/api/admin/see_table/user
http://localhost:5000/api/admin/see_table/task
http://localhost:5000/api/admin/see_table/reminder
```