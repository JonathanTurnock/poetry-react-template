# Poetry React Template
Template Python project which uses Python Flask and React to serve a standalone web application with a React UI.

## 🎟 Installation & Usage
⚠ NOTE: Project management will require Poetry https://python-poetry.org/

Clone the project and run the application using
```bash
    $ poetry install && poetry run dev
```

## 🏗 Development
### Setup
#### 🐍 Python
* Install Python https://www.python.org/
* Install Poetry
```bash
    $ pip3 install poetry
```
* Configure Project
```bash
    $ poetry install
```
* Confirm Tests Run
```bash
    $ poetry run test
```

#### ⚛ Node & React
* Install NodeJS https://nodejs.org/en/
* Install Yarn
```bash
    $ npm install -g yarn
```

### 👨‍💻 Local Environment
Start the application with Dev environment settings using
```bash
    $ poetry run dev
```

To run the React Application separately using the development server run
```bash
    $ poetry run react-app
```

⚠️ NOTE: This will cause requests to be proxied to `127.0.0.1:5000`

### 📦 Build
Build the application using
```bash
   $ poetry run build
```

### 🚢 Release
TBC

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## ⚖️ License
TBC 
