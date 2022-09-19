import axios from "axios";

const loadScript = (src) => {
  return new Promise((resolve) => {
    const script = document.createElement("script");
    script.src = src;
    script.onload = () => {
      resolve(true);
    };
    script.onerror = () => {
      resolve(false);
    };
    document.body.appendChild(script);
  });
};

export default async function displayRazorpay() {
  //load the Razorpay checkout script
  const res = await loadScript('https://checkout.razorpay.com/v1/checkout.js')

  if (!res) {
    alert('Razorpay checkout script failed to load. Please check your internet connection and try to reload the page?');
    return;
  }

  // Prepare for the payment initiation - Send the relevant data for the backend to be able to compute the total amount of the order
  const user_data = {
    user_id: "X123X45",
    user_name: 'James Bond',
    user_email: 'james@bond.com',
    user_mobile: '0987654321'
  }

  // Send the data to the backend to create an order and return back the order_id and details
  const razorpay_order_data = await axios.post("/payment/create_razorpay_order", user_data)
      .then(res => res.data)
      .catch(err => console.log(err))

  console.log(razorpay_order_data);

  const options = {
    key: process.env.REACT_APP_RAZORPAY_KEY_ID,
    order_id: razorpay_order_data.id,
    currency: razorpay_order_data.currency,
    amount: razorpay_order_data.amount,
    name: "GDO Retail",
    description: "Order payment",
    handler: function (response) {
      //Payment successful
      // alert("PAYMENT ID ::" + response.razorpay_payment_id);
      // alert("ORDER ID :: " + response.razorpay_order_id);
      alert("Thanks for making the payment...");
    },
    prefill: {
      name: user_data.user_name,
      email: user_data.user_email,
      contact: user_data.user_mobile,
    },
  };

  // Initiate payment - open the Razorpay modal

  const paymentObject = new window.Razorpay(options);
  paymentObject.open();
}
