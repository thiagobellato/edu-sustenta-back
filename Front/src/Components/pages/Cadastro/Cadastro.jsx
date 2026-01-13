import { useState } from 'react';
import { FaUser, FaLock, FaEnvelope } from 'react-icons/fa';
import { Link, useNavigate } from 'react-router-dom';
import { registrarUsuario } from '../../../services/api';
import './Cadastro.css';


const Cadastro = () => {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [role, setRole] = useState(null);

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!name.trim()) {
            alert("Por favor, preencha seu nome completo.");
            return;
        }

        if (password !== confirmPassword) {
            alert("As senhas não coincidem!");
            return;
        }

        if (!role) {
            alert("Por favor, selecione se você é Aluno ou Professor.");
            return;
        }

        const novoUsuario = {
            nome: name,
            email: email,
            password: password,
            role: role,
            ativo: true
        };

        try {
            const response = await registrarUsuario(novoUsuario);

            if (response && response.ok) {
                alert("Cadastro realizado com sucesso!");
                setName("");
                setEmail("");
                setPassword("");
                setConfirmPassword("");
                setRole(null);
            } else {
                alert("Erro ao cadastrar usuário no servidor.");
            }
        } catch (error) {
            console.error(error);
            alert("Erro de conexão com o servidor.");
        }
    };

    return (
   
        <div className="content-wrap">
            <form onSubmit={handleSubmit}>
                <h1>Crie sua Conta</h1>

                <div className='input-field'>
                    <input 
                        type="text" 
                        placeholder="Nome Completo" 
                        required 
                        value={name} 
                        onChange={(e) => setName(e.target.value)} 
                    />
                    <FaUser className='icon' />
                </div>

                <div className='input-field'>
                    <input 
                        type="email" 
                        placeholder="E-mail" 
                        required 
                        value={email} 
                        onChange={(e) => setEmail(e.target.value)} 
                    />
                    <FaEnvelope className='icon' />
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

                <div className='input-field'>
                    <input 
                        type="password" 
                        placeholder="Confirmar Senha" 
                        required 
                        value={confirmPassword} 
                        onChange={(e) => setConfirmPassword(e.target.value)} 
                    />
                    <FaLock className='icon' />
                </div>

                <div className='role-container'>
                    <p>Eu sou:</p>
                    <div className='role-options'>
                        <label>
                            <input 
                                type="checkbox" 
                                checked={role === "ALUNO"} 
                                onChange={() => setRole("ALUNO")} 
                            /> Aluno
                        </label>
                        <label>
                            <input 
                                type="checkbox" 
                                checked={role === "PROFESSOR"} 
                                onChange={() => setRole("PROFESSOR")} 
                            /> Professor
                        </label>
                    </div>
                </div>

                <button type="submit">Cadastrar</button>

                <div className='singnup-link'>
                    <p>Já tem uma conta? <Link to="/login">Entrar</Link></p>
                </div>
            </form>
        </div>
       
    );
};

export default Cadastro;