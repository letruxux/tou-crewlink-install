aunlocker_cfg = """
## Settings file was created by plugin AUnlocker v1.1.7-dev+55b5f755f853c1bd319efdae87f00a892c2d9617
## Plugin GUID: AUnlocker

[AccountPatches]

## Remove guest restrictions (no custom name, no freechat, no friendlist)
# Setting type: Boolean
# Default value: false
UnlockGuest = true

## Remove minor status and restrictions (no online play)
# Setting type: Boolean
# Default value: false
UnlockMinor = true

## Remove the penalty after disconnecting from too many lobbies
# Setting type: Boolean
# Default value: true
RemovePenalty = true

[ChatPatches]

## Enable chat-related patches
# Setting type: Boolean
# Default value: true
ChatPatches = true

[CosmeticPatches]

## Unlocks all cosmetics
# Setting type: Boolean
# Default value: true
CosmeticPatches = true

[OtherPatches]

## Enter how many FPS you want
# Setting type: Int32
# Default value: 60
UnlockFPS = 144

## Stop the game from collecting analytics and sending them to Innersloth
# Setting type: Boolean
# Default value: true
NoTelemetry = true

## Add the ability to enable Long Boi Mode (only client-side)
# Setting type: Boolean
# Default value: false
UnlockAprilFoolsMode = false

## Enable Horse Mode (only client-side)
# Setting type: Boolean
# Default value: false
EnableHorseMode = false
""".strip()
