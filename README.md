# SpotifyVRCassistant
Matches spotify tracks with youtube links.

My first repo so excuse me for the issues

This program is mostly aimed at VRChat where sharing music in the world has to happen through youtube
This program takes the track and artist name of spotify and tries to match it with youtube search result, giving you a youtube link of the first matching result.

Features:
- Settings → Spotify API Credentials… (saved locally)
- Settings → Auto Clipboard Mode (watches clipboard for Spotify track URLs; auto-fetch + auto-copy)
- Auto-fetch on paste/typing (debounced) and on Enter
- About menu with creator info and clickable links (dialog centered; aligned rows)
- Compact dark UI + dark title bars on Windows (DWM)

How to use:

.

Go to:
https://developer.spotify.com/dashboard/


2. 

Log in with your existing spotify account


3. 

Press "Create App"

4.

Add a random App name
Add a random description
Add a random redirect url (I used: https://www.google.com) It is important your url is https.

Agree to the terms and save

5. 

Go to the app in the dashboard and copy the Client ID and paste it into the program

Click "View client Secret"

Copy the client secret
Paste the client secret into the program.

6.

You are now ready to use the program.
Auto clipboard is suggested when using it for VR/VRchat
