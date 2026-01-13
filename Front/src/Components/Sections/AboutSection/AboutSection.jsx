import Card from '../../UI/Card.jsx';
export default function AboutSection() {
  return (
    <div className="about">
      <h2>Sobre nós</h2>

      <div className="cards">
        <div className="card">
          <h3>Missão</h3>
          <p>Promover educação ambiental acessível e de impacto.</p>
        </div>

        <div className="card">
          <h3>Visão</h3>
          <p>Ser referência em educação sustentável no Brasil.</p>
        </div>

        <div className="card">
          <h3>Valores</h3>
          <p>Responsabilidade, inovação, colaboração e ética.</p>
        </div>
      </div>
    </div>
  );
}
