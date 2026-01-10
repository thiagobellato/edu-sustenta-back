import { FaFacebook, FaInstagram, FaLinkedin, FaEnvelope, FaPhone } from 'react-icons/fa';
import './Footer.css';

const Footer = () => {
    return (
        <footer className="site-footer">
            <div className="footer-container">
                <div className="footer-column">
                    <h3>Edu-Sustenta</h3>
                    <p>Transformando a educação através da sustentabilidade. Junte-se a nós para um futuro mais verde.</p>
                </div>
                <div className="footer-column">
                    <h4>Contato</h4>
                    <p><FaEnvelope /> contato@edusustenta.com</p>
                    <p><FaPhone /> (24) 2233-4455</p>
                    <div className="social-icons">
                        <a href="#"><FaFacebook /></a>
                        <a href="#"><FaInstagram /></a>
                        <a href="#"><FaLinkedin /></a>
                    </div>
                </div>
            </div>
            <div className="footer-bottom">
                <p>© 2026 Edu-Sustenta. Todos os direitos reservados.</p>
            </div>
        </footer>
    );
};

export default Footer;