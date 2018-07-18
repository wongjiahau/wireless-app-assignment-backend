# API Documentation

## `/api/retrieve_task`
### Params
Email. For example,
```
http://localhost:5000/api/retrieve_task/john@gmail.com
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

## `/api/create_task`
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

## `/api/delete_task`
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

## `/api/update_task`
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

