import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

import HomeSection from "../../Sections/HomeSection/HomeSection";
import AboutSection from "../../Sections/AboutSection/AboutSection";
import HelpSection from "../../Sections/HelpSection/HelpSection";

import "./landing.css";

export default function LandingPage() {
  const navigate = useNavigate();

  const homeRef = useRef(null);
  const aboutRef = useRef(null);
  const helpRef = useRef(null);

  useEffect(() => {
    const sections = [
      { ref: homeRef, path: "/" },
      { ref: aboutRef, path: "/sobre" },
      { ref: helpRef, path: "/ajuda" },
    ];

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const section = sections.find(
              (s) => s.ref.current === entry.target
            );
            if (section) {
              navigate(section.path, { replace: true });
            }
          }
        });
      },
      { threshold: 0.6 }
    );

    sections.forEach((section) => {
      if (section.ref.current) {
        observer.observe(section.ref.current);
      }
    });

    return () => observer.disconnect();
  }, [navigate]);

  return (
    <main>
      <section ref={homeRef} className="section">
        <HomeSection />
      </section>

      <section ref={aboutRef} className="section">
        <AboutSection />
      </section>

      <section ref={helpRef} className="section">
        <HelpSection />
      </section>
    </main>
  );
}
