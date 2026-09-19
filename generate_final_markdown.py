import re
import subprocess
import os

with open('ikkyu_and_the_crazy_cloud_anthology_a_zen_poet_of_medieval_translation.raw.md', 'r', encoding='utf-8') as f:
    pages = f.read().split('\x0c')

# 1. Comprehensive Typo and OCR normalization dictionary
TYPO_FIXES = [
    (r'\bTIkkyu\b', 'Ikkyū'),
    (r'\b1kkya\b', 'Ikkyū'),
    (r'\bIkkyws\b', "Ikkyū's"),
    (r'\bIkkya\b', 'Ikkyū'),
    (r'\bIkkyt\b', 'Ikkyū'),
    (r'\bIkkyti\b', 'Ikkyū'),
    (r'\bIkkyn\b', 'Ikkyū'),
    (r'\bIkkyd\b', 'Ikkyū'),
    (r'\bIkkyii\b', 'Ikkyū'),
    (r'\bIkky@\b', 'Ikkyū'),
    (r'\bSdjun\b', 'Sōjun'),
    (r'\bS6jun\b', 'Sōjun'),
    (r'\bKyounshii\b', 'Kyōunshū'),
    (r'\bKydunshii\b', 'Kyōunshū'),
    (r'\bKyounsha\b', 'Kyōunshū'),
    (r'\bKyounshn\b', 'Kyōunshū'),
    (r'\bKyounshi\b', 'Kyōunshū'),
    (r'\bkQan\b', 'kōan'),
    (r'\bkGan\b', 'kōan'),
    (r'\bk6an\b', 'kōan'),
    (r'\bkdan\b', 'kōan'),
    (r'\bKean\b', 'Kōan'),
    (r'\bY6so\b', 'Yōsō'),
    (r'\bYos6\b', 'Yōsō'),
    (r'\bY6sd\b', 'Yōsō'),
    (r'\bY6s6\b', 'Yōsō'),
    (r'\bYoQsos\b', "Yōsō's"),
    (r'\bYoQso\b', 'Yōsō'),
    (r'\bDaitd\b', 'Daitō'),
    (r'\bKasd\b', 'Kasō'),
    (r'\bKas6\b', 'Kasō'),
    (r'\bGoj6\b', 'Gojō'),
    (r'\bGojd\b', 'Gojō'),
    (r'\bSoj687\b', 'Sōjō [87]'),
    (r'\bSeizan88\b', 'Seizan [88]'),
    (r'\bShiichi Kato\b', 'Shūichi Katō'),
    (r'\bKato Shiichi\b', 'Shūichi Katō'),
    (r'fryu、', 'fūryū, '),
    (r'Faryu、', 'Fūryū, '),
    (r'\bfnryu\b', 'fūryū'),
    (r'\bfiryii\b', 'fūryū'),
    (r'\bfrya\b', 'fūryū'),
    (r'\bfiryu\b', 'fūryū'),
    (r'\bfuryi\b', 'fūryū'),
    (r'\bboftheFounder\'s\b', "of the Founder's"),
    (r'\bofthe\b', 'of the'),
    (r'\bpurein\b', 'pure in'),
    (r'\batjust\b', 'at just'),
    (r'\bconcerns\.of\b', 'concerns of'),
    (r'\bthe\.Zen\b', 'the Zen'),
    (r'\bso\.often\b', 'so often'),
    (r'\btrans\.by\b', 'trans. by'),
    (r'\baMaster\b', 'a Master'),
    (r'\bsMonk\b', "'s Monk"),
    (r'\bcupofcitrus\b', 'cup of citrus'),
    (r'\btrahslations\b', 'translations'),
    (r'\bconcerete\b', 'concrete'),
    (r'\bdrunknneess\b', 'drunkenness'),
    (r'\befHorescence\b', 'efflorescence'),
    (r'\bimpoverishcd\.4\b', 'impoverished [4]'),
    (r'\bsufh-\s*cient\b', 'sufficient'),
    (r'\bSelfAppraisal\b', 'Self-Appraisal'),
    (r'\bSelf-A ppraisal\b', 'Self-Appraisal'),
    (r'\bCl’w’s\b', "Ch’u’s"),
    (r'Praising Saint\s+日\s*Onen', 'Praising Saint Hōnen'),
    (r'“Li Chien’s House「:', '“Li Chien’s House”:'),
    (r'Periors、\s*a\s+term', 'superiors, a term'),
    (r'In “The Waste Land、\s*use', 'In "The Waste Land," use'),
    (r'existance', 'existence'),
    (r'senient', 'sentient'),
    (r'ephithet', 'epithet'),
    (r'frequently occuring', 'frequently occurring'),
]

def apply_typos(text):
    for pat, rep in TYPO_FIXES:
        text = re.sub(pat, rep, text)
    return text

def dehyphenate(text):
    def replace_hyphen(m):
        w1, w2 = m.group(1), m.group(2)
        if w1.lower() in ('non', 'self', 'well', 'all', 'cross'):
            return f'{w1}-{w2}'
        return f'{w1}{w2}'
    return re.sub(r'([a-zA-Z]+)-\n\s*([a-zA-Z]+)', replace_hyphen, text)

