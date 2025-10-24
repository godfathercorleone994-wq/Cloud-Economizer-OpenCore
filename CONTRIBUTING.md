# Contributing to Cloud Economizer

Thank you for your interest in contributing to Cloud Economizer!

## How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs
- Include detailed steps to reproduce
- Provide system information (OS, Python version, etc.)

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run tests: `pytest tests/`
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and small

### Running Tests

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=cloud_economizer tests/
```

### Adding New Cloud Providers

To add support for a new cloud provider:

1. Create a new analyzer in `cloud_economizer/providers/`
2. Follow the pattern of existing analyzers (AWS, Azure, GCP)
3. Implement the `analyze()` method
4. Return results in the standard format
5. Add tests

### Documentation

- Update README.md for user-facing changes
- Add docstrings for code changes
- Update relevant documentation in `docs/`

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Keep discussions on-topic

## Questions?

Open a GitHub Discussion or reach out to the maintainers.

Thank you for contributing!
