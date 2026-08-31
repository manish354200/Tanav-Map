# Contributing Guidelines

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Write tests for your changes
5. Commit with clear messages: `git commit -m "Add feature: description"`
6. Push to the branch: `git push origin feature/your-feature`
7. Submit a Pull Request

## Code Standards

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints for functions
- Write docstrings for all functions and classes
- Minimum 80% test coverage

```bash
# Format code
black app/

# Lint
flake8 app/

# Type check
mypy app/
```

### JavaScript/React (Frontend)
- Use ESLint configuration
- Write clear component documentation
- Use TypeScript where possible
- Follow React best practices

```bash
npm run lint
npm run format
npm test
```

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat:` A new feature
- `fix:` A bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Example:
```
feat(distress-score): add exponential weighting for recent data

- Implemented exponential decay function
- Added configuration for decay rate
- Updated tests for new calculation

Closes #123
```

## Testing

### Backend
```bash
cd backend
pytest tests/
pytest tests/test_file.py::test_function -v
pytest --cov=app tests/
```

### Frontend
```bash
cd frontend
npm test
npm test -- --coverage
```

## Documentation

- Update README.md for major changes
- Add docstrings to new functions
- Update API documentation for new endpoints
- Include examples in comments

## Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. Add/update tests for new functionality
4. Request review from maintainers
5. Address review comments
6. Maintain a clean commit history

## Reporting Issues

- Check existing issues before creating new ones
- Provide clear description of the problem
- Include steps to reproduce
- Add relevant logs and screenshots
- Mention your environment (OS, Python/Node version, etc.)

## Code Review

- Be respectful and constructive
- Ask questions rather than make demands
- Suggest improvements, not criticisms
- Test changes locally before approving
- Ensure adherence to project standards
