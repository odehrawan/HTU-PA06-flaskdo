DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS TaskList;
DROP TABLE IF EXISTS Task;

-- Create 'User' table
CREATE TABLE User (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT,
  last_name TEXT,
  email TEXT UNIQUE NOT NULL,
  avatarURL TEXT,
  birthdate TEXT,
  address TEXT,
  password TEXT NOT NULL,
  psw TEXT  NOT NULL
);

-- Create 'TaskList' table
CREATE TABLE TaskList (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (user_id) REFERENCES user (id)

  
  
);

-- Create 'Task' table
CREATE TABLE Task (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  task_list_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  priority INTEGER NOT NULL,
  description TEXT,
  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (task_list_id) REFERENCES taskList (id)
   
);