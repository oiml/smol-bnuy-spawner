# Oiml's Smol Bnuy Spawner

This is intended to work with the [EnemySpawner](LINK REQUIRED)" mod for BG3.
Configure, then have people write "!Spawn <monster> <now/later>" in chat to spawn the monster into BG3.

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