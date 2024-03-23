# Oiml's Smol Bnuy Spawner

This is intended to work with the [EnemySpawner](https://www.nexusmods.com/baldursgate3/mods/8216) mod for BG3.
Configure, then have people write "!Spawn <monster> <now/combat>" in chat to spawn the monster into BG3. Now spawns right now, combat spawns it into the next combat. Will not spawn into an existing combat.

### Disclaimer

This is just intended as a demonstration for now. I am aware that the program is terribly written and has just very basic functionality (e.g. chat is completely unfiltered, meaning it could spawn 15 enemies at once into your game).

Possible improvements:
- More configuration options, especially for filtering and chat commands
- Properly redo the Twitch authentication (so you can use channel subscriptions, donations, bits or even channel point redemptions)
- clean up code in general (duh)

### Configuration

The following configuration variables can be set in the `config.ini` file:

| Variable | Type | Default | Description |
|--|--|--|--|
| `[FILES]` | | |
| inputfilepath | Path | | Path to the `monster db.ini` |
| outputfilepath | Path | | Path to the `SpawnEnemy.txt`.  Usually found in `AppData/Local/Larian Studios/Baldur's Gate 3/Script Extender/` |
| `[TWITCH]` | | |
| twitch_server | String | irc.chat.twitch.tv | Twitch chat server to connect to. |
| twitch_port | int | 6667 | Port for the Twitch chat server. |
| twitch_nickname | String |  | Your Twitch name. |
| twitch_token | String |  | OAuth token. There are various websites to generate one. |
| twitch_channel | #String |  | The Twitch stream you want to follow and read chat from. |
|--|--|--|

The following configuration is required in the `monster db.ini` file:

Add new enemies in the following format:
`monster name`,`UUID`

| Variable | Description |
|--|--|
| Monster Name | Name displayed in the Tool and the name used to spawn the monster |
| UUID | Unique ID for the monster. Can be found with e.g. BG3 Modders Multitool |