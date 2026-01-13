// import style from './style.css';
export const Button = ({ children, variant = "primary", onClick }) => {
  return (
    <button className={`btn btn-${variant}`} onClick={onClick}>
      {children}
    </button>
  );
};
