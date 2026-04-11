# Hume Social

*Twitter without the noise. Wikipedia with original research.*

A platform for structured intellectual discourse where quality emerges from community validation rather than centralized moderation.

## 🎯 Project Aim and Philosophy

Hume Social is designed to foster meaningful intellectual discourse across all domains of human knowledge by enforcing structured argumentation and community-driven quality control. Our philosophy is rooted in the belief that:

- **Quality over Quantity**: Every contribution must follow rigorous logical structure
- **Community Validation**: Truth emerges from distributed peer review, not algorithmic curation
- **Progressive Engagement**: Users earn capabilities through demonstrated competence
- **Structured Thinking**: Complex topics require clear premises, facts, and conclusions

We reject the attention-driven model of social media in favor of a reputation-driven ecosystem where intellectual rigor is rewarded, regardless of the domain - be it philosophy, science, politics, or policy analysis.

## 👥 Target Audience

- **Researchers and Academics**: Scholars across disciplines seeking structured debate platforms
- **Policy Makers and Analysts**: Government officials and think tank researchers
- **Scientists and Engineers**: Technical professionals engaging in rigorous discourse
- **Intellectually Curious Individuals**: Those interested in deep, meaningful discussions on any topic
- **Students and Educators**: Learning environments for critical thinking development
- **Journalists and Media Professionals**: Fact-based analysis and structured argumentation
- **Anyone Seeking Quality Discourse**: Users tired of social media's superficiality

## 💡 Use Cases

### For Individuals
- **Create Structured Arguments**: Build and share well-reasoned theses on any intellectual topic
- **Learn Through Discourse**: Engage with diverse perspectives on complex issues
- **Build Intellectual Reputation**: Earn recognition through quality contributions
- **Discover Quality Content**: Personalized feed based on interests and rigor

### For Communities
- **Academic Discussions**: Structured debates across all disciplines
- **Policy Analysis**: Rigorous examination of political and social issues
- **Scientific Discourse**: Peer review and validation of research arguments
- **Research Collaboration**: Cross-disciplinary validation of complex arguments
- **Educational Forums**: Teaching critical thinking through structured discourse

### For Organizations
- **Think Tanks**: Structured analysis of policy and political issues
- **Research Institutions**: Platform for scholarly discourse across fields
- **Government Agencies**: Rigorous policy development and analysis
- **Scientific Organizations**: Structured scientific debate and validation
- **Educational Institutions**: Interdisciplinary learning environments

## 🛠 Tech Stack

### Backend
- **Python 3.12**: Core programming language
- **Django 4.2.7**: Web framework with custom user model
- **Django REST Framework**: API capabilities
- **PostgreSQL**: Primary database (SQLite for development)

### Frontend
- **HTMX**: Dynamic interactions without JavaScript complexity
- **Django Templates**: Server-side rendering
- **CSS**: Custom styling

### Development & Testing
- **pytest**: Testing framework with Django integration
- **Pylint**: Code quality analysis (10.00/10 score achieved)
- **Black**: Code formatting
- **isort**: Import sorting

### Infrastructure
- **Docker**: Containerization (planned)
- **PostgreSQL**: Production database
- **Redis**: Caching and session storage (planned)

## 🔄 How It Works

### 1. Structured Content Creation
Users create **MiniTheses** following strict logical structure:
- **Facts**: Evidence and data supporting the argument
- **Normative Premises**: Ethical or value-based assumptions
- **Conclusion**: Logical outcome of the reasoning
- **Limits**: Scope and boundaries of the argument

### 2. Community Validation System
Content undergoes distributed peer review through **tagging**:
- Community members vote on content quality tags
- Tags are resolved through consensus algorithms
- Each validated thesis receives a **rigor score** (0-2 scale)
- Higher scores indicate greater intellectual credibility

### 3. Progressive User Permissions
Users advance through capability levels based on demonstrated competence:
- **Reader**: Basic access to view content
- **Commentator**: Can participate in discussions
- **Tagger**: Can validate content through voting
- **Reviewer**: Full editorial oversight capabilities

### 4. Personalized Content Discovery
The **feed algorithm** matches content to users based on:
- **User Preferences**: Topics and rigor thresholds
- **Tag Accuracy**: User's voting history success rate
- **Reputation**: Community standing and sponsorship relationships
- **Interaction History**: Past engagement patterns

### 5. Reputation and Sponsorship
- **Tag Accuracy Scoring**: Measures voting quality over time
- **Sponsorship Network**: Experienced users mentor newcomers
- **Founder Cohorts**: Structured onboarding for new communities
- **Reputation System**: Influences content visibility and user capabilities

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- PostgreSQL (recommended) or SQLite (development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hume_social.git
   cd hume_social
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements/local.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   cd src
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

### Testing

```bash
# Run all tests
cd src
python manage.py test

# Run specific tests
python -m pytest apps/users/tests.py apps/theses/tests.py -v
```

## 📁 Project Structure

```
hume_social/
├── src/                          # Django project root
│   ├── manage.py                # Django management script
│   ├── config/                  # Project configuration
│   │   ├── settings/           # Environment-specific settings
│   │   └── urls.py             # Main URL configuration
│   └── apps/                   # Django applications
│       ├── users/              # Custom user model & auth
│       ├── theses/             # MiniThesis content management
│       ├── tags/               # Community tagging system
│       ├── moderation/         # Content moderation
│       ├── feed/               # Personalized content discovery
│       └── sponsorship/        # User onboarding & mentoring
├── requirements/               # Python dependencies
├── static/                     # Static files
├── media/                      # User-uploaded content
├── docs/                       # Documentation
├── diagrams/                   # Architecture diagrams (gitignored)
└── tests/                      # Test utilities
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

## 🙏 Acknowledgments

- Inspired by intellectual traditions of structured argumentation across all disciplines
- Built on the principles of distributed quality control
- Dedicated to fostering meaningful intellectual discourse in the digital age

