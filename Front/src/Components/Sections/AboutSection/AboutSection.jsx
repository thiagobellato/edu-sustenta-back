import { Card } from '../../UI/Card.jsx';
import './aboutSection.css';

import forest2 from "../../../assets/Images/forest2.png";

export default function AboutSection() {
  return (
    <section
          className="about"
          style={{ backgroundImage: `url(${forest2})` }}
      >   
    <div className="about">
      <h2>Sobre nós</h2>

      <div className="cards">
        <Card
          title="Missão"
          description="Promover educação ambiental acessível e de impacto."
        />

        <Card
          title="Visão"
          description="Ser referência em educação sustentável no Brasil."
        />

        <Card
          title="Valores"
          description="Responsabilidade, inovação, colaboração e ética."
        />
      </div>
    </div>
  </section>
  );
}
