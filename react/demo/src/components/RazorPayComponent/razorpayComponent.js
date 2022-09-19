import "./style.css"
import * as Razorpay from "razorpay";

function loadScript(src) {
    return new Promise((resolve) => {
        const script = document.createElement('script')
        script.src = src
        script.onload = () => {
            resolve(true)
        }
        script.onerror = () => {
            resolve(false)
        }
        document.body.appendChild(script)
    })
}

async function displayRazorpay() {
    const res = await loadScript('https://checkout.razorpay.com/v1/checkout.js')

    if (!res) {
        alert('Razorpay SDK failed to load. Are you online?')
        return
    }
    // Here's where you call the backend to create an razorpay order id and send it back to you
    const data = await fetch('/payment/create_order', { method: 'POST' }).then((t) =>
        t.json()
    )

    console.log(data)

    const options = {
        key: 'rzp_test_csFXBrtAla4nqI',
        currency: data.currency,
        amount: data.amount.toString(),
        order_id: data.id,
        name: 'Make Payment',
        description: 'GDO Retail',
        image: 'http://localhost:1337/logo.svg',
        handler: function (response) {
            alert(response.razorpay_payment_id)
            alert(response.razorpay_order_id)
            alert(response.razorpay_signature)
        },
        prefill: {
            name: "",
            email: "",
            phone_number: "",
        }
    }
    const paymentObject = new window.Razorpay(options)
    paymentObject.open()
}

const RazorpayComponent = () => {
    return(
        <div id="container">
        <div class="button" id="razorpay-button" onClick={displayRazorpay}>
            <div id="dub-arrow"><img
                src="https://github.com/atloomer/atloomer.github.io/blob/master/img/iconmonstr-arrow-48-240.png?raw=true"
                alt=""/></div>
            <a href="#">Make Payment!</a>
        </div>
        </div>
    );
}
export default RazorpayComponent;

