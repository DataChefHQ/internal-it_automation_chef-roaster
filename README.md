# Chef Roaster 😈

Chef Roaster is an AI-powered roasting platform where users can generate witty and hilarious "roasts" for chefs based on their characteristics. This project combines a serverless backend with dynamic AI processing, voice-based interactions, and customizable roast outputs.

## Features

- 🌶 **Funny and personalized Roast**: Generate funny roast for each chef based on their characteristics and data fed to the model.
- 🔥 **Dynamic Roast Image Generation**: Generate roast-themed images for each chef.
- 🌐 **Web Application**: A polished frontend for users to interact with the roasting experience.
- 🔗 **Unique URL for Each Roast**: Easily share your roasts with victims via one-click URL sharing!
- 🎙 **Voice Output Support**: Receive roasts as audio (Text-to-Speech (TTS)).

## Roadmap

### Planned Enhancements
1. **Voice Input Support**:
   - Submit roast descriptions through voice (powered by Speech-to-Text (STT)).
     
2. **Custom Roast Styles**:
   - Choose from snarky, sarcastic, or kind roast templates.

3. **Mobile Compatibility**:
   - Enhance experience for mobile users.

4. **Localization**:
   - Add support for multiple languages.

## Tech Stack

- **Backend**: Python (Flask), AWS Lambda
- **Frontend**: HTML, CSS, JavaScript
- **Serverless Framework**: AWS infrastructure setup and deployment
- **Dependencies**:
  - Flask, Werkzeug, OpenAI API
  - Boto3 for AWS interactions

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js (for serverless integration)
- AWS CLI configured with appropriate permissions

### Running Locally

1. **Setup the environment**:
   ```bash
   pip install poetry
   poetry install
   ```
2. **Start the server**:
   ```bash
   python -m src.main
   ```
3. Open the application in your browser at:
   ```
   http://127.0.0.1:5000/
   ```

## Deployment

The project uses the Serverless Framework for deployment on AWS Lambda.

1. **Install dependencies**:
   ```bash
   npm install
   ```
2. **Deploy to AWS**:
   ```bash
   serverless deploy
   ```

## Project Structure

```
Chef-Roaster/
├── src/
│   ├── main.py                # Flask app and API handlers
│   ├── bedrock.py             # Core AI logic for finding chefs and roasting
│   ├── roasts/                # Roast content files
│   ├── static/                # Frontend assets (CSS, JS, images)
│   ├── templates/             # HTML templates for the web app
├── serverless.yml             # Serverless configuration
├── pyproject.toml             # Python dependencies (Poetry)
├── package.json               # Node.js dependencies
```

## Contributing

1. Fork the repository and create a branch for your feature.
2. Submit a pull request with detailed changes and test cases.

## License

This project is licensed under the MIT License.
