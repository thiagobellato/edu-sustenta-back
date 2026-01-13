import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import {useRef, useEffect} from 'react';
import Login from "./Components/pages/Login/Login";
import Cadastro from "./Components/pages/Cadastro/Cadastro";
import LandingPage from './Components/pages/LandingPage/LandingPage';
import Navbar from "./Components/Navbar/Navbar";
import Footer from "./Components/Footer/Footer";


export default function AppRoutes() {
  const navigate = useNavigate();
  const location = useLocation();
  const homeRef = useRef(null);
  const aboutRef = useRef(null);
  const helpRef = useRef(null);

  const scrollTo = (section) => {
    const map = {
      home: homeRef,
      about: aboutRef,
      help: helpRef,
    };

    map[section]?.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleNav = (section) => {
    if (location.pathname === "/") {
      scrollTo(section);
    } else {
      navigate("/", { state: { scrollTo: section } });
    }
  };

  useEffect(() => {
    if (location.pathname === "/" && location.state?.scrollTo) {
      scrollTo(location.state.scrollTo);
    }
  }, [location]);

  return (
  
      <div className="main-container">
        <Navbar onNavigate={handleNav}/>
        
        <Routes>
          {/* <Route path="/" element={<Navigate to="/login" />} /> */}
          <Route path="/" element={<LandingPage 
              homeRef={homeRef}
              aboutRef={aboutRef}
              helpRef={helpRef}/>} />
          <Route path="/login" element={<Login />} />
          <Route path="/cadastro" element={<Cadastro />} />
        </Routes>

        <Footer />
      </div>
    
  );
}

