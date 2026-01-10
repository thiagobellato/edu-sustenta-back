import { useState } from 'react';
import { FaUser, FaLock } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import './Login.css';

const Login = () => {
    const [username, setUsername] = useState("");  
    const [password, setPassword] = useState("");

    const handleSubmit = (event) => {
        event.preventDefault();  
       
        alert("Login efetuado! Usuário: " + username);
    }

    return (
        <div className="content-wrap">
            <form onSubmit={handleSubmit}> 
                <h1>Acesse o Sistema</h1>
                
                <div className='input-field'>
                    <input 
                        type="email" 
                        placeholder="E-mail" 
                        required 
                        value={username}  
                        onChange={(e) => setUsername(e.target.value)}  
                    />
                    <FaUser className='icon' />
                </div>

                <div className='input-field'>
                    <input 
                        type="password" 
                        placeholder="Senha" 
                        required 
                        value={password}  
                        onChange={(e) => setPassword(e.target.value)}  
                    />
                    <FaLock className='icon' />
                </div>

                <div className='recall-forget'>
                    <label>
                        <input type='checkbox' />
                        Lembrar de mim?
                    </label>
                </div>

                <button type="submit">Entrar</button>
                
                <div className='singnup-link'>
                    <p>Não tem uma conta? <Link to="/cadastro">Registrar</Link></p>
                </div>
            </form>
        </div>
    );
}

export default Login;