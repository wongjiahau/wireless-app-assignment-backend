# API Documentation

## `/api/retrieve_task`
### Params
No need
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
	date:		number; // Epoch time in seconds
	id:			number;
	task_id:	number;
}
```