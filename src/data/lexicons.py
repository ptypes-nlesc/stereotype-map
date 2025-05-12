# gendered_nouns

female_nouns = {"woman", "girl", "female", "femme", "babe", "sweetheart", "lady", "girlfriend"} 
female_roles = {"whore", "model", "wife", "housewife", "cleaning lady", "cougar", "milf", "nymph", "schoolgirl", 
                  "secretary", "nurse", "maid", "bride", "porn star", "vixen", "dominatrix", "playgirl", "girl-next-door", 
                  "temptress", "goddess", "siren", "cheerleader", "coed", "damsel", "princess", "barmaid", "dancer", "stripper", 
                  "seductress", "brat", "stepmom", "stepsister", "stepdaughter", "mom", "mommy", "aunt", "granny", "mother-in-law", 
                  "babysitter", "nanny", "camgirl", "escort", "prostitute", "hooker", "starlet", "bride-to-be", "widow", "nympho", 
                  "doll", "barbie", "sugar baby", "mistress", "bimbo", "bitch", "girl scout", "bff", "receptionist", "cowgirl", 
                  "mamasita", "queen", "sugar mama", "sister", "daughter", "school teacher", "teacher", "classmate", "roommate"}
male_nouns = {"man", "boy", "male", "stud", "boyfriend"}
male_roles = {"toyboy", "hunk", "adonis", "alpha", "macho", "daddy", 
                  "boss", "gigolo", "sugardaddy", "trainer", "fireman", "cop", "chief", "soldier", "doctor", "plumber", "handyman", "sugar daddy", 
                  "bad boy", "biker", "bodybuilder", "jock", "athlete", "rebel", "dominant", "master", "king", "seducer", "playboy", "player", 
                  "beast", "cowboy", "knight", "predator", "stepdad", "stepbrother", "husband", "groom", "widower", "client", "pimp", "john", 
                  "nerd", "landlord", "neighbor", "prince", "simp"}
# racialized nouns
racialized_nouns = {"black", "white", "asian", "latina", "latino", "european", "chinese", "japanese", "latin", "african", "middle eastern", "arab", 
                    "mixed-race", "biracial", "ebony", "ivory", "caramel", "oriental", "exotic", "latina bombshell", "ebony queen", "asian doll", 
                    "arab princess", "chocolate stud", "latin lover", "african warrior", "tribe", "oriental beauty", "desert rose", "jungle king", 
                    "eastern goddess", "island girl", "pale beauty", "dark god", "golden boy", "mocha queen", "tiger man", "indian", "pakistani", 
                    "thai", "filipina", "korean","american" "native american", "hispanic", "latinx", "black stud", "white trash", "redneck", "gypsy", 
                    "russian", "eastern european", "brazilian", "afro-latina", "brown sugar", "cherry blossom", "black panther", "safari", "village", "snowbunny"} 

# appearance adjectives
attractiveness_adj = {"beautiful", "cute", "pretty", "sexy", "attractive", "gorgeous", "hot", "exotic", "spicy", "innocent", "delicate", "mature", "erotic", 
                      "bombshell" "elegant", "petite", "curvy", "voluptuous", "huge", "slender", "toned", "muscular", "fit", "slim", "flexible", "athletic", 
                      "trained", "firm-bodied", "tight", "supple", "youthful","fresh-faced", "nubile", "luscious", "blonde", "brunette", "red-haired", "curly", 
                      "dark-skinned", "light-skinned", "pale", "tanned", "glowing", "smooth-skinned", "flawless", "doll-like", "glossy", "hyperfeminine", 
                      "hypermasculine", "rugged", "rough-looking", "rough-edged", "natural", "natural-looking", "artificial-looking", "heavily made-up", 
                      "tattooed", "pierced", "provocative", "pornified", "hypersexualized", "glamorous", "dramatic", "polished", "seductive-looking", 
                      "luscious-lipped", "big-breasted", "firm-breasted", "hourglass-shaped", "wide-hipped", "narrow-waisted", "long-legged", "short-statured", 
                      "broad-shouldered", "chiseled", "sharp-jawed", "scruffy", "hairy", "clean-shaven", "styled", "costumed", "fetishized", "plump", "BBW", 
                      "thick", "stacked", "skinny", "buxom", "ample", "flat-chested", "big-booty", "tattooed all over", "pierced nipples", "pierced clit", 
                      "shaved", "hairy", "natural breasts", "fake breasts", "siliconed", "enhanced", "bleached blonde", "tanned-to-brown", "dark roots", 
                      "freckled", "scarred", "branded", "wet", "monster", "sweaty", "dripping"}
