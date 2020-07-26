import React from "react";
import "./App.css";
import {send} from "./ipc/handler";

export const App: React.FC = () => {
    return (
        <div className="App">
            <header className="App-header">
                <div className="container d-flex flex-column justify-content-center align-items-center">
                    <div className="menu-container">
                        <h1>App Template</h1>
                        <div className="main-menu">
                            <h2 className="pb-3"> Main Menu </h2>
                            <button type="button" className="btn btn-primary main-menu__option"
                                    onClick={() => send("closeApplication")}>Close
                            </button>
                        </div>
                    </div>
                </div>
                <div className="help">
                    <p className="pt-4">Edit React App in <code>/client</code><br/>Edit Python app
                        in <code>/server</code><br/>See <code>Readme.md</code> for additional information</p>
                </div>
                <div className="icons">
                    <img className="icon" src="https://www.vectorlogo.zone/logos/reactjs/reactjs-ar21.svg"/>
                    <img className="icon  " src="https://www.vectorlogo.zone/logos/python/python-ar21.svg"/>
                </div>
            </header>
        </div>
    );
};

export default App;
