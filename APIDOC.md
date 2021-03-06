# API Documentation
## Login `/api/login` (method = `POST`)
### Params
```ts
interface LoginParams {
	email: string;
	password: string;
}
```
### Response
```ts
interface LoginResponse {
	matching_user_id: number | null;
	session_id: number
}
```

## Login `/api/logout` (method = `POST`)
### Params
```ts
interface LogoutParams {
	session_id: number;
}
```


## Retrieve task `/api/task` (method = `GET`)
### Params
Session_id. For example,
```
http://localhost:5000/api/task/1532420297001
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

## Create task `/api/task` (method = `POST`)
### Params
```ts
interface CreateTaskParam {
	session_id:   number;
	title:     string;
	content:   string;
	pinned:    number; // Either 1 or 0
	reminders: Reminder[];
}

interface Reminder {
	date:       number; // Epoch time in seconds
}
```
### Response 
```ts
inteface Response {
	affected: number;
	id:       number;
}
```

## Delete task `/api/task` (method = `DELETE`)
### Params
```ts
interface DeleteTaskParam {
	session_id: number;
	task_id: 	number;
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

## Update task `/api/task` (method = `PUT`)
### Params
```ts
interface UpdateTaskParam {
	task_id:   number;
	title:     string;
	content:   string;
	pinned:    number; // Either 1 or 0
	reminders: Reminder[];
}

interface Reminder {
	date:       number; // Epoch time in seconds
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

