console.log('Sanity check!');


// Get Stripe publishable key
fetch("/orders/config/")
    .then((result) => result.json())
    .then((data) => {
        console.log(data)
        const stripe = Stripe(data.publicKey);

        // Event Handler
        document.querySelector("#submitBtn")
            .addEventListener("click", () => {
                // Get Checkout Session ID
                fetch("/orders/create-checkout-session/")
                    .then((result) => result.json())
                    .then((data) => {
                        console.log(data);
                        // Redirect to Stripe Checkout
                        return stripe.redirectToCheckout({
                            sessionId: data.sessionId
                        })
                    })
                    .then((res) => {
                        console.log(res);
                    });
            });
    })