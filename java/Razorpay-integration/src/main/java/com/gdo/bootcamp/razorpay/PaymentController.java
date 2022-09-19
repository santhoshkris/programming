package com.gdo.bootcamp.razorpay;

import java.util.Map;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import com.razorpay.*;

@Controller
@RequestMapping("/payment")
@PropertySource("classpath:application.properties")
public class PaymentController {
    @Autowired
    private Environment env;

    @GetMapping("")
    public String paymentsHome() {
        return "payment";
    }

    @PostMapping("/create_razorpay_order")
    @ResponseBody
    public String createOrder(@RequestBody Map<String, Object> order_data) throws RazorpayException {

        System.out.println("------------------------------------------");
        System.out.println("Order received...");
        System.out.println("------------------------------------------");
        System.out.println("Razorpay Key: " + env.getProperty("payments.razorpay.key"));
        System.out.println("Razorpay Secret: " + env.getProperty("payments.razorpay.secret"));
        System.out.println(order_data);
        // fetch the cart details for the user and compute the total amount
        int amount = 100;
        String currency = "INR"; // this should be configurable
        var rzp_client = new RazorpayClient(env.getProperty("payments.razorpay.key"),
                env.getProperty("payments.razorpay.secret"));
        JSONObject options = new JSONObject();
        options.put("amount", amount * 100);
        options.put("currency", currency);
        options.put("receipt", "txn_123456");
        Order order = rzp_client.orders.create(options);
        System.out.println("Order created...\n" + order);
        System.out.println("------------------------------------------");
        return order.toString();
    }

    @PostMapping("/verify_razorpay_payment")
    @ResponseBody
    public String verifyPayment(@RequestHeader Map<String, Object> header, @RequestBody String data) {
        System.out.println("------------------------------------------");
        System.out.println("Verification request has come through... ");
        System.out.println("------------------------------------------");
        System.out.println("Header is: " + header);
        System.out.println("Signature in Header is: " + header.get("x-razorpay-signature"));
        System.out.println("Data is: " + data);
        JSONObject jObject = new JSONObject(data);
        JSONObject entity = (((jObject.getJSONObject("payload"))).getJSONObject("payment")).getJSONObject("entity");
        System.out.println("Entire data JSON Object is: " + jObject.toString());
        System.out.println("Entity JSON Object is: " + entity.toString());
        String payment_id = entity.getString("id");
        String order_id = entity.getString("order_id");
        String status = entity.getString("status");
        System.out.println("payment id: " + payment_id + " order_id: " + order_id + " status: " + status);

        try {
            boolean result = Utils.verifyWebhookSignature(data, header.get("x-razorpay-signature").toString(),
                    env.getProperty("payments.razorpay.verification.secret"));
            System.out.println("Signature verification status: " + result);
            if (result) {
                if (entity.getString("status").equals("captured")) {
                    System.out.println("Payment captured and verified...");
                } else {
                    System.out.println("Payment didn't go through...pls check the same...");
                }
            } else {
                System.out.println("Payment failed to verify...");
            }
        } catch (RazorpayException e) {
            e.printStackTrace();
        }
        System.out.println("------------------------------------------");
        return "";
    }
}
