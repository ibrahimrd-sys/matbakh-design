# assets

Drop the photos, clips and `media.js` here, keeping the filenames the
prototypes expect. `python3 build.py` lists any that are missing.

Expected right now:

    broth.jpg  chicken-seared.jpg  garlic-butter-pan.jpg  lemons.jpg
    molokhia-dish.jpg  onion-chopped.jpg  clip-knife.webm  media.js

`media.js` defines `window.MB_MEDIA`, a map from these paths to embedded data
URIs. When it is present the images load from the map; when it is absent the
prototypes fall back to loading the files from this folder. Both work — which
means a reviewer with a slow connection and a reviewer opening a single saved
file both see the same screens.

All current files are Wikimedia Commons placeholders. Record each one in
`ATTRIBUTIONS.md` before the repository goes public.
