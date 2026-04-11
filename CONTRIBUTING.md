# Contributing to Hume Social

Thank you for your interest in contributing to Hume Social! We welcome contributions from the community that align with our philosophy of structured, quality-driven discourse.

## 🎯 Our Philosophy

Before contributing, please understand our core principles:

- **Quality over Quantity**: All contributions must maintain high standards
- **Structured Thinking**: Code should be well-architected and thoroughly tested
- **Community Focus**: Changes should benefit the intellectual discourse ecosystem
- **Progressive Enhancement**: Build upon existing foundations thoughtfully

## 👑 Maintainership

**Main Maintainer**: @kakch (Project Creator)

The main maintainer has final authority on:
- Project direction and philosophy
- Code quality standards
- Feature prioritization
- Release decisions

## 📋 Contribution Types

### 🐛 Bug Reports
- Use the issue tracker on GitHub
- Include detailed reproduction steps
- Provide environment information
- Suggest potential fixes if possible

### ✨ Feature Requests
- Check existing issues first
- Clearly describe the problem you're solving
- Explain how it aligns with project philosophy
- Consider implementation complexity

### 💻 Code Contributions
- Follow our coding standards
- Include comprehensive tests
- Update documentation
- Ensure backward compatibility

### 📚 Documentation
- Improve existing documentation
- Add examples and tutorials
- Create architectural diagrams
- Maintain API documentation

## 🚀 Development Workflow

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/hume_social.git
cd hume_social

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/local.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Run migrations
cd src
python manage.py migrate

# Create test data (optional)
python manage.py createsuperuser
```

### 2. Development Process

1. **Choose an Issue**: Pick from existing issues or create a new one
2. **Create a Branch**: Use descriptive branch names
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number-description
   ```
3. **Write Code**: Follow our coding standards
4. **Write Tests**: Ensure comprehensive test coverage
5. **Run Quality Checks**:
   ```bash
   # Run tests
   python manage.py test

   # Check code quality
   pylint src/apps/ --disable=C0114,C0115,C0116

   # Format code
   black src/
   isort src/
   ```
6. **Update Documentation**: Modify README.md or create docs as needed
7. **Commit Changes**: Write clear, descriptive commit messages

### 3. Pull Request Process

1. **Push your branch** to your fork
2. **Create a Pull Request** with:
   - Clear title describing the change
   - Detailed description of what was changed and why
   - Reference to any related issues
   - Screenshots for UI changes
3. **Address Review Comments** promptly
4. **Merge** once approved

## 📏 Coding Standards

### Python Code Quality
- **Pylint Score**: Maintain 10.00/10 on all new code
- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type annotations where beneficial
- **Docstrings**: Document all public functions and classes

### Django Best Practices
- **Model Design**: Follow Django model best practices
- **Query Optimization**: Use select_related and prefetch_related
- **Security**: Implement proper authentication and authorization
- **Testing**: Write comprehensive unit and integration tests

### Commit Messages
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Maintenance

### Branch Naming
```
feature/description-of-feature
fix/issue-number-description
docs/update-documentation
```

## 🧪 Testing Requirements

### Test Coverage
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test component interactions
- **Model Tests**: Validate data integrity
- **API Tests**: Test endpoints and serialization

### Quality Gates
- ✅ All tests pass
- ✅ Pylint score ≥ 9.5/10
- ✅ No PEP 8 violations
- ✅ Documentation updated
- ✅ Backward compatibility maintained

## 🔒 Security Considerations

- Never commit sensitive data (API keys, passwords, etc.)
- Use Django's security best practices
- Report security issues privately to maintainers
- Implement proper input validation and sanitization

## 📚 Documentation

### Code Documentation
- Use docstrings for all public APIs
- Comment complex business logic
- Maintain up-to-date API documentation

### User Documentation
- Keep README.md current
- Document new features
- Provide usage examples

## 🤝 Code Review Process

### Review Criteria
- **Functionality**: Does it work as intended?
- **Code Quality**: Follows our standards?
- **Testing**: Adequate test coverage?
- **Documentation**: Properly documented?
- **Philosophy**: Aligns with project goals?

### Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests are comprehensive and passing
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Backward compatibility maintained

## 🎉 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md (future)
- Acknowledged in release notes
- Invited to discussions about project direction
- Considered for maintainer roles based on contributions

## 📞 Getting Help

- **Issues**: Use GitHub issues for bugs and features
- **Discussions**: Use GitHub discussions for questions
- **Documentation**: Check existing docs first
- **Maintainer**: Contact @kakch for urgent matters

## 📜 License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

Thank you for contributing to Hume Social and helping build a platform for meaningful intellectual discourse! 🚀