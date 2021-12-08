console.log("sanity check!");

// Get Stripe publishable key
fetch("/subscriptions/config/")
  .then((result) => result.json())
  .then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);
    console.log(stripe);

    // Event Handler
    let submitBtn = document.querySelector("#submitBtn");
    if (submitBtn !== null) {
      submitBtn.addEventListener("click", () => {
        
        // Get Checkout Session ID
        fetch("/subscriptions/create-checkout-session/")
          .then((result) => result.json())
          .then((data) => {
            console.log(data);
            // Redirect to Stripe Checkout
            return stripe.redirectToCheckout({sessionId: data.sessionId})
          })
        .then((res) => console.log(res))
      });
      
    }
  });
