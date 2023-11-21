from flask import Flask
import stripe


app = Flask(__name__)
stripe.api_key = "sk_test_sdjhfhjdsfvsdfsdhfsdfskjhdbfksjbdfkjsbdflksbdfkjsbdf"

@app.route("/")
def hello():
    return "Hello World!"



@app.route('/api/subscription', methods=['POST'])
def create_checkout_session(current_user):
    try:
        prices = stripe.Price.list(
            lookup_keys=[request.form['lookup_key']],
            expand=['data.product']
        )  
        checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': prices.data[0].id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=f"https://episyche.com/home?paymentstatus=true",
                cancel_url=f"https://episyche.com/pushmode?paymentstatus=false",
                allow_promotion_codes=True,
                metadata={
                    "user_id": current_user,
                    "price_id": prices.data[0].id,
                },
                customer_creation="always",
            )
        print("==================checkout_session_object=====================")
        print(checkout_session)
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        print(e)
        return jsonify({'status': True, 'data': [], 'message': f"subscription failed"}), 200


@app.route('/api/webhook', methods=['POST'])
def webhook_received():
    webhook_secret = "whsec_ousdfliksdkfskdfbsweopa,xnbfwe52J"
    try:
        signature = request.headers.get('stripe-signature')
        event = stripe.Webhook.construct_event(
            payload=request.data, sig_header=signature, secret=webhook_secret)

        if(event['type'] == "charge.succeeded"):
            temp_dict = {}
            temp_dict["status"] = "success"
        if(event['type'] == "charge.failed"):
            temp_dict = {}
            temp_dict["status"] = "failed"

        return jsonify({"data": [temp_dict]}), 200
    except Exception as e:
        print(" webhook error",e)
        return jsonify({'message': 'webhook error'}), 500





if __name__ == "__main__":
    app.run()