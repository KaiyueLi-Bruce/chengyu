# 🀄 Chengyu CLI

A command-line tool to learn Chinese idioms (成语) with translations powered by DeepL.

Every time you run `chengyu`, you get a random idiom with its pinyin and explanation in your preferred language.

## Installation
```bash
pip install chengyu-cli
```

## Setup

On first run, you will be guided through a quick setup:
```bash
chengyu
```

If you choose any language other than Chinese, you will need a free DeepL API key.
Get one at: https://www.deepl.com/pro-api (choose the Free plan)

## Usage
```bash
chengyu                    # Show next idiom in your default language
chengyu japanese           # Override language for this run only
chengyu --change french    # Change your default language
chengyu --add-key          # Add or update your DeepL API key
chengyu --setup            # Redo the initial setup
chengyu --help             # Show help
```

## Supported Languages

Chinese, English, Japanese, French, German, Spanish, Italian, Korean, Portuguese, Russian, Dutch, Polish

## How It Works

- Idioms are stored locally — no internet needed to fetch them
- Chinese output requires no API key
- All other languages are translated via the DeepL API
- The next idiom is preloaded in the background so display is instant

## Credits

Idiom data sourced from [chinese-xinhua](https://github.com/pwxcoo/chinese-xinhua) (MIT License)

## Auto Publish to PyPI

This project is configured to auto-publish to PyPI via GitHub Actions on tags like `v0.1.1`.

Workflow file: `.github/workflows/publish-pypi.yml`

One-time setup (recommended):
1. In PyPI, open your project settings and add a Trusted Publisher for this GitHub repository.
2. In GitHub, ensure Actions are enabled for this repository.

Release flow:
1. Update version in `pyproject.toml`.
2. Commit and push to `main`.
3. Create and push a matching tag:

```bash
git tag v0.1.1
git push origin v0.1.1
```

The workflow will build and publish automatically. It also checks that the tag version matches `pyproject.toml`.