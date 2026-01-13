import './style.css';

export const Card = ({ title, description }) => {
  return (
    <div className="card"> 
        <h3>{title}</h3>
        <div className="underline">
          <p>{description}</p>
        </div>
        
    </div>
  );
}