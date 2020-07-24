import React from 'react';
import logo from './logo.svg';
import './App.css';
import config from "./config";

const socket = new WebSocket(`ws://${config.ipc.host}:${config.ipc.port}`)

function App() {

    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo"/>
                <p>
                    Edit <code>src/App.tsx</code> and save to reload.
                </p>
                <a
                    className="App-link"
                    href="https://reactjs.org"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Learn React
                </a>
                <button
                    onClick={() => socket.send(JSON.stringify({action: "closeApp", params: {}}))}>Close
                    App!
                </button>
            </header>
        </div>
    );
}

export default App;