def strip_page_footer(page_text):
    pat = r'\n\s*\S+\s+(?:FOREWORD|PREFACE|INTRODUCTION|POEM\s+NUMBER\s+\d+|I?NOTES\s+TO\s+PAGES.*|BIBLIOGRAPHY|INDEX\s+TO\s+POEMS|GLOSSARY-INDEX|ABBREVIATIONS)\s*$'
    return re.sub(pat, '', page_text.rstrip(), flags=re.IGNORECASE)

cjk_pat = re.compile(r'[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff\uff00-\uffef]')

def clean_translation_line(line):
    if len(line) - len(line.lstrip()) >= 45:
        return ''
    m_cjk = cjk_pat.search(line)
    if m_cjk:
        cjk_pos = m_cjk.start()
        if 'Praising Saint' in line and cjk_pos < 40:
            pass
        elif cjk_pos >= 35:
            return line[:cjk_pos].rstrip()
    for m in re.finditer(r'\s{4,}\S', line):
        col = m.end() - 1
        if col >= 45:
            return line[:m.start()].rstrip()
    return line.rstrip()

def parse_prose(text):
    lines = text.splitlines()
    paragraphs = []
    curr_para = []
    for l in lines:
        s = l.strip()
        if not s:
            if curr_para:
                paragraphs.append(' '.join(curr_para))
                curr_para = []
            continue
        indent = len(l) - len(l.lstrip())
        if indent >= 2 and curr_para:
            prev = curr_para[-1]
            if prev.endswith(('.', '!', '?', '”', '"', ':', '’', "'", ';', '—')):
                paragraphs.append(' '.join(curr_para))
                curr_para = []
        curr_para.append(s)
    if curr_para:
        paragraphs.append(' '.join(curr_para))
    cleaned = []
    for p in paragraphs:
        p_clean = re.sub(r'\s+', ' ', p).strip()
        if p_clean:
            cleaned.append(apply_typos(p_clean))
    return cleaned

print("Preprocessing modules ready.")

# 2. Section Builders

def build_frontmatter():
    lines = [
        "# Ikkyū and the Crazy Cloud Anthology: A Zen Poet of Medieval Japan",
        "",
        "**Translation with an Introduction by Sonja Arntzen**  ",
        "**Foreword by Shūichi Katō**  ",
        "University of Tokyo Press",
        "",
        "## Plates",
        "",
        "### Plate 1: Calligraphy: \"Do No Evil, Do Much Good\"",
        "",
        "![Plate 1: Calligraphy: \"Do No Evil, Do Much Good\"](images/plate_1_calligraphy.png)",
        "",
        "\"Do no evil, do much good,\" a maxim made famous by the dialogue between Niao K’o and Po Chü-i. See pages 35–36. Calligraphy in Ikkyū’s hand. Courtesy of Shinjuan, Daitokuji, Kyoto.",
        "",
        "### Plate 2: Portrait of Ikkyū by Bokusai",
        "",
        "![Plate 2: Portrait of Ikkyū by Bokusai](images/plate_2_portrait_bokusai.png)",
        "",
        "Portrait of Ikkyū by Bokusai. The poem, in Ikkyū’s hand, accompanying the portrait is \"Self-Appraisal\" (poem no. 130). Courtesy of Tokyo National Museum.",
        "",
        "### Plate 3: Ikkyū's Death Poem",
        "",
        "![Plate 3: Ikkyū's Death Poem](images/plate_3_death_poem.png)",
        "",
        "Ikkyū’s death poem, in his own hand. The poem is translated on page 32. Courtesy of Shinjuan, Daitokuji, Kyoto.",
        "",
        "### Plate 4: Portrait of Ikkyū and Lady Mori with Poems",
        "",
        "![Plate 4: Portrait of Ikkyū and Lady Mori with Poems](images/plate_4_ikkyu_and_mori.png)",
        "",
        "Portrait of Ikkyū and Mori with a Chinese poem in Ikkyū’s hand at the top of the painting, and a Japanese poem presumably in Mori’s hand in the lower half of the scroll. Courtesy of Masaki Museum, Osaka.",
        "",
        "*Ikkyū’s poem:*",
        "",
        "Within the circle, appears a whole self;  ",
        "This painting expresses the true features of Hsü-t’ang.  ",
        "The blind girl’s love song laughs at the pavilion girls,  ",
        "One song before the blossoms is ten thousand years of spring.",
        "",
        "*Mori’s poem:*",
        "",
        "Sleep of yearning,  ",
        "Sleep of sorrow, in bed,  ",
        "Floating and sinking,  ",
        "But for tears,  ",
        "There is no consolation.",
        "",
        "---",
        "",
        "### UNESCO Collection of Representative Works: Japanese Series",
        "",
        "This book has been accepted in the Japanese Series of the Translation Collection of the United Nations Educational, Scientific and Cultural Organization (UNESCO).",
        "",
        "---",
        "",
        "### Epigraph",
        "",
        "> \"To speak of Ikkyū is really to speak of oneself. ... This man will now continue for some time to summon up a new concern among various people. We forget he was a Zen monk. It is a strange and marvelous thing that everyone has the sense of secretly having met him somewhere before. Is he not perhaps the only one of a kind in the history of Buddhism through India, China, and Japan?\"  ",
        "> — **Yanagida Seizan**",
        "",
        "---",
        "",
        "## Contents",
        "",
        "- [Plates](#plates)",
        "- [Foreword by Shūichi Katō](#foreword-by-shūichi-katō)",
        "- [Preface](#preface)",
        "- [Introduction](#introduction)",
        "  - [Ikkyū (1394–1481): The Man and His Times](#ikkyū-13941481-the-man-and-his-times)",
        "  - [Dialectic of Non-Duality](#dialectic-of-non-duality)",
        "  - [Allusion](#allusion)",
        "  - [A Note on the Text and Its Organization](#a-note-on-the-text-and-its-organization)",
        "- [Translations from the Crazy Cloud Anthology](#translations-from-the-crazy-cloud-anthology)",
        "- [Abbreviations](#abbreviations)",
        "- [Notes](#notes)",
        "  - [Notes to Introduction](#notes-to-introduction)",
        "  - [Notes to Translations](#notes-to-translations)",
        "- [Bibliography](#bibliography)",
        "  - [Primary Sources](#primary-sources)",
        "  - [Secondary Sources](#secondary-sources)",
        "- [Index of Poems](#index-of-poems)",
        "- [Glossary-Index](#glossary-index)",
        "",
        "---",
        ""
    ]
    return '\n'.join(lines)

