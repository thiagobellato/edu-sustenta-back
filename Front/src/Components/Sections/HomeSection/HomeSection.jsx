import { Button } from "../../UI/Button.jsx";
import "./homeSection.css";
import forest1 from '../../../assets/Images/forest1.png';

export default function HomeSection() {
  return (
  <section className="home"
    style={{ backgroundImage: `url(${forest1})` }}
    >
    <div className="overlay">
      <h1>EduSustenta</h1>

      <p>
        Aprendendo a cuidar do nosso futuro.
        <br />
        Conectamos escolas, professores e alunos na jornada do conhecimento
        sobre sustentabilidade.
      </p>

      {/* <Button variant="secondary">Cancelar</Button> */}
      <Button onClick = {() => "/login"}>Acessar Plataforma</Button>

      <span className="link">
        Ainda não faz parte? <a href="/cadastro">Cadastre-se</a>
      </span>
    </div>
    </section>
  );
}
