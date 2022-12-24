import {Link} from "react-router-dom"
import './App.css';


export default function App(){
    return (
        <div>
            <h1>Camera Vehicle Manager</h1>
            <nav
                    style={{
                    borderBottom: "solid 1px",
                    paddingBottom: "1rem",
                    }}
                >
                <Link to="/setting">Setting</Link>
                <Link to="/region">Region</Link>
                <Link to="/test">Test</Link>
            </nav>
        </div>
    )
}