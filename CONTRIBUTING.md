# Contributing to AI-Ops Workflow Governor

Thanks for your interest in contributing! Here's how to get started.

---

## Ways to Contribute

- Fix a bug
- Add a new pattern detector (e.g. detect high TTFB, poor Core Web Vitals)
- Add support for new rule types (e.g. cache rules, image optimization)
- Improve the log collector to support more pages
- Write more tests
- Improve documentation

---

## Setup

```bash
git clone https://github.com/Niswan028/ai_ops_workflow_governor.git
cd ai_ops_workflow_governor
pip install -r requirements.txt
python -m playwright install chromium
```

---

## Making Changes

1. Fork the repo on GitHub
2. Create a branch for your change:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Run tests to make sure nothing is broken:
   ```bash
   pytest tests/
   ```
5. Commit and push:
   ```bash
   git add .
   git commit -m "describe what you changed"
   git push origin feature/your-feature-name
   ```
6. Open a Pull Request on GitHub

---

## Code Style

- Keep functions small and focused
- Add a test for any new function you write
- No external dependencies unless absolutely necessary

---

## Reporting Bugs

Open an issue on GitHub with:
- What you ran
- What you expected
- What actually happened
