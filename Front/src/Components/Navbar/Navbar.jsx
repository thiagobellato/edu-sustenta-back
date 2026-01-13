import { FaLeaf } from "react-icons/fa";
import "./Navbar.css";

const Navbar = ({ onNavigate }) => {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <FaLeaf className="navbar-icon" />
        <span>Edu-Sustenta</span>
      </div>

      <div className="navbar-links">
        <button onClick={() => onNavigate("home")}>Início</button>
        <button onClick={() => onNavigate("about")}>Sobre</button>
        <button className="nav-btn" onClick={() => onNavigate("help")}>
          Ajuda
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
