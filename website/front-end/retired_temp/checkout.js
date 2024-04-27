// This is your test publishable API key.
const stripe = Stripe("pk_live_51PACDsA9jJc3aGYgDGcDNozqerUaEur80oY9gZuslOvsrFGUTun0cluVU8hNWhO6XMkusDY3AlYo7LanJn70r2ET00VNxSeW4Y");

initialize();

// Create a Checkout Session
async function initialize() {
  const fetchClientSecret = async () => {
    const response = await fetch("http://localhost:5001/create-checkout-session", {
      method: "POST",
    });

    console.log(response);

    const { clientSecret } = await response.json();

    return clientSecret;
  };


  const checkout = await stripe.initEmbeddedCheckout({
    fetchClientSecret,
  });

  // Mount Checkout
  checkout.mount('#checkout');
}