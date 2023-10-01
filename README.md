# Security Face Recognition Telegram Python Bot

## Introduction
This Python bot is designed to enhance security by using facial recognition technology to identify authorized users and detect banned faces. It integrates with the Telegram messaging platform and offers commands for controlling its functionality.

## Features
- **Facial Recognition:** The bot uses OpenCV and a trained machine learning model to recognize faces.
- **Telegram Integration:** Users can interact with the bot through Telegram using commands.
- **Authorized User:** Only authorized users faces are allowed; others are detected and logged.
- **Logging:** The bot keeps logs of unrecognized or banned face detections.
- **Commands:**
  - `/start`: Start the bot and authenticate as an authorized user.
  - `/help`: Display information about how to use the bot.
  - `/logs`: Retrieve logs of unrecognized or banned face detections.

## Setup
1. **Clone the Repository:** Clone this repository to your local machine.
```bash
git clone https://github.com/your-repo/security-face-bot.git
```
2. **Install Dependencies:** Install the required Python libraries.
3. **Configuration:** Edit the `.env.template` file to specify your Telegram API token and other settings.
4. **Training Data:** Collect authorized and banned face images for training and place them in the appropriate folders.
5. **Run the Bot:** Execute the bot script.
```bash
python main.py
```

## Usage
1. Start the bot by sending `/start` on Telegram.
2. To add authorized user, provide face for training.
3. The bot will continuously monitor the webcam for incoming faces.
4. If an unauthorized or banned face is detected, it logs the event and can send an alert to authorized user.

## Contributing
Contributions are welcome! If you have ideas for improving the bot or adding new features, please open an issue or submit a pull request.

## License
This project is licensed under the [MIT License](https://github.com/Mori0x/telegram-face-system/blob/main/LICENSE).

## Author

- Mori0x

## Disclaimer
This bot is for educational purposes and should not be used for critical security applications. Facial recognition technology may have privacy and ethical implications. Use it responsibly and in accordance with applicable laws and regulations.