def build_foreword():
    raw = '\n'.join([strip_page_footer(pages[i]) for i in range(16, 20)])
    paras = parse_prose(dehyphenate(raw))
    # Filter out heading "Foreword" if present as first element
    if paras and paras[0].lower() == 'foreword':
        paras = paras[1:]
    out = ["## Foreword by Shūichi Katō", ""]
    for p in paras:
        out.append(p)
        out.append("")
    return '\n'.join(out)

def build_preface():
    raw = '\n'.join([strip_page_footer(pages[i]) for i in range(20, 23)])
    paras = parse_prose(dehyphenate(raw))
    if paras and paras[0].lower() == 'preface':
        paras = paras[1:]
    out = ["## Preface", ""]
    for p in paras:
        out.append(p)
        out.append("")
    return '\n'.join(out)

def build_introduction():
    # Section 1: p26 to p58 line 24
    p26_to_57 = '\n'.join([strip_page_footer(pages[i]) for i in range(26, 58)])
    p58_lines = pages[58].splitlines()
    dial_idx = -1
    for i, l in enumerate(p58_lines):
        if 'Dialectic' in l:
            dial_idx = i
            break
    sec1_raw = p26_to_57 + '\n' + '\n'.join(p58_lines[:dial_idx])
    sec1_paras = parse_prose(dehyphenate(sec1_raw))
    if sec1_paras and 'The Man and His Times' in sec1_paras[0]:
        sec1_paras = sec1_paras[1:]

    # Section 2: p58 dial_idx to p62 allusion
    p58_to_62_lines = p58_lines[dial_idx:]
    for idx in range(59, 62):
        p58_to_62_lines.extend(strip_page_footer(pages[idx]).splitlines())
    p62_lines = strip_page_footer(pages[62]).splitlines()
    allusion_idx = -1
    for i, l in enumerate(p62_lines):
        if l.strip() == 'Allusion':
            allusion_idx = i
            break
    p58_to_62_lines.extend(p62_lines[:allusion_idx])
    sec2_raw = '\n'.join(p58_to_62_lines)
    sec2_paras = parse_prose(dehyphenate(sec2_raw))
    if sec2_paras and 'Dialectic of' in sec2_paras[0]:
        sec2_paras = sec2_paras[1:]

    # Section 3: p62 allusion to p82 note
    p62_to_82_lines = p62_lines[allusion_idx:]
    for idx in range(63, 82):
        p62_to_82_lines.extend(strip_page_footer(pages[idx]).splitlines())
    p82_lines = strip_page_footer(pages[82]).splitlines()
    note_idx = -1
    for i, l in enumerate(p82_lines):
        if 'A Note on the Text' in l:
            note_idx = i
            break
    p62_to_82_lines.extend(p82_lines[:note_idx])
    sec3_raw = '\n'.join(p62_to_82_lines)
    sec3_paras = parse_prose(dehyphenate(sec3_raw))
    if sec3_paras and sec3_paras[0].strip() == 'Allusion':
        sec3_paras = sec3_paras[1:]

    # Section 4: p82 note to p84
    p82_to_84_lines = p82_lines[note_idx:]
    for idx in [83, 84]:
        p82_to_84_lines.extend(strip_page_footer(pages[idx]).splitlines())
    sec4_raw = '\n'.join(p82_to_84_lines)
    sec4_paras = parse_prose(dehyphenate(sec4_raw))
    if sec4_paras and 'A Note on the Text' in sec4_paras[0]:
        sec4_paras = sec4_paras[1:]

    out = ["## Introduction", ""]
    out.append("### Ikkyū (1394–1481): The Man and His Times\n")
    for p in sec1_paras:
        out.append(p + "\n")
    out.append("### Dialectic of Non-Duality\n")
    for p in sec2_paras:
        out.append(p + "\n")
    out.append("### Allusion\n")
    for p in sec3_paras:
        out.append(p + "\n")
    out.append("### A Note on the Text and Its Organization\n")
    for p in sec4_paras:
        out.append(p + "\n")
    return '\n'.join(out)

print("Front matter and Introduction builders defined.")

