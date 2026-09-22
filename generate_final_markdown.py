import re
import subprocess
import os

with open('ikkyu_and_the_crazy_cloud_anthology_a_zen_poet_of_medieval_translation.raw.md', 'r', encoding='utf-8') as f:
    pages = f.read().split('\x0c')

# 1. Comprehensive Typo and OCR normalization dictionary
#
# Macrons are what the OCR loses first, so every romanized proper noun in this
# book has one correct spelling and a long tail of wrong ones. Enumerating the
# tail does not converge -- match the shape instead. O is the OCR's repertoire
# for a long o; the correct forms use ō and ū, which are in none of the classes
# below, so a fixed spelling is never matched a second time.
O = '[oO06QGd]'
OE = '[oO06QGde]'   # kōan also OCRs as "Kean"

TYPO_FIXES = [
    # The subject's own name. The OCR produces some twenty spellings of it and
    # the tail is long, so match the stem rather than enumerate: anything that
    # reads "Ikky" plus ASCII junk is the name. "Ikkyū" itself is safe from
    # these -- the ū is not in any of the junk classes.
    # 一休 in a Japanese book title, read as kana plus noise.
    (r'(?:\d\s*)?た\s*k?y[gz]\b', 'Ikkyū'),
    (r'\bTokushi\b', 'Tokushū'),
    (r'\bOsho\b', 'Oshō'),
    (r'\bKenkyu\b', 'Kenkyū'),
    (r'\bTkita\b', 'Ikita'),
    (r'\bHirano Sojo\b', 'Hirano Sōjō'),
    # "ofthe", "ofhistorians", "ofJapan": the space after "of" is the one the
    # OCR drops most. Every English word that really begins "of" is off-, oft
    # or often. The three-word runs it leaves behind are named.
    (r'\bofiryi\b', 'of fūryū'),      # note 77, "explanation of fūryū"
    (r'\bof(?!f|ten\b|t\b)(?=[A-Za-z])', 'of '),
    (r'\btheFounder\b', 'the Founder'),
    (r'\bherselfto\b', 'herself to'),
    (r'\bweforget\b', 'we forget'),
    (r'\ba(?=simple\b|snail\b|peach\b|country\b|monastic\b|flick\b|hundred\b|moment\b)', 'a '),
    # Hyphens the print carries and dehyphenate() drops, since neither half is
    # in its keep-list. Checked against the raw: each breaks across a line.
    (r'\bandsand\b', 'and-sand'),
    (r'\bbrokenfooted\b', 'broken-footed'),
    (r'\bcloudrain\b', 'cloud-rain'),
    (r'\blongstanding\b', 'long-standing'),
    (r'\bpleasureloving\b', 'pleasure-loving'),
    (r'\bsimpleminded\b', 'simple-minded'),
    (r'\bslopwater\b', 'slop-water'),
    (r'\btwentyseventh\b', 'twenty-seventh'),
    (r'\bdrunkeness\b', 'drunkenness'),
    (r'\bcommited\b', 'committed'),
    (r'\bT?[I1]kky[a-zA-Z@#]*[\'’]s\b', 'Ikkyū’s'),
    (r'\bT?[I1]kky[a-zA-Z@#]*s\b', 'Ikkyū’s'),
    (r'\bT?[I1]kky[a-zA-Z@#]+', 'Ikkyū'),
    (r'\bT?[I1]kky\b', 'Ikkyū'),
    (r'\bIkkyū[\'’]s(?=enlightenment)', 'Ikkyū’s '),
    (r'\bIkkyū\'s\b', 'Ikkyū’s'),
    (rf'\bS{O}jun\b', 'Sōjun'),
    (rf'\bKy{O}unsh[a-z]*\b', 'Kyōunshū'),
    (rf'\bk{OE}an\b', 'kōan'),
    (rf'\bk{OE}ans\b', 'kōans'),
    (rf'\bK{OE}an\b', 'Kōan'),
    (rf'\bY{O}Q?s{O}[\'’]s\b', 'Yōsō’s'),
    (rf'\bY{O}Q?s{O}s\b', 'Yōsō’s'),
    (rf'\bY{O}Q?s{O}\b', 'Yōsō'),
    (rf'\bDait{O}[\'’]s\b', 'Daitō’s'),
    (rf'\bDait{O}\b', 'Daitō'),
    (rf'\bDaid{O}?\b', 'Daitō'),
    (r'\bDaitokwji\b', 'Daitokuji'),
    (rf'\bKas{O}[\'’]s\b', 'Kasō’s'),
    (rf'\bKas{O}\b', 'Kasō'),
    (rf'\bGoj{O}\b', 'Gojō'),
    (r'\bSoj687\b', 'Sōjō [87]'),
    (r'\bSeizan88\b', 'Seizan [88]'),
    (r'\bSh[t]?iichi Kat[oō]\b', 'Shūichi Katō'),
    (r'\bKat[oō] Sh[t]?iichi\b', 'Shūichi Katō'),
    # fūryū: "fury", "faryu", "fnryu", "firyii", "frya", ... Spelled out rather
    # than f[aiun]*ry[aiun]* so that "fairy" is not swept up with it. Before the
    # ii sweep, which would otherwise claim "firyii" for Wade-Giles.
    (r'\b([fF])(?:u|a|i|n|ur|an)?ry(?:u|a|i|d|ii)?\b、', r'\1ūryū, '),
    (r'\b([fF])(?:u|a|i|n|ur|an)?ry(?:u|a|i|d|ii)?\b', r'\1ūryū'),
    # Both Wade-Giles ü and Japanese ū come out of the OCR as "ii". Which one
    # a word wants is not recoverable from the shape, so the handful of
    # Japanese and Sanskrit ones are named and the rest -- all Wade-Giles --
    # fall to the sweep below.
    (r'\bexhibiion\b', 'exhibition'),
    (r'\bAsii-t’ang\b', 'Hsü-t’ang'),
    (r'\b([Ss])iitra\b', r'\1ūtra'),
    (r'\bSiirangama\b', 'Sūrangama'),
    (r'\bChiisei\b', 'Chūsei'),
    (r'\bShunjiisha\b', 'Shunjūsha'),
    (r'\bSh[t]?iichi\b', 'Shūichi'),
    (r'\bKenkyii\b', 'Kenkyū'),
    (r'\bTokushii\b', 'Tokushū'),
    (r'\bShiion\b', 'Shūon'),
    (r'\bKokyiian\b', 'Kokyūan'),
    (r'\bChiigoku\b', 'Chūgoku'),
    (r'\bDa[it]y[aiu]+n\b', 'Daiyūan'),
    (r'\bDa[it]y[aiu]*\b', 'Daiyū'),
    (r'(?<![aeiouAEIOUvVxX])ii', 'ü'),
    # Dehyphenation fuses the Chinese names that break across a line.
    (r'\bHs[tuü]+[ec]?h?-?tou\b', 'Hsüeh-tou'),
    (r'\bHsüch\b', 'Hsüeh'),
    (r'\bHsütang\b', 'Hsü-t’ang'),
    (r'\bYünmen\b', 'Yün-men'),
    (r'\bYüanming\b', 'Yüan-ming'),
    (r'\bSungyüan\b', 'Sung-yüan'),
    (r'\bNan-?c[hl]’üan\b', 'Nan-ch’üan'),
    (r'\bWenchün\b', 'Wen-chün'),
    (r'\bKüang\b', 'Kuang'),
    (r'\bChü-’i\b', 'Chü-i'),
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
    # Endnote digits fused to the word before them (STYLE.md §4.2): the print
    # sets a bare superscript digit and OCR welds it onto the preceding word
    # or its closing parenthesis. Bracket it -- nothing else in the book
    # writes a bracketed digit, so the form is unambiguous downstream.
    # Excludes "p.61", the one real citation with no space before its digits.
    (r'(?<!\bp)([.?])(\d{1,3})\b', r'\1 [\2]'),
    (r'\)(\d{1,3})\b', r') [\1]'),
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

HYPHEN_PAT = re.compile(r'([a-zA-Z]+)-\n\s*([a-zA-Z]+)')

def join_hyphen(m):
    w1, w2 = m.group(1), m.group(2)
    if w1.lower() in ('non', 'self', 'well', 'all', 'cross'):
        return f'{w1}-{w2}'
    return f'{w1}{w2}'

def dehyphenate(text):
    return HYPHEN_PAT.sub(join_hyphen, text)

def strip_page_footer(page_text):
    pat = r'\n\s*\S+\s+(?:FOREWORD|PREFACE|INTRODUCTION|POEM\s+NUMBER\s+\d+|I?NOTES\s+TO\s+PAGES.*|BIBLIOGRAPHY|INDEX\s+TO\s+POEMS|GLOSSARY-INDEX|ABBREVIATIONS)\s*$'
    return re.sub(pat, '', page_text.rstrip(), flags=re.IGNORECASE)

cjk_pat = re.compile(r'[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff\uff00-\uffef]')

word_pat = re.compile(r'\b[A-Za-z][a-z]{2,}\b')
shout_pat = re.compile(r'\b[A-Z][A-Za-z]*[A-Z][A-Za-z0-9]*\b')

# Two or more all-caps tokens in a row: the OCR's failed reading of the
# Chinese column -- "ABA RE", "BRETC EER". Used by drop_column() to confirm
# that what sits right of a measured gutter really is the column.
shout_run_pat = re.compile(r'(?<![.\w])(?:\b[A-Z]{2,}\b[ ]?){2,}')

def is_column_junk(tail):
    """Is this the Chinese column, read by the OCR as Latin?

    The print edition sets the original in a right-hand column. Where the OCR
    read it as CJK the character range finds it; where it failed it produced
    things like "TEL ek RE 9S", which only a shape test can tell from the
    continuation of an English sentence across the same gutter. English prose
    is made of ordinary words; the column has none, or one flanked by capital
    salad.
    """
    if re.fullmatch(r"[a-z’'\-.,;:!?]+", tail.strip()):
        return False          # "up", "ado." -- a short word the line broke before
    words = word_pat.findall(tail)
    return not words or (len(words) <= 1 and len(shout_pat.findall(tail)) >= 2)

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
    # Three spaces, not four: on the tightest lines the gutter comes through as
    # only three. A wide gap that far into a line is as often prose the OCR
    # spaced badly, so cut only where what follows is the column.
    for m in re.finditer(r'\s{3,}\S', line):
        col = m.end() - 1
        if col < 45:
            continue
        if col - m.start() >= 4 or is_column_junk(line[col:]):
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

POEM7_DEATH_VERSE = re.compile(
    r'(?P<pre>.*admired:) '
    r'Eighty-five years Knowing nothing even about the Patriarchs, '
    r'Rowing with my elbow, serving, going, '
    r'Erasing my tracks in the Great Void\. \[4\] '
    r'(?P<post>Yü-wang:.*)'
)

def split_poem7_death_verse(paras):
    """Re-break Hsü-t'ang's death poem out of poem 7's flattened note.

    See STYLE.md §3.3. The raw OCR still shows the print's own line breaks
    (checked against the PDF), which parse_prose has no way to keep.
    """
    out = []
    for p in paras:
        m = POEM7_DEATH_VERSE.match(p)
        if not m:
            out.append(p)
            continue
        out.append(m.group('pre'))
        out.append('Eighty-five years\n'
                    'Knowing nothing even about the Patriarchs,\n'
                    'Rowing with my elbow, serving, going,\n'
                    'Erasing my tracks in the Great Void. [4]')
        out.append(m.group('post'))
    return out

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
        "### Plate 3: Ikkyū’s Death Poem",
        "",
        "![Plate 3: Ikkyū’s Death Poem](images/plate_3_death_poem.png)",
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

def drop_column(page_text):
    """Cut the Chinese column off a two-column Introduction page.

    Spec 008 requirement 2 recorded this as needing "its own extraction logic"
    because the Introduction's English wraps around the column. It does not --
    the page is an ordinary two-column setting, English left and the original
    right. What went wrong is that build_introduction() joins the lines into
    paragraphs without cutting the column off first, so the right-hand text
    lands *between* two English words: "they would ignore fF, DARRZ karma and
    the world..." That reads as interleaving but is only a missing cut.

    clean_translation_line() is the poem files' cut and is wrong here. It
    treats any run of three spaces past column 45 as the gutter, and the
    Introduction is set justified, so it also eats stretched word spacing --
    52 lines, including "his craziness" and "balancing act".

    find_gutter() measures the blank run instead of guessing at it, and the
    measurement doubles as the test for whether to cut at all: a one-column
    page has no such run, raises, and is returned untouched. Over the three
    sections this removes 363 CJK characters and garbage runs and leaves every
    English word standing.
    """
    lines = page_text.splitlines()
    if not lines or not max(map(len, lines), default=0):
        return page_text
    try:
        gutter = find_gutter(lines)
    except ValueError:
        return page_text                  # one column: nothing to cut
    right = '\n'.join(l[gutter:] for l in lines)
    # A gutter alone is not enough -- a page can have a wide blank run for
    # other reasons. Cut only where what is to the right of it is the column.
    if not (cjk_pat.search(right) or shout_run_pat.search(right)):
        return page_text
    return '\n'.join(l[:gutter].rstrip() for l in lines)


def intro_page(i):
    """One Introduction page: footer off, Chinese column off."""
    return drop_column(strip_page_footer(pages[i]))


def build_introduction():
    # Section 1: p26 to p58 line 24
    p26_to_57 = '\n'.join([intro_page(i) for i in range(26, 58)])
    p58_lines = drop_column(pages[58]).splitlines()
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
        p58_to_62_lines.extend(intro_page(idx).splitlines())
    p62_lines = intro_page(62).splitlines()
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
        p62_to_82_lines.extend(intro_page(idx).splitlines())
    p82_lines = intro_page(82).splitlines()
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
        p82_to_84_lines.extend(intro_page(idx).splitlines())
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

# The running foot of every translation page reads "<page>  POEM NUMBER  <n>",
# where <n> is the first or last poem opening on that page. It is the only
# independent witness to a poem's number, and the OCR of the big display number
# at the head of a poem is not reliable -- on p. 101 it reads "8" where the poem
# is no. 93. Keep the foot to arbitrate.
FOOT_NUM = re.compile(r'POEM\s+NUMBER\s+(\d+)\s*$', re.IGNORECASE)

def get_trans_lines():
    """The translation pages as lines, plus each line's page-foot poem number.

    Dehyphenation joins lines across the whole run, so page starts are tracked
    by raw line number and shifted by however many lines each join swallowed.
    A marker line in the text would be simpler but would also block the joins
    that straddle a page break.
    """
    all_lines = []
    page_starts = []
    for p_idx in range(88, 201):
        m = FOOT_NUM.search(pages[p_idx].rstrip())
        page_starts.append((len(all_lines), m.group(1) if m else None))
        for l in strip_page_footer(pages[p_idx]).splitlines():
            all_lines.append(clean_translation_line(l))

    text = '\n'.join(all_lines)
    joins = []
    def log_join(m):
        joins.append((text.count('\n', 0, m.start()), m.group(0).count('\n')))
        return join_hyphen(m)
    lines = HYPHEN_PAT.sub(log_join, text).splitlines()

    foots = [None] * len(lines)
    for raw, foot in page_starts:
        i = raw - sum(n for at, n in joins if at < raw)
        for j in range(min(i, len(lines)), len(lines)):
            foots[j] = foot
    return lines, foots

def build_translations():
    lines, foots = get_trans_lines()

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

    # Poem numbers run monotonically through the anthology. Where the display
    # number OCRs to something that would run backwards, believe the page foot
    # instead -- p. 101 reads "8" for poem no. 93, and nothing downstream can
    # tell a wrong poem number from a right one.
    item_starts = []
    last_num = 0
    for i, l in enumerate(lines):
        if not is_item_start(i, l):
            continue
        s = l.strip()
        num = None if is_set_header(i, l) else get_num(i, s)
        if num:
            if int(num) <= last_num and foots[i] and int(foots[i]) > last_num:
                num = foots[i]
            assert int(num) > last_num, f'poem {num} after {last_num} at line {i}: {s!r}'
            last_num = int(num)
        item_starts.append((i, s, num))

    out = ["## Translations from the Crazy Cloud Anthology", ""]
    
    for k in range(len(item_starts)):
        pos, s, num = item_starts[k]
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
            # The column gutter survives inside these headings as a run of
            # spaces, and the count ("two poems") sits on either the heading
            # line or the one below it.
            set_title = re.sub(r'\s+', ' ', s)
            cont = re.sub(r'\s+', ' ', chunk[0].strip()) if chunk else ''
            if cont in ('two poems', 'three poems'):
                set_title += f': {cont}'
            elif cont == 'My Circle':
                set_title += f' {cont}'
            set_title = re.sub(r'(?<!:) (two|three) poems$', r': \1 poems', set_title)
            out.append(f"### {apply_typos(set_title)}\n")
            continue
            
        # 3. Poem Number
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
            note_paras = parse_prose('\n'.join(n_lines))
            if num == '7':
                # STYLE.md §3.3: Hsü-t'ang's death poem, quoted inline in the
                # note, is a stanza in the print edition but parse_prose has
                # no way to tell a quoted verse from a quoted anecdote and
                # flattens both alike (checked: doing this generally turns
                # dozens of quoted kōans in other notes into fake "verse").
                # This is the one case confirmed against the raw OCR.
                note_paras = split_poem7_death_verse(note_paras)
            for p in note_paras:
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

def find_gutter(lines):
    """The column at which the right-hand column of a two-column page starts.

    Measured rather than tabulated. The gap between the columns is the one run
    of columns blank on every line of the page, so the right column starts just
    after it. A tabulated gutter set one column too wide shaves the first
    letter off every line of the right column and leaves it at the end of the
    left one -- which is what "the Onin N War" and "the Muromachi t period"
    are: a whole page of notes with a column of stray letters combed into it.
    """
    width = max(map(len, lines))
    blank = [c for c in range(width)
             if all(len(l) <= c or l[c] == ' ' for l in lines)]
    runs = []
    for c in blank:
        if runs and runs[-1][1] == c - 1:
            runs[-1][1] = c
        else:
            runs.append([c, c])
    wide = [r for r in runs if r[1] - r[0] >= 2]
    if not wide:
        raise ValueError('no column gutter found')
    start, end = min(wide, key=lambda r: (r[0] - r[1],
                                          abs((r[0] + r[1]) / 2 - width / 2)))
    return end + 1

def build_notes():
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
        gutter = find_gutter(lines)
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
