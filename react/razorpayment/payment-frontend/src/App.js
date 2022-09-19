import "./App.css";
import PaymentButton from "./components/Payment/PaymentButton";
import displayRazorpay from "./components/Payment/utils/RazorpayPaymentGateway";

const App = () => {
    return (
        <div className="App">
            <header className="App-header">
                <p>
                    Make Payment using the Razorpay payment gateway...
                </p>
                <PaymentButton onClick={displayRazorpay}/>
            </header>
        </div>
    );
};

export default App;