# Complete POEM_TITLES dictionary
POEM_TITLES = {
    '6': 'Face to Face with the Beautiful One on the Eve of Daitō’s Commemoration Ceremony',
    '7': 'Praising Monk Hsü-t’ang',
    '8': 'On the Topic of The Venerable Master Daitō’s Conduct',
    '17': 'Straw-Sandal Ch’en',
    '25': 'One’s Eyes Are Not Yet Clear; How Is It That You Make Trousers to Wear Out of Empty Air?',
    '26': 'Draw a Line on the Earth, Make a Cage; How Is It That You Penetrate But Do Not Pass Through?',
    '27': 'Go to the Sea and Count the Sands; How Do You Stand Tiptoe on the Point of a Needle?',
    '33': 'A Cup of Rice in a Broken-Footed Cauldron',
    '35': 'Peach Blossom Waves',
    '37': 'Addressed to an Assembly on the Winter Solstice',
    '40': 'The Buddha’s Nirvana',
    '44': 'Two Pieces of Skin and One Set of Bone',
    '46': 'Pleasure in Pain',
    '47': 'Pain in Pleasure',
    '52': 'Tortoise Around Ta-sui’s Hermitage',
    '54': 'Rinzai Burned the Meditation Plank and Desk',
    '66': 'The Great Master Yüan-wu Strikes a Harmony with the Cosmic Organ',
    '68': 'Praising the Fish-Basket Kannon',
    '69': 'The Scriptures Wipe Away Filth (I)',
    '70': 'The Scriptures Wipe Away Filth (II)',
    '71': 'The Scriptures Wipe Away Filth (III)',
    '74': 'Frogs',
    '75': 'Shakuhachi',
    '78': 'Chrysanthemums: An Arhat and Yang Kuei-fei in the Same Vase',
    '79': 'Snowball',
    '89': 'Living in the Mountains (I)',
    '90': 'Living in the Mountains (II)',
    '91': 'Instructing the Cook in the Mountains',
    '93': 'From the Mountains, Returning to the City',
    '94': 'Old Woman Kōan',
    '101': 'Troubles at Daitokuji (I)',
    '108': 'Troubles at Daitokuji (II)',
    '110': 'Wind Bell',
    '115': 'Earth House',
    '117': 'Straw Raincoat and Hat',
    '120': 'Congratulations for Yōsō (I)',
    '121': 'Congratulations for Yōsō (II)',
    '126': 'Praising P’u-hua',
    '128': 'Under One’s Feet, the Red Thread',
    '130': 'Self-Appraisal',
    '134': 'Three Poems to Show the Assembly (I)',
    '135': 'Three Poems to Show the Assembly (II)',
    '136': 'Three Poems to Show the Assembly (III)',
    '140': 'On Tiger Mount, the Snow Falls on Three Grades of Monks (I)',
    '141': 'On Tiger Mount, the Snow Falls on Three Grades of Monks (II)',
    '144': 'On a Brothel',
    '145': 'Addressed to a Monk in the Hall of Long Life',
    '153': 'Sakyamuni Practicing Ascetic Discipline',
    '156': 'Self-Appraisal',
    '166': 'Praising the Dharma Master Tz’u-en K’uei-chi',
    '175': 'Congratulating Daiyūan’s Monk Yōsō upon Receiving the Honorary Title Zen Master Sōe Daishō',
    '176': 'Addressed to a Monk at Daitokuji',
    '179': 'Inscription for Yōsō’s Hermitage',
    '180': 'Pai-chang Fasting',
    '184': 'Presented to a Gathering',
    '187': 'Master Sung-yüan Rose to Lecture and Presented This Case',
    '188': 'Nirvana Hall',
    '209': 'Three Reflections of Master Fo-yen',
    '210': 'Composing a Poem and Trading It for Food',
    '216': 'Fisherman',
    '223': 'Addressed to a Monk Who Killed a Cat',
    '234': 'About Disturbances at Daitokuji',
    '240': 'Congratulating Elder Ki on the New Construction of Eagle Tail Monastery and Inquiring after His Leprosy (I)',
    '244': 'Congratulating Elder Ki on the New Construction of Eagle Tail Monastery and Inquiring after His Leprosy (II)',
    '249': 'Thanking a Man for the Gift of Soy Sauce',
    '251': 'Composed When Ill',
    '254': 'Picture of an Arhat Reveling in a Brothel (I)',
    '255': 'Picture of an Arhat Reveling in a Brothel (II)',
    '264': 'A Layman Reciting a Poem Before the Gate of a Brothel and Then Returning',
    '280': 'Remorse over Sins for Which My Tongue Should Be Pulled Out',
    '284': 'With a Poem About a Brothel, Putting to Shame Those Brothers Who Obtain the Dharma',
    '287': 'Acts of Grace',
    '291': 'The Correct Skill for Great Peace',
    '292': 'The Correct Skill for a Disorderly Age',
    '293': 'Reducing Desires and Knowing Contentment',
    '308': 'No One Sees It the Same',
    '344': 'Untitled [Two pieces of skin and one set of bone]',
    '352': 'Taking a Metaphor for Reality',
    '362': 'Praising Saint Hōnen',
    '367': 'Ridiculing Literature',
    '376': 'Quietly Singing Beside the Lamp',
    '381': 'Recollecting the Past',
    '383': 'The Stick',
    '384': 'Untitled [Utterly absorbed in the dream of Wu-shan]',
    '385': 'Deluded Enlightenment',
    '388': 'Addressed to a Monk Who Burned Books (I)',
    '389': 'Addressed to a Monk Who Burned Books (II)',
    '390': 'Addressed to a Monk Who Burned Books (III)',
    '394': 'Lamenting Soldiers Dead in the War',
    '441': 'Hell',
    '454': 'I Hate Incense',
    '494': 'Spreading Horse Dung to Cultivate the Mottled Bamboo',
    '512': 'Praising Master Rinzai',
    '531': 'Mori Refusing to Eat (I)',
    '532': 'Mori Refusing to Eat (II)',
    '533': 'Lady Mori Rides in a Cart',
    '535': 'A Beautiful Woman’s Dark Place Has the Fragrance of a Narcissus',
    '536': 'Calling My Hand Mori’s Hand',
    '539': 'Promise to Be Born in the Time of Maitreya',
    '541': 'Blind Girl’s Love Songs at Yakushidō',
    '542': 'I Recall the Old Times Living at Takigi',
    '543': 'Wishing to Thank Mori for My Deep Debt to Her',
    '544': 'Lady Mori’s Afternoon Nap',
    '545': 'Night Conversation in the Dream Chamber',
    '555': 'Fisherman',
    '572': 'Po Lo-t’ien',
    '593': 'Cause and Effect for a Lustful Monk',
    '604': 'Retreating from Mikanohara and Going to Nara',
    '605': 'Untitled [Would that it were the realm of Gods and Immortals]',
    '639': 'The Second Year of Kanshō—Starvation (I)',
    '640': 'The Second Year of Kanshō—Starvation (II)',
    '641': 'The Second Year of Kanshō—Starvation (III)',
    '647': 'The World at War, All Heaven, All Earth, Battle',
    '715': 'Sonrin, Forest of Venerability',
    '771': 'On a Spring Outing to the Tomb of the Retired Emperor Go Komatsu at Unryōin in Sen’yūji',
    '819': 'Dream Chamber (I)',
    '820': 'Dream Chamber (II)',
    '821': 'Dream Chamber (III)',
    '822': 'Dream Chamber (IV)',
    '839': 'When Ikkyū Was Old',
}

