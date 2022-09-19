import logo from './logo.svg';
import './App.css';
import RazorpayComponent from "./components/razorpay-component";


function App() {

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
          <RazorpayComponent/>
      </header>
    </div>
  );
}

export default App;
