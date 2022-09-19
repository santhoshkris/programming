import "./css/style.css"

const PaymentButton = (props) => {
  return (
        <button className="btn" onClick={props.onClick}><span>Pay!</span></button>
  );
};

export default PaymentButton;