OCR_MAP = {
    'i': '7', '8': '8', 'y/': '17', 'ZS': '25', '2)': '27',
    '99': '35', '97': '37', '15': '75', 'Dil': '251',
    'BiZ': '512', 'Dot': '531', '592': '532', '7': '572',
    '593': '593', 'wk': '771'
}

KNOWN_SETS = [
    "Hsii-t’ang’s Three Pivot Phrases",
    "Three Poems to Show the Monks of",
    "Living in the Mountains",
    "Addressed to a Monk Who Burned Books",
    "Three Poems to Show the Assembly",
    "Picture of an Arhat Reveling in a Brothel",
]

def get_trans_lines():
    all_lines = []
    for p_idx in range(88, 201):
        p = strip_page_footer(pages[p_idx])
        for l in p.splitlines():
            all_lines.append(clean_translation_line(l))
    return dehyphenate('\n'.join(all_lines)).splitlines()

def build_translations():
    lines = get_trans_lines()
    
    def get_num(idx, s):
        if idx == 1714 or s == '2':
            return '121'
        if s in OCR_MAP:
            return OCR_MAP[s]
        if s.isdigit() and int(s) in range(1, 900):
            return s
        return None

    def is_set_header(idx, line):
        s = line.strip()
        for sh in KNOWN_SETS:
            if s.startswith(sh):
                if not s.endswith(('.', ':', ';')) and not s.startswith('Hsii-t’ang’s Three Pivot Phrases:'):
                    return True
        return False

    def is_item_start(idx, l):
        s = l.strip()
        if not s: return False
        if s.startswith('Prose Introduction'):
            return True
        if is_set_header(idx, l):
            return True
        if get_num(idx, s):
            return True
        if s.startswith(('Notes:', 'Note:')):
            return True
        return False

    item_starts = []
    for i, l in enumerate(lines):
        if is_item_start(i, l):
            item_starts.append((i, l.strip()))

    out = ["## Translations from the Crazy Cloud Anthology", ""]
    
    for k in range(len(item_starts)):
        pos, s = item_starts[k]
        next_pos = item_starts[k+1][0] if k+1 < len(item_starts) else len(lines)
        chunk = [lines[j] for j in range(pos+1, next_pos) if lines[j].strip()]
        
        # 1. Prose Introduction
        if s.startswith('Prose Introduction'):
            # clean title
            intro_title = s
            # Check if continued on next line
            raw_chunk = [lines[j].strip() for j in range(pos+1, next_pos) if lines[j].strip()]
            if raw_chunk and raw_chunk[0].startswith('to Nos.'):
                intro_title += ' ' + raw_chunk[0]
                raw_chunk = raw_chunk[1:]
            out.append(f"### {apply_typos(intro_title)}\n")
            
            # If prose intro to No. 33, it includes the verse of poem 33 at the end
            if '33' in intro_title:
                # Prose intro paragraphs
                # Split at line 'What precedes is Master Tetto'
                p_text = '\n'.join(raw_chunk)
                split_m = re.search(r'(If your skill cannot work in the Nirvana Hall.*)', p_text, re.DOTALL)
                if split_m:
                    intro_part = p_text[:split_m.start()]
                    verse_part = split_m.group(1)
                    paras = parse_prose(intro_part)
                    for p in paras:
                        out.append(p + "\n")
                    out.append("### Poem 33: A Cup of Rice in a Broken-Footed Cauldron\n")
                    # unwrap verses
                    v_list = [re.sub(r'\s+', ' ', apply_typos(v)).strip() for v in verse_part.splitlines() if v.strip()]
                    # unwrap verses
                    uv = []
                    curr = ''
                    for vl in v_list:
                        if vl.startswith(('If ', 'Confronted', 'I believe', 'One bowl')):
                            if curr: uv.append(curr)
                            curr = vl
                        else:
                            curr += ' ' + vl
                    if curr: uv.append(curr)
                    for v in uv:
                        out.append(v)
                    out.append("")
                else:
                    for p in parse_prose('\n'.join(raw_chunk)):
                        out.append(p + "\n")
            else:
                for p in parse_prose('\n'.join(raw_chunk)):
                    out.append(p + "\n")
            continue
            
        # 2. Set Header
        if is_set_header(pos, lines[pos]):
            set_title = s
            # check if continued (e.g. two poems, three poems)
            if chunk and chunk[0].strip() in ('two poems', 'three poems', 'two      poems', 'My Circle'):
                set_title += f": {chunk[0].strip()}"
            out.append(f"### {apply_typos(set_title)}\n")
            continue
            
        # 3. Poem Number
        num = get_num(pos, s)
        if num:
            title = POEM_TITLES.get(num, f"Poem {num}")
            out.append(f"### Poem {num}: {title}\n")
            
            # Determine title lines to skip in chunk
            t_lines = 0
            if len(chunk) > 0:
                c0 = chunk[0].strip()
                if len(chunk) > 3 and "On a Spring Outing to the Tomb" in c0:
                    t_lines = 3
                elif len(chunk) > 3 and "With a Poem About a Brothel" in c0:
                    t_lines = 3
                elif len(chunk) > 2 and any(k in c0 for k in [
                    "Face to Face with the Beautiful", "On the Topic", "Draw a Line", "Go to the Sea",
                    "One’s Eyes Are Not Yet", "Addressed to an Assembly", "The Great Master Yiian-wu",
                    "Chrysanthemums: An Arhat", "Living in the Mountains", "Congratulating Daiyuan",
                    "A Layman Reciting", "Remorse         over", "No One Sees", "Spreading Horse Dung",
                    "A Beautiful Woman’s Dark", "Wishing to Thank", "Retreating from Mikanohara"
                ]):
                    t_lines = 2
                elif len(chunk) > 1 and any(k in c0 for k in [
                    "Praising Monk", "Straw-Sandal", "Peach Blossom", "The Buddha’s", "Pleasure in Pain",
                    "Pain in Pleasure", "Rinzai Burned", "Praising the Fish-Basket", "Frogs", "Shakuhachi",
                    "Snowball", "Instructing the Cook", "From the Mountains", "Wind Bell", "Straw Raincoat",
                    "Praising P’u-hua", "Under One’s Feet", "Self-Appraisal", "Self-A ppraisal", "On a Brothel",
                    "Addressed to a Monk in the Hall", "Addressed to a Monk at Daitokuji", "Sakyamuni Practicing",
                    "Praising the Dharma Master", "Inscription for", "Pai-chang Fasting", "Presented to a Gathering",
                    "Nirvana Hall", "Composing a Poem", "Fisherman", "Addressed to a Monk Who Killed",
                    "About Disturbances", "Thanking a Man", "Composed When Ill", "Acts of Grace",
                    "The Correct Skill", "Reducing Desires", "Taking a Metaphor", "Praising Saint",
                    "Ridiculing Literature", "Recollecting the Past", "The Stick", "Deluded Enlightenment",
                    "Lamenting Soldiers", "Hell", "1 Hate Incense", "Praising Master Rinzai",
                    "Lady Mori Rides", "Calling My Hand", "Lady Mori's Afternoon", "Night Conversation",
                    "Po Lo-t ien", "Cause and Effect", "Sonrin, Forest"
                ]):
                    t_lines = 1
                else:
                    t_lines = 0
            
            v_lines = chunk[t_lines:]
            
            # Special handling for poems with attached notes without 'Notes:' header
            trailing_notes = []
            if num == '541':
                # 4 verses, then notes
                actual_v = v_lines[:4]
                trailing_notes = v_lines[4:]
                v_lines = actual_v
            elif num == '542':
                # 4 verses, then prose commentary
                actual_v = v_lines[:4]
                trailing_notes = v_lines[4:]
                v_lines = actual_v
            elif num == '715':
                # prose intro was before the 4 verses
                # find where 'Sixteen-foot' starts
                v_start = 0
                for vi, vl in enumerate(v_lines):
                    if 'Sixteen-foot' in vl:
                        v_start = vi
                        break
                prose_intro_lines = v_lines[:v_start]
                v_lines = v_lines[v_start:]
                # output prose intro paragraph
                p_text = ' '.join([vl.strip() for vl in prose_intro_lines])
                p_text = re.sub(r'\s+', ' ', p_text).strip()
                out.append(apply_typos(p_text) + "\n")

            # unwrap verses
            verses = []
            curr = ''
            for l in v_lines:
                st = l.strip()
                if not st: continue
                indent = len(l) - len(l.lstrip())
                if indent >= 2 and curr:
                    curr += ' ' + st
                else:
                    if curr: verses.append(curr)
                    curr = st
            if curr: verses.append(curr)
            
            verses = [re.sub(r'\s+', ' ', apply_typos(v)).strip() for v in verses]
            for v in verses:
                out.append(v)
            out.append("")
            
            if trailing_notes:
                out.append("#### Notes\n")
                tn_text = '\n'.join(trailing_notes)
                if tn_text.startswith('Notes'):
                    tn_text = tn_text[5:].strip()
                for p in parse_prose(tn_text):
                    out.append(p + "\n")
            continue
            
        # 4. Notes Section
        if s.startswith(('Notes:', 'Note:')):
            out.append("#### Notes\n")
            # Parse note paragraphs
            n_lines = chunk
            # If the header line had text after colon
            after_colon = re.sub(r'^(?:Notes:|Note:)\s*', '', s).strip()
            if after_colon:
                n_lines = [after_colon] + n_lines
            for p in parse_prose('\n'.join(n_lines)):
                out.append(p + "\n")
            continue
            
    return '\n'.join(out)

