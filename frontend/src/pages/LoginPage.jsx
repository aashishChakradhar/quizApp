import React,{useState} from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/authService';

export default function LoginForm(props){
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    
    const handleSubmit = async e => {
        e.preventDefault();
        try {
            await login(username, password);
            navigate('/dashboard');
        } catch (err) {
            alert('Login failed');
        }
    };
    return <form action="" method="post" onSubmit={handleSubmit}>
        <div>Login</div>
        <label htmlFor="username">Username
            <input type="text" name="username" id="username" value={username} onChange={e=> setUsername(e.target.value)}/>
        </label>
        <label htmlFor="password">Password
            <input type="password" name="password" id="password" value={password} onChange={e => setPassword(e.target.value)}/>
        </label>
        <button type="submit">Login</button>
    </form>
}
