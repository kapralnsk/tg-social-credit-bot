# Telegram Social Credit Bot

Bot for group chats, which keeps track of user's Social Credit score. Social Credit is manipulated by other users in chat via replies to messages, using PoohSoicalCredit stickers https://t.me/addstickers/PoohSocialCredit

## System dependencies

This project relies on `MongoDB` > 4.0. 

## Commands

* `/social_credit_enable` - enables Social Credit system bot for group chat. Can only be done by Chat Admin
* `/social_credit_enroll` - enrolls chat member to Social Credit system
* `/social_credit_myscore` - shows your current Social Credit score
* `/social_credit_chatinfo` - displays everyone enrolled in Social Credit system and their current score
* `/social_credit_help` - displays help message

## Localization

This project uses *nix `gettext` library to localise all bot messages. 
In the future, all chats can choose their language upon enabling the bot.
Localisations files are expected in `locale` directory in project root. 
Using `translation_template.po` file in repo root, you can create your own translations.
See `gettext` library documentation for more details on working with this format.

## Docker

Image is provided [here](https://hub.docker.com/repository/docker/kapral/tg-scoial-credit-bot).