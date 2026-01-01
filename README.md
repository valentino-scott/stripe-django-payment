# Card Payment Integration with Stripe (Django)

A Django web application that integrates **Stripe card payments**, allowing users to securely purchase premium products or services.

---

## 🚀 Features

* Stripe Checkout integration
* Secure card payments
* Demo products: Basic & Premium
* Success & cancel payment pages
* Environment-based configuration
* Follows Django best practices

---

## 🛠️ Tech Stack

* Python 3.x
* Django 4.x
* Stripe API
* HTML / CSS / JavaScript
* SQLite (default database)

---

## 📦 Installation

### 1️⃣ Clone the repository

```
git clone https://github.com/valentino-scott/stripe-django-payment.git
cd stripe-django-payment
```

### 2️⃣ Create a virtual environment

```
python3 -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Setup environment variables

Create a `.env` file based on `.env.example`:

```
DJANGO_SECRET_KEY=your_django_secret_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
DEBUG=True
```

### 5️⃣ Apply database migrations

```
python manage.py migrate
```

### 6️⃣ Create a superuser (optional for admin)

```
python manage.py createsuperuser
```

### 7️⃣ Run the development server

```
python manage.py runserver
```

Open your browser and go to:

```
http://127.0.0.1:8000/
```

---

## 💳 Stripe Setup

1. Create a Stripe account: [https://stripe.com](https://stripe.com)
2. Get your **Test API keys**
3. Add them to your `.env` file:

```
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxx
```

---

## 🔔 Webhooks (Optional)

If you want to test Stripe webhooks locally:

```
stripe listen --forward-to localhost:8000/webhook/
```

---

## 🧪 Test Cards

Use Stripe’s test card for payments:

```
Card number: 4242 4242 4242 4242
Expiry date: Any future date
CVC: Any 3 digits
```

---

## 📄 License

MIT License

---

## 👨‍💻 Author

@valentinoachira
