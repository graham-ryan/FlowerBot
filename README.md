# FlowerBot
A Discord bot to quickly edit pictures by layering emotes on them.

Emotes can be either the default unicode ones, or custom made from Discord servers.

Assets for default emotes comes from [Twemoji](https://github.com/twitter/twemoji) 

Translation / mapping to codepoint comes from UTF-8 [Unicode's Website](https://unicode.org/Public/emoji/13.1/emoji-test.txt)

# Commands
Command prefix is by default '~'

* `border <Num. Emotes> <Emote>...` - In reply to another Discord message with an image embedded, sends an image back with the emotes and number of emotes specified in the command placed along the border

* `emojitoimage <Emote>...` - Given any/all emotes in the command line, sends images of all the emotes back into the text channel

* `gimmethat` - In reply to another Discord message with an image embedded, resends the image into the text channel
