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
### get_task
```
curl http://localhost:5000/api/get_task/john@gmail.com
```

### new_task
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"user_id":"1","title":"new","content":"oop","pinned":0}' \
  http://localhost:5000/api/new_task
```

## How to view tables
```
http://localhost:5000/api/admin/see_table/user
http://localhost:5000/api/admin/see_table/task
http://localhost:5000/api/admin/see_table/reminder
```