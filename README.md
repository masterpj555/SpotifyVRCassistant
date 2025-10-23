# SpotifyVRCassistant
My first repo so excuse me for any publication, formatting issues.


Matches spotify tracks with youtube links.

This program is mostly aimed at VRChat where sharing music in the world has to happen through youtube.

This program takes the track and artist name of spotify and tries to match it with youtube search result, giving you a youtube link of the first matching result.

Features:
- Settings → Spotify API Credentials… (saved locally)
- Settings → Auto Clipboard Mode (watches clipboard for Spotify track URLs; auto-fetch + auto-copy)
- Auto-fetch on paste/typing (debounced) and on Enter
- About menu with creator info and clickable links (dialog centered; aligned rows)
- Compact dark UI + dark title bars on Windows (DWM)

How to use:

1. Download the Exe: SpotifyToYouTube.exe (found in the releases section)
   
   Go to: https://developer.spotify.com/dashboard/


3. Log in with your existing spotify account


4. Press "Create App"


6. Add a random App name
   
   Add a random description
   
   Add a random redirect url (I used: https://www.google.com) It is important your url is https.
   
   Agree to the terms and save


7. Go to the app in the dashboard and copy the Client ID and paste it into the program
   
   Click "View client Secret"
   
   Copy the client secret
   
   Paste the client secret into the program.


9. You are now ready to use the program.
    
   Auto clipboard is suggested when using it for VR/VRchat


# Do not share your API key with anyone else. Transferring the exe to someone else does not expose your API keys