print("Translation builder defined.")

def build_abbreviations():
    out = [
        "## Abbreviations",
        "",
        "- **CZS**: *Chūsei Zenka no Shisō* (中世禅家の思想). Ichikawa Hakugen et al., ed. Tokyo: Iwanami Shoten, 1972.",
        "- **KZ**: *Kyōunshū Zenshaku* (狂雲集全釈). Hirano Sōjō. Tokyo: Shunjūsha, 1976.",
        "- **SP**: *Ssu Pu Pei Yao* (四部備要). Shanghai: Chung hua shu chü, 1936.",
        "- **T**: *Taishō Shinshū Daizōkyō* (大正新修大蔵経). Tokyo: Taishō Issai Kyō Kankōkai, 1922.",
        "- **ZZ**: *Zoku Zōkyō* (続蔵経). Hong Kong: Hong Kong Buddhist Association, 1968.",
        ""
    ]
    return '\n'.join(out)

def build_notes():
    PAGE_GUTTERS = {
        203: 50,
        204: 60,
        205: 53,
        206: 57,
        207: 53,
    }

    NOTE_FIXES = [
        (r'SOM Chivane\s+MO\s+6\s+2\s+Sleep:\s*230b\.', '59. Ch’uan Teng Lu, roll 6, T 51, p. 230b.'),
        (r'60\)\s*CZSsnow\s*177\.\s*Not translated here:', '60. CZS, no. 177. Not translated here.'),
        (r'Us Cie\.\s*240\s*ike,\s*wes\s*Wi,\s*PS\s*284a\.', '73. CZS, no. 240, T 48, p. 284a.'),
        (r'OK Zeal\s*に', '9. KZ, p. 18.'),
        (r'TIT KZeep\.\s*36\.', '11. KZ, p. 36.'),
        (r'230\s*CZSape\s*372\.', '23. CZS, p. 372.'),
        (r'DAN Gh van henoe Lay rol iia\s*wolep:\s*286a\.', '24. Ch’uan Teng Lu, roll 11a, T 51, p. 286a.'),
        (r'D9,\s*KZ pa\s*52:', '29. KZ, p. 52.'),
        (r'DUNS Chins\s*Parola\s*ET', '59. Shih Chi, SP, roll 84, p. 4b.'),
        (r'625\s*CZ;\s*ps\s*429:', '62. CZS, p. 429.'),
        (r'Gbr KZ pul\s*26:', '65. KZ, p. 126.'),
        (r'68:\s*KZ,\s*p\.\s*139\)', '68. KZ, p. 139.'),
        (r'\bKM\b', '78. KZ, p. 176.'),
        (r'dBSy pall Sas', 'roll 7, ZZ, v. 138, p. 116a.'),
        (r'13sps iib:', 'roll 13, p. 11b.'),
        (r'dizi Se collllspa25ab;', 'Tzu, SP, roll 8, p. 25ab.'),
    ]

    all_notes_text = []
    for p in range(203, 208):
        res = subprocess.run(['pdftotext', '-layout', '-f', str(p), '-l', str(p), 'ikkyu_and_the_crazy_cloud_anthology_a_zen_poet_of_medieval_translation.pdf', '-'], capture_output=True, text=True)
        lines = res.stdout.splitlines()[:-2]
        gutter = PAGE_GUTTERS[p]
        left = [l[:gutter].rstrip() for l in lines]
        right = [l[gutter:].rstrip() for l in lines]
        all_notes_text.append('\n'.join(left))
        all_notes_text.append('\n'.join(right))

    full_notes = dehyphenate('\n\n'.join(all_notes_text))
    for pat, rep in NOTE_FIXES:
        full_notes = re.sub(pat, rep, full_notes)

    trans_pos = full_notes.find('Translations\n')
    intro_notes_raw = full_notes[:trans_pos]
    trans_notes_raw = full_notes[trans_pos:]

    def parse_notes_block(raw_text):
        notes = []
        curr = []
        for l in raw_text.splitlines():
            s = l.strip()
            if not s or s in ('Notes', 'Introduction', 'Translations'):
                continue
            m = re.match(r'^(\d+)\.\s+(.*)', s)
            if m:
                if curr:
                    notes.append(' '.join(curr))
                    curr = []
                curr.append(s)
            else:
                if curr:
                    curr.append(s)
        if curr:
            notes.append(' '.join(curr))
        
        cleaned = []
        for n in notes:
            n_clean = re.sub(r'\s+', ' ', n).strip()
            cleaned.append(apply_typos(n_clean))
        return cleaned

    intro_notes = parse_notes_block(intro_notes_raw)
    trans_notes = parse_notes_block(trans_notes_raw)

    out = [
        "## Notes",
        "",
        "### Notes to Introduction",
        ""
    ]
    for n in intro_notes:
        out.append(n)
        out.append("")
        
    out.append("### Notes to Translations")
    out.append("")
    for n in trans_notes:
        out.append(n)
        out.append("")
        
    return '\n'.join(out)