youthfulness_adj = {"teen", "youthful", "doll-like", "fresh-faced"}
body_adj = {"tiny", "tight", "big", "small", "petite", "curvy", "voluptuous", "huge", "slender", "toned", "muscular", "fit", "slim", "big-breasted", 
            "firm-breasted", "hourglass-shaped", "wide-hipped", "narrow-waisted", "long-legged", "thick", "stacked", "skinny", "natural", "artificial", 
            "fake", "silicone", "short-statured", "broad-shouldered", "sharp-jawed", "firm-bodied", "hairy", "clean-shaven", "flat-chested", "shaved"} 
hair_adj = {"blonde", "brunette", "red-haired", "curly", "bleached blonde"} 
ethno_racial_adj = {"exotic", "spicy", "dark-skinned", "light-skinned", "pale", "tanned", "dark roots"}

sex_role_adj: {"innocent", "delicate", "elegant", "glamorous", "seductive", "hyperfeminine", "hypermasculine", "provocative", "pornified", "hypersexualized"} 
action_adj = {"dominant", "submissive", "aggressive", "assertive", "controlling", "demanding", "obedient", "eager", "ready", "teasing", "rough", "violent", 
              "seductive", "naughty", "nasty", "filthy", "passionate", "lustful", "craving", "hungry", "thirsty", "wild", "insatiable", "shameless", 
              "brazen", "playful", "naive", "experienced", "naive", "empowered", "forced", "coerced", "consensual", "fetishized", "taboo-breaking", 
              "voyeuristic", "exhibitionistic", "role-playing", "objectifying", "subservient", "hypermasculine", "hyperfeminine", "overstimulated", 
              "degraded", "hardcore", "kinky", "animalistic", "desperate", "needy", "feral", "sloppy"}

# locations
location_nouns = {"ghetto", "strip club", "brothel", "massage parlor", "massage room", "hotel room", "motel", "airbnb", "locker room", "gym", "shower", 
                  "bathroom", "bedroom", "bed", "kitchen", "kitchen counter", "basement", "rooftop", "office", "boss office", "school classroom", "teacher office",
                "taxi", "limousine", "car backseat", "van", "public toilet", "outside", "public park", "beach", "jacuzzi", "sauna", "spa", "swimming pool", 
                "doctor office", "nurse station", "police station", "prison cell", "couch", "casting couch", "porn studio", "cam studio", "webcam room", 
                "photo studio", "sex shop", "peep show booth", "adult cinema", "adult theater", "fetish dungeon", "sex dungeon", "BDSM club", "stripper stage", 
                "private booth", "mansion bedroom", "cheap motel", "fraternity house", "sorority house", "student dorm room", "college dorm", "train", 
                "public bus", "subway car", "changing room", "glory hole booth", "parking lot", "gas station", "store", "mall", "balcony"} 

# sex action adjectives
sex_action_verb = {"fucked", "penetrated", "double penetrated", "triple penetrated", "boned", "railed", "brainfucked", "dick sucked", "cuckolded", "humiliated", 
                   "worshipping", "disciplining", "punishing", "choking", "spanking", "pegged", "fisted", "restrained", "gagged", "dominated", "forced-to-serve", 
                   "made-to-watch", "shared", "exposed", "outed", "defiled", "ruined", "used", "publicly used", "breedable", "bred", "milked", "impregnated", 
                   "creampied", "stuffed", "pumped", "deepthroated", "face fucked", "anal fucked", "gaped", "stretched", "gangbanged", "bukkaked", "cumslutted", 
                   "pounded", "slapped", "hair pulled", "face slapped", "orgasm", "forced orgasm", "edged", "denied", "forced cum", "overstimulated", "squirted", 
                   "licked", "rimmed", "teabagged", "69ed", "fingered", "handjobbed", "jerked off", "masturbated", "soloed", "voyeurized", "filmed", "recorded", 
                   "live-streamed", "probed", "inserted", "objectified", "bound", "ball gagged", "hogtied", "leashed", "collared", "trained", "bred", "milked", 
                   "marked", "painted", "branded", "tattooed", "pierced", "licked clean", "smeared", "soaked", "pissed on", "spit on", "spitroasted", "licked up", 
                   "licked down", "worn out", "showed", "slided", "received", "bounced", "flashed", "ripped", "swallowed", "exploded"} 

 

 