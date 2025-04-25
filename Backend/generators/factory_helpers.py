





import random

import urllib


def construct_dicebear_api_url(self, style, seed=None):
    """Construct the API URL for generating a photo."""
        # Schema-based enum options
        
    if style == "notionists-neutral":
        glasses_options = [f"variant{str(i).zfill(2)}" for i in range(1, 12)]
        eyes_options = [f"variant{str(i).zfill(2)}" for i in range(1, 6)]
        lips_options = [f"variant{str(i).zfill(2)}" for i in range(1, 31)]
        nose_options = [f"variant{str(i).zfill(2)}" for i in range(1, 21)]
        bg_colors = ["b6e3f4", "ffd5dc", "d1d4f9", "fff5b7", "c0aede", "ffffff"]

        # Random selection (1 value per trait)
        params = {
            "glasses": random.choice(glasses_options),
            "eyes": random.choice(eyes_options),
            "lips": random.choice(lips_options),
            "nose": random.choice(nose_options),
            "backgroundColor": random.choice(bg_colors)
        }
    elif style == "lorelei-neutral":
        variant = lambda prefix, count: [f"{prefix}{str(i).zfill(2)}" for i in range(1, count + 1)]

        params = {
            "backgroundColor": random.choice(["ffffff", "b6e3f4", "ffd5dc", "d1d4f9", "fff5b7", "c0aede"]),
            "eyebrows": random.choice(variant("variant", 13)),
            "eyes": random.choice(variant("variant", 24)),
            "eyesColor": random.choice(["000000", "4a4a4a", "7f8c8d"]),
            "glasses": random.choice(variant("variant", 5)),
            "glassesColor": random.choice(["000000", "4a4a4a", "ffffff"]),
            "mouth": random.choice([
                "happy01", "happy02", "happy03", "happy04", "happy05", "happy06", "happy07",
                "happy08", "happy09", "happy10", "happy11", "happy12", "happy13", "happy14",
                "happy15", "happy16", "happy17", "happy18", "sad01", "sad02", "sad03", "sad04",
                "sad05", "sad06", "sad07", "sad08", "sad09"
            ]),
            "nose": random.choice(variant("variant", 6)),
        }
    elif style == "avataaars-neutral": 
        params = {
            "backgroundColor": random.choice(["614335", "d08b5b", "ae5d29", "edb98a", "ffdbb4", "fd9841", "f8d25c"]),
            "backgroundType": random.choice(["solid", "gradientLinear"]),
            "eyebrows": random.choice([
                "angryNatural", "defaultNatural", "flatNatural", "frownNatural",
                "raisedExcitedNatural", "sadConcernedNatural", "unibrowNatural", "upDownNatural",
                "angry", "default", "raisedExcited", "sadConcerned", "upDown"
            ]),
            "eyes": random.choice([
                "closed", "cry", "default", "eyeRoll", "happy", "hearts", "side",
                "squint", "surprised", "winkWacky", "wink", "xDizzy"
            ]),
            "mouth": random.choice([
                "concerned", "default", "disbelief", "eating", "grimace", "sad",
                "screamOpen", "serious", "smile", "tongue", "twinkle", "vomit"
            ]),
            "nose": "default"
        }
        
    else:
        # Default options for other styles
        params = {
            "seed": seed,
            "size": 512,
            "backgroundColor": "ffffff",
            "style": style
        }
        style = "lorelei-neutral" 
        
    dice_bear_api = "https://api.dicebear.com/9.x/"
    query = urllib.parse.urlencode(params)
    url = f"{dice_bear_api}{style}/svg?{query}"
    return url