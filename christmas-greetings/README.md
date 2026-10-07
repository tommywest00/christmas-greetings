# Christmas Greetings landing page kit

## Folder layout
- template.html: the page design. Edit once; every prospect page uses it.
- program.json: packages, prices, dates, fine print, default script, and your contact info. Update this each year.
- prospects.csv: one row per business.
- prospects/<folder>/: one folder per business holding logo.png (or .jpg/.svg) and greeting.mp3.
- assets/: optional station logos (classic-rock.png, myfm.png, wow-fm.png, northumberland-daily.png). Names show as text if these are missing.
- output/: finished pages, plus report.txt listing anything missing.

## prospects.csv columns
- folder: must match the folder name under prospects/
- business_name, location (address and town, used in the script)
- contact_first_name: used in the headline, "Thank Northumberland for a great year, Dave."
- digital_headline: optional. Leave blank to rotate Happy Holidays / Seasons Greetings / Merry Christmas / Warmest Wishes / Peace On Earth
- custom_script: optional. Use {CLIENT} and {LOCATION}. Blank uses the default script.
- rep_name, rep_email, rep_phone: optional per-row override of the default rep.
- default_station: cr, myfm, or wow. Pre-selects the prospect's station and the listener number under the play button.

## Building the pages
Run: python3 generate.py

Or paste this prompt into Claude Cowork or Claude Code with this folder open:

    Open my christmas-greetings folder. Check prospects.csv against the
    folders in prospects/ and tell me about any mismatches. Then run
    generate.py and show me report.txt.

## Writing spec scripts before recording
Paste this into Claude with prospects.csv attached:

    For each business in this CSV, write a 15-second radio Christmas greeting
    (about 35 words) that includes only the business name and address, warm
    and community-focused, no prices or offers. Return the CSV with the
    custom_script column filled in.

## Hosting
Each output/<folder>/index.html is one self-contained file (logo and audio embedded).
Upload each folder to Netlify Drop, GitHub Pages, or a hidden section of your station site,
then email the prospect their link.

## Proof, deadline, and packages
All in program.json: `proof` (participant count, business names, and the "thousands of local listeners/readers" lines), `deadline` (the page counts down to it and switches to "call me for current rates" after), and `radio.packages` (the three package cards; `best_value` sets the badge and the default) and `digital.packages` (the add-on box, first option pre-selected). Use real numbers only.

## Pricing logic in the order builder
The radio package price is per station. Choosing all 3 stations charges the third at half price
(e.g. 8 days on all 3 = $469 + $469 + $234.50). Digital is a flat price regardless of how many
websites are chosen. Change the discount in program.json if your rules differ.