def build_bibliography():
    def parse_bib_section(pages_idx):
        lines = []
        for p in pages_idx:
            text = strip_page_footer(pages[p])
            lines.extend(text.splitlines())
        
        entries = []
        curr = []
        for l in lines:
            s = l.strip()
            if not s or s in ('Bibliography', 'Primary Sources', 'Secondary Sources'):
                continue
            indent = len(l) - len(l.lstrip())
            if indent == 0 and curr:
                entries.append(' '.join(curr))
                curr = []
            curr.append(s)
        if curr:
            entries.append(' '.join(curr))
            
        cleaned = []
        for e in entries:
            e_clean = re.sub(r'\s+', ' ', e).strip()
            cleaned.append(apply_typos(e_clean))
        return cleaned

    prim = parse_bib_section([208, 209])
    sec = parse_bib_section([210, 211, 212])

    out = [
        "## Bibliography",
        "",
        "### Primary Sources",
        ""
    ]
    for e in prim:
        out.append(f"- {e}")
    out.append("")
    
    out.append("### Secondary Sources")
    out.append("")
    for e in sec:
        # Check if second work by Arntzen
        if e.startswith('Arntzen, Sonja.') and '“The Poetry of the Kyōunshū' in e:
            parts = e.split('“The Poetry of the Kyōunshū')
            e1 = parts[0].strip('. ')
            e2 = '“The Poetry of the Kyōunshū' + parts[1]
            out.append(f"- {e1}")
            out.append(f"- ——. {e2}")
        else:
            out.append(f"- {e}")
    out.append("")
    return '\n'.join(out)

