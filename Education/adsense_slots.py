# ==============================================================================
# Google AdSense ad-unit slot IDs.
#
# One entry per RED position in "Advt units.docx". These slots use the FALLBACK
# rule: if a paid institution banner is active for that position it shows; only
# when the slot is empty does the Google ad fill it.
#
# HOW TO FILL THIS IN:
#   1. AdSense dashboard -> Ads -> "By ad unit" tab -> Display ads.
#   2. Create one ad unit per position below (name it to match the key, e.g.
#      "EK - Home R2"). Choose "Responsive".
#   3. AdSense shows a code snippet containing  data-ad-slot="1234567890".
#      Copy ONLY that number.
#   4. Paste it as the value below, e.g.  "homepage_r2": "1234567890",
#
# Leave a value as "" until you have its ID -- an empty slot renders nothing,
# so it is always safe to deploy half-filled.
#
# Publisher is ca-pub-0514207241892727 (baked into templates/base.html loader
# and templates/ads/adsense_unit.html -- do not put it here).
# ==============================================================================

ADSENSE_SLOTS = {
    "homepage_r2":     "6761830954",  # Home page  -> Right Side 2      (was SMU)
    "news_r2":         "7970970845",  # News page  -> Right Side 2      (was Agilo Skill)
    "news_r5":         "1161607223",  # News page  -> Right Side 5      (was Modern International)
    "news_mid1":       "1405562498",  # News page  -> Mid 1            (was Bhardwaj Career Classes)
    "category_r2":     "7535443889",  # News category pages -> Right Side 2   (was Modern International)
    "category_bottom": "9004850911",  # News category pages -> Bottom above footer  (was EK football)
    "jobs_mid1":       "9970035534",  # Jobs (Teaching) -> Mid, after 8 listings
    "search_mid1":     "9966166106",  # Search results  -> Mid, after 10 listings
}
