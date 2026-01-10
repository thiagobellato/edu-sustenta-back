import { FaLeaf } from 'react-icons/fa';
import './Navbar.css';

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <FaLeaf className="navbar-icon" />
                <span>Edu-Sustenta</span>
            </div>
            <div className="navbar-links">
                <a href="#">Início</a>
                <a href="#">Sobre</a>
                <button className="nav-btn">Ajuda</button>
            </div>
        </nav>
    );
};

export default Navbar;