def build_index_of_poems():
    lines = []
    for p in range(214, 218):
        text = strip_page_footer(pages[p])
        lines.extend(text.splitlines())

    entries = []
    curr = []
    for l in lines:
        s = l.strip()
        if not s or s == 'Index to Poems' or 'Most poems     are indexed under' in l or 'titles have been provided' in l or 'the poem or are indexed' in l:
            continue
        indent = len(l) - len(l.lstrip())
        if indent == 0 and curr:
            entries.append(' '.join(curr))
            curr = []
        curr.append(s)
    if curr:
        entries.append(' '.join(curr))

    cleaned = []
    for e in entries:
        e_clean = re.sub(r'\s+', ' ', e).strip()
        cleaned.append(apply_typos(e_clean))

    out = [
        "## Index of Poems",
        "",
        "Most poems are indexed under their titles. Those without titles have been provided with one based on the content of the poem or are indexed under their first lines. Numbers refer to the pages of the original publication.",
        ""
    ]
    for e in cleaned:
        out.append(f"- {e}")
    out.append("")
    return '\n'.join(out)

def build_glossary_index():
    all_entries = []
    for p in range(218, 221):
        lines = strip_page_footer(pages[p]).splitlines()
        left, right = [], []
        for l in lines:
            if not l.strip() or 'Glossary-Index' in l:
                continue
            gutter = 48
            left.append(l[:gutter].rstrip())
            if len(l) > gutter:
                right.append(l[gutter:].rstrip())
        for col in [left, right]:
            curr = []
            for l in col:
                s = l.strip()
                if not s:
                    if curr:
                        all_entries.append(' '.join(curr))
                        curr = []
                    continue
                indent = len(l) - len(l.lstrip())
                if indent == 0 and curr:
                    all_entries.append(' '.join(curr))
                    curr = []
                curr.append(s)
            if curr:
                all_entries.append(' '.join(curr))

    cleaned = []
    for e in all_entries:
        e_clean = re.sub(r'\s+', ' ', e).strip()
        cleaned.append(apply_typos(e_clean))

    out = [
        "## Glossary-Index",
        "",
        "Terms and proper names appearing in the book with their original kanji / Chinese characters and original page references.",
        ""
    ]
    for e in cleaned:
        out.append(f"- {e}")
    out.append("")
    return '\n'.join(out)

# Main Assembly
print("Assembling entire book...")
full_doc = []
full_doc.append(build_frontmatter())
full_doc.append(build_foreword())
full_doc.append(build_preface())
full_doc.append(build_introduction())
full_doc.append(build_translations())
full_doc.append(build_abbreviations())
full_doc.append(build_notes())
full_doc.append(build_bibliography())
full_doc.append(build_index_of_poems())
full_doc.append(build_glossary_index())

final_markdown = '\n'.join(full_doc)

output_filename = "ikkyu_and_the_crazy_cloud_anthology_a_zen_poet_of_medieval_translation.md"
with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(final_markdown)

print(f"Successfully generated {output_filename} ({len(final_markdown)} characters, {len(final_markdown.splitlines())} lines).")
