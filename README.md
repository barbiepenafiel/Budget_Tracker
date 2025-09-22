# Budget Tracker

A modern, responsive Budget/Expense Tracker web application built with Django REST Framework and TailwindCSS.

## Features

- **Responsive Dashboard**: Works perfectly on desktop and mobile devices
- **Real-time Balance Tracking**: Automatically calculates income vs expenses
- **REST API**: Full CRUD operations with API endpoints
- **Modern UI**: Black and white theme with smooth animations
- **Categories**: Organize transactions by category (Food, Transport, Entertainment, etc.)
- **Transaction Types**: Support for both income and expense entries
- **Real-time Updates**: Instant UI updates without page refresh

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Frontend**: HTML5, TailwindCSS, Vanilla JavaScript
- **Database**: SQLite (default, easily switchable)
- **API**: RESTful JSON API

## Installation & Setup

1. **Clone or download the project**
   ```bash
   cd Budget_Tracker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Create sample data (optional)**
   ```bash
   python manage.py create_sample_data
   ```

8. **Start the development server**
   ```bash
   python manage.py runserver
   ```

9. **Open in browser**
   - Main Dashboard: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## API Endpoints

### Expenses
- `GET /api/expenses/` - List all expenses
- `POST /api/expenses/` - Create new expense
- `GET /api/expenses/{id}/` - Get specific expense
- `PUT /api/expenses/{id}/` - Update expense
- `DELETE /api/expenses/{id}/` - Delete expense

### Summary
- `GET /api/summary/` - Get income/expense summary

### Example API Usage

**Create a new expense:**
```bash
curl -X POST http://127.0.0.1:8000/api/expenses/ \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 25.50,
    "description": "Coffee and pastry",
    "category": "food",
    "transaction_type": "expense"
  }'
```

**Get all expenses:**
```bash
curl http://127.0.0.1:8000/api/expenses/
```

## Features Overview

### Dashboard Components

1. **Summary Cards**
   - Total Income (green)
   - Total Expenses (red)
   - Current Balance (green/red based on value)

2. **Add New Entry Form**
   - Amount input with validation
   - Description text field
   - Category dropdown
   - Transaction type (Income/Expense)
   - Real-time form validation

3. **Transactions Table**
   - Sortable by date (newest first)
   - Color-coded by transaction type
   - Edit and delete buttons for each entry
   - Responsive design for mobile

4. **Edit Modal**
   - Popup form for editing existing transactions
   - Pre-filled with current values
   - Smooth animations

### Design Features

- **Black & White Theme**: Clean, professional appearance
- **Smooth Animations**: Hover effects, fade-in, slide-up animations
- **Mobile Responsive**: Optimized for all screen sizes
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages
- **Success Notifications**: Confirmation messages for actions

### Categories Available

- Food
- Transport
- Entertainment
- Bills
- Healthcare
- Shopping
- Salary
- Freelance
- Investment
- Other

## Project Structure

```
Budget_Tracker/
├── budget_tracker/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── expenses/                # Main app
│   ├── models.py           # Expense model
│   ├── views.py            # API and template views
│   ├── serializers.py      # DRF serializers
│   ├── urls.py             # URL patterns
│   ├── admin.py            # Admin configuration
│   └── management/         # Custom commands
├── templates/              # HTML templates
│   └── expenses/
│       └── dashboard.html  # Main dashboard
├── static/                 # Static files
├── requirements.txt        # Python dependencies
└── manage.py              # Django management script
```

## Default Admin User

If you used the setup script, a default admin user is created:
- **Username**: admin
- **Password**: admin123
- **Email**: admin@example.com

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues, please create an issue in the repository.

---

**Happy budgeting! 💰**
