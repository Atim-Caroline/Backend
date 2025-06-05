# Aalysis platform

A Django-based platform for managing social media analytics and post scheduling.

## Features

- Social Media Account Management (Facebook, Instagram)
- Analytics Dashboard
- Post Scheduling
- Trend Analysis
- Automated Reports
- User Authentication and Authorization

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd Final
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
Final/
├── analytics/          # Analytics app
├── scheduler/          # Post scheduling app
├── trends/            # Trend analysis app
├── social_insights/    # Main project directory
├── templates/         # HTML templates
├── static/           # Static files
├── requirements.txt  # Project dependencies
└── manage.py        # Django management script
```

## Configuration

1. Create a `.env` file in the project root:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
```

2. Configure social media API keys in Django admin.

## Usage

1. Access admin interface at `/admin/`
2. Configure social media accounts
3. View analytics at `/analytics/`
4. Schedule posts at `/scheduler/`
5. Monitor trends at `/trends/`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
