# AI Council CLI

A CLI tool that creates a council of AI models to discuss topics and reach an agreement.

I was trying to create a new feature for my other project, but I think this is also sth cool to test and play with it. I got inspired by Pewdiepies vid and also (im not sure which one) another github repo for ai council. 

Feel free to use it, upgrade it, whatever you want to.

<img width="1050" height="621" alt="image" src="https://github.com/user-attachments/assets/45184122-d5e0-4037-b48d-acea6d5b9dcd" />

## Features

- Multiple AI models discuss a topic in turns
- Models see and respond to each other's messages
- Configurable number of discussion rounds
- Final consensus summary at the end

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install anthropic python-dotenv
   ```
3. Create a `.env` file with your API key:
   ```
   ANTHROPIC_API_KEY=your-api-key-here
   ```

## Usage

```bash
python main.py
```

Enter a topic when prompted and watch the council discuss it.

## Project Structure

```
council-cli/
├── main.py              # Entry point
├── controller.py        # Manages conversation flow
├── models/
│   ├── base_model.py    # Base model class
│   └── anthropic.py     # Anthropic API integration
└── .env                 # API keys (not committed)
```

## Models

Currently configured with:
- **Claude Sonnet 4.5** - Council leader, open to new ideas
- **Claude Haiku 4.5** - Challenger, questions mainstream ideas

- Im going to add OpenAI & some local models to this project.