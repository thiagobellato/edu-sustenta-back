import { useState } from "react";
import "./HelpSection.css";
import {Button} from "../../UI/Button.jsx";

export default function HelpSection() {
  const [open, setOpen] = useState(null);

  const topics = [
    {
      title: "Criar e personalizar um perfil",
      content: "Você pode editar seu perfil acessando o menu do usuário."
    },
    {
      title: "Gerenciar cursos",
      content: "Acompanhe seus cursos na área 'Minha conta'."
    }
  ];

  return (
    <div className="help">
      <h2>Ajuda</h2>

      {topics.map((item, index) => (
        <div key={index} className="dropdown">
          <Button onClick={() => setOpen(open === index ? null : index)}>
            {item.title}
          </Button>

          {open === index && <p>{item.content}</p>}
        </div>
      ))}


    </div>
  );
}
