# API Documentation

## Retrieve task `/api/task` (method = `GET`)
### Params
Email. For example,
```
http://localhost:5000/api/task/john@gmail.com
```
### Response 
```ts
type Response = Task[]

interface Task {
	user_id:	number;
	id: 		number;
	title:		string;
	content: 	string;
	reminder:	Reminder[];
	
}

interface Reminder {
	date:       number; // Epoch time in seconds
	id:         number;
	task_id:    number;
}
```

<hr>

## Update task `/api/task` (method = `PUT`)
### Params
```ts
interface CreateTaskParam {
	user_id: number;
	title:   string;
	content: string;
	pinned:  number; // Either 1 or 0
}
```
### Response 
```ts
inteface Response {
	affected: number;
	id:       number;
}
```

## Delete task `/api/delete_task` (method = `DELETE`)
### Params
```ts
interface DeleteTaskParam {
	task_id: number;
}
```
### Response 
```ts
inteface Response {
	affected: number;
	id:       number;
}
```
<hr>

## Update task `/api/update_task` (method = `POST`)
### Params
```ts
interface DeleteTaskParam {
	task_id:   number;
	title:     string;
	content:   string;
	pinned:    number; // Either 1 or 0
}
```
### Response 
```ts
inteface Response {
	affected: number;
	id:       number;
}
```
<hr>

