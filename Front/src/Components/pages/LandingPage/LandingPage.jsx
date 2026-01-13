import HomeSection from "../../Sections/HomeSection/HomeSection.jsx";
import AboutSection from "../../Sections/AboutSection/AboutSection.jsx";
import HelpSection from "../../Sections/HelpSection/HelpSection.jsx";
import "./landing.css";
import MegaForest from "../../../assets/Images/MegaForest.png";


export default function LandingPage({homeRef, aboutRef, helpRef}) {
 

  return (
     <>
        <section
    //   style={{ backgroundImage: `url(${MegaForest})` }}
    >
    
   
      {/* <Navbar scrollTo={scrollTo} /> */}

      <section ref={homeRef}>
        <HomeSection />
      </section>

      <section ref={aboutRef}>
        <AboutSection />
      </section>

      <section ref={helpRef}>
        <HelpSection />
      </section>
    
    
        </section>
    </>
  );
}
