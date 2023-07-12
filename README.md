This bot will ping a role or user on a previous specified channel if all the positive keywords are found on the embed contents and no negative keywords are found following a **case insensitive** algorithm.

# Installation
- Make sure to have all indent privileges enabled for your bot.
- Give the bot admin or high permissions on your server so it can tag any role, read messages and see all channels.
- Move the bot role above any roles you or your users might want to tag.
- You must fill the constants.py file with appropriate values before running the bot.

# Instructions
You can add and delete as many pings as you want. All the added pings will be saved into a .json file so you can stop or reboot the bot at any time without losing the already added pings.

To add more than one positive or negative keywords split them using a comma.

Negative keywords are always optional.
## Role ping
A role it's a ping which is linked to a role, and not to a specific user, to set this kind of ping, you **must** fill the `target_role` camp with the role you want to tag.

*This ping can only by added by server administrators*
## User ping
A user it's a ping which is linked to a user, and not to a role, to set this kind of ping, you **must not** fill the `target_role` camp, this will link the ping to the user setting the ping.

*This ping can by added by both server administrators and users*
