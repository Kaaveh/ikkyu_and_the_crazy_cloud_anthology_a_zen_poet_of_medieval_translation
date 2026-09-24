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
    (r'\beverbeleaguered\b', 'ever-beleaguered'),
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
    # "Daid" is not always a mangled "Daitō". Three of its four occurrences in
    # the OCR are Daiō Kokushi -- Hsü-t'ang's student and Daitō's own master --
    # and mapping them all to Daitō erased him from the book and made poem 7's
    # note say Hsü-t'ang instructed Daitō, which he did not. Checked against
    # pp. 93, 94 and 105 of the scan. Only the Daitokuji founder is Daitō.
    (rf'\bDaid{O}?\b(?=,\s*founder)', 'Daitō'),
    (rf'\bDaid{O}?\b', 'Daiō'),
    # An ideographic comma the OCR left in English prose, in text the gutter
    # fix above restores. Targeted, not a general 、 -> , rule: four more sit
    # in preface.md and introduction-1/3, whose Persian is already translated,
    # and re-running 67 K characters of Introduction for a comma is not a
    # trade worth making. Those four are recorded in spec 008 instead.
    (r'kōan、 no\.', 'kōan, no.'),
    # p. 132 reads "as warm as a cave in winter". The capital is the OCR's,
    # and left standing it reads as a proper noun in a poem line. Matched
    # without "winter": typos are applied per line and the verse breaks
    # between "in" and "winter". \s+ because this is a verse line and the
    # justified spacing has not been collapsed yet at this point.
    (r'as warm\s+as a Cave\b', 'as warm as a cave'),
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
    # Yüeh Küang, of the Chin Shu anecdote in poem 27's note: the print has the
    # umlaut (p. 97, and the glossary). The OCR gives five spellings of him.
    (r'\bY[a-zü]*eh K[a-zü]*ang\b', 'Yüeh Küang'),
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
    # Spec 010 session 2, poems 37-66, scan pp. 102-112. Each checked against
    # the page image. The endnote markers come first: the rules below them
    # would bracket a misread number as it stands.
    # Session 1's decade, pp. 89-101, re-read for markers alone.
    (r'comely woman\.!', 'comely woman. [1]'),
    (r'can’t answer 5 sums', 'can’t answer” [5] sums'),
    (r'denizen of hell\.’', 'denizen of hell. [7]'),
    (r'relieved\.9', 'relieved. [6]'),
    (r'\((2[67]) (?=the bow|son of)', r'[\1] '),   # poem-number labels, p. 97
    (r'\bsouls210\b', 'souls? [10]'),
    (r'\bYGanwu', 'Yüan-wu'),
    (r'deep meaning\.”', 'deep meaning.” [11]'),       # digits lost entirely
    (r'inspection\.!2', 'inspection. [12]'),
    (r'completely at\s+will\.18', 'completely at will. [13]'),
    (r'response\.”(?=$| One, two)', 'response.” [17]'),
    (r'grass\.”"!8', 'grass.” [18]'),
    (r'dung\.\?°', 'dung. [20]'),
    (r'lips\.’’24', 'lips.” [21]'),
    (r'world\.”(?= As can be seen)', 'world.” [26]'),
    (r'object\.’’2\?', 'object.” [27]'),
    (r'destroyed\.’’3®', 'destroyed.” [30]'),
    (r'Buddha-nature\.”3!', 'Buddha-nature.” [31]'),
    (r'itch\.”’2', 'itch.” [32]'),
    (r'enlightened\.\*8', 'enlightened. [33]'),
    (r'capacity\.33', 'capacity. [34]'),
    (r'poem no\. Tk\b', 'poem no. 71.'),
    (r'\brennorseful\b', 'remorseful'),
    (r'\bSGto\b', 'Sōtō'),
    (r'\bIam\b', 'I am'),
    (r'\bTs ao-shan\b', 'Ts’ao-shan'),
    (r'\.\.\.@ burning', '. . . a burning'),
    (r'\bwas also tryu\b', 'was also fūryū'),
    (r'then ll be\b', 'then I’ll be'),
    (r'and burn, \| An', 'and burn, . . . : An'),
    (r'\bWuc-tsu\b', 'Wu-tsu'),
    (r'\bHui Yian\b', 'Hui Yüan'),
    (r'\b([Ss])itra\b', r'\1ūtra'),
    (r'voice\.’”’', 'voice.’”'),
    # pp. 91-94, the notes to "The Scriptures Wipe Away Filth" (poems 69-71),
    # each checked on the page. Anchored on their own text, and ahead of the
    # general marker rules below, which would bracket the wrong digit.
    (r'wiping filth\.’3\? 69\]', 'wiping filth.” [37] [69]'),
    (r'\bSea Dragon King Stitra\b', 'Sea Dragon King Sūtra'),
    (r'\(79 (?=bow’s reflection)', '[70] '),
    (r'\bOn Wu-tai mountain\b', 'On Wu-t’ai mountain'),
    (r'pisses at the sky\.4°', 'pisses at the sky. [40]'),
    (r'\bPi (?=On the south side of the mountain)', '[71] '),
    (r'gold is like dung \?42', 'gold is like dung? [41]'),   # 42 in the OCR
    (r'fragrant flowing water\.’ 3\b', 'fragrant flowing water.’” [42]'),
    (r'\bconJures\b', 'conjures'),
    (r'“Fallen Hower "is\b', '“Fallen flower” is'),
    # pp. 89-100, poems 68-90 (spec 010, session 3), each checked on the page.
    # Two markers carry the wrong number, so these too run ahead of the
    # general marker rules.
    (r'wife of a layman\.”’', 'wife of a layman.”'),
    (r'the bottom of the well\.’’48', 'the bottom of the well.” [43]'),  # 48 in the OCR
    (r'\bT ien-pao\b', 'T’ien-pao'),
    (r'Hinayana “‘lesser vehicle”', 'Hinayana “lesser vehicle”'),
    (r'the term ““Arhat”’', 'the term “Arhat”'),
    (r'let you go yet\. Ch’', 'let you go yet.” Ch’'),
    (r'interjects, ““At the first', 'interjects, “At the first'),
    (r'hit him with it\."35', 'hit him with it.” [45]'),             # 35 in the OCR
    (r'notes to poem no, 54\.\)', 'notes to poem no. 54.)'),
    (r'\(90 Daité:', '[90] Daitō:'),
    (r'Letter from Nanko”', 'Letter from Nankō”'),
    (r'“Mountain Road”’ has', '“Mountain Road” has'),
    (r'In the years of Kansho,', 'In the years of Kanshō,'),         # p. 167
    # pp. 100-108, poems 91-115 (spec 010, session 4), each checked on the
    # page. Markers first, for the same reason as above.
    (r'Kuei-tsung hit him again\.4\?', 'Kuei-tsung hit him again. [47]'),
    (r'problem of relations between men and women\.”5\?', 'problem of relations between men and women.” [50]'),
    (r'polished balustrade\.5\?', 'polished balustrade. [57]'),
    (r'originating in the Wen Hsüan\.6°', 'originating in the Wen Hsüan. [60]'),
    (r'\bWu Teng Aui Yüan\b', 'Wu Teng Hui Yüan'),
    (r'“I’m: going here', '“I’m going here'),
    (r'Zen of Five flavors\.”’', 'Zen of Five flavors.”'),
    (r'two lines ina poem', 'two lines in a poem'),
    (r'heaviness of other flavors \?', 'heaviness of other flavors?'),
    (r'shout ‘‘Katsu,”’', 'shout “Katsu,”'),
    (r'shout “Katsu\. \(See', 'shout “Katsu.” (See'),
    (r'a charlatan\.”’', 'a charlatan.”'),
    (r'burned the hermitage, is one', 'burned the hermitage,” is one'),
    (r'doctrine of Ryozen is swept', 'doctrine of Ryōzen is swept'),
    (r'doctrine of Rydzen: Ryozcens style', 'doctrine of Ryōzen: Ryōzen’s style'),
    (r'\boppor- _ tunity\b', 'opportunity'),
    (r'One said, ““The banner moves', 'One said, “The banner moves'),
    (r'“The wind moves\. Hui-neng', '“The wind moves.” Hui-neng'),
    (r'midnight watch at noon\.55', 'midnight watch at noon.” [55]'),
    (r'receding into the stancc\.', 'receding into the distance.'),
    (r'\bHalfaCloud\b', 'Half a Cloud'),
    (r'\blibrarian Shoen\b', 'librarian Shōen'),
    # pp. 109-115, poems 117-134 (spec 010, session 5), each checked on the
    # page. Markers first, as above.
    (r'in a revolting way\.’61', 'in a revolting way.” [61]'),
    (r'common likes of you\.”’6\b', 'common likes of you.” [62]'),
    (r'kings and dukes \?68', 'kings and dukes? [63]'),
    (r'red thread is not yet severed\?’64', 'red thread is not yet severed?” [64]'),
    (r'Buddha of the future\.’’6°', 'Buddha of the future.” [65]'),
    (r'\bDaiki Koja Zenji\b', 'Daiki Kōjū Zenji'),
    (r'the Essential Message\.’ So', 'the Essential Message.” So'),
    (r'splendid fame, 1s what', 'splendid fame, is what'),
    (r'How about Lan-tsan turning', 'How about Lan-ts’an turning'),
    (r'Master as: Kasō Sddon', 'Master Kasō: Kasō Sōdon'),
    (r'\bYSso \(1376', 'Yōsō (1376'),
    (r'bring about Ch us defeat', 'bring about Ch’u’s defeat'),
    (r'Lan-tsan was roasting', 'Lan-ts’an was roasting'),
    (r'messenger\? Lan-ts an replied', 'messenger?” Lan-ts’an replied'),
    (r'“great activity’ and', '“great activity” and'),
    (r'\bP’yu-hua:', 'P’u-hua:'),
    (r'\bKasé’s descendant', 'Kasō’s descendant'),
    (r'"1 know Zen best', '“I know Zen best'),
    (r'last words of Tetto,', 'last words of Tettō,'),
    (r'words of the scriptures ;', 'words of the scriptures;'),
    # Lan-ts'an elsewhere, found by the same session: pp. 51-52 print
    # "Lan-ts'an", p. 66 prints "Lan-t'san" twice -- the book's own slip.
    (r'alluding to Lan-tsan who baked', 'alluding to Lan-ts’an who baked'),
    (r'the mention of Lan-ts an\.', 'the mention of Lan-ts’an.'),
    (r'applies it to Lan-tsan\. Lan-t’san’s', 'applies it to Lan-t’san. Lan-t’san’s'),
    # pp. 115-122, poems 135-175 (spec 010, session 6), each checked on the
    # page. Markers first, as above.
    (r'not mere fabrications\.66', 'not mere fabrications.” [66]'),
    (r'“I have pacified your mind\.67', '“I have pacified your mind.” [67]'),
    (r'to the present day\.”\?!', 'to the present day.” [71]'),
    (r'tusks of Tozan', 'tusks of Tōzan'),
    (r'Tozan “sword mountain is', 'Tōzan “sword mountain” is'),
    (r'great compassion \.\. \. Feast', 'great compassion... Feast'),
    (r'Vimalakirti Sutra\. Vimalakirti describes', 'Vimalakirti Sūtra. Vimalakirti describes'),
    (r'with great\s+compassion\.’ \(See', 'with great compassion.” (See'),
    (r'of “far-out\. \(See', 'of “far-out.” (See'),
    (r'"to\s+cast one’s body into Hames represents', '“to cast one’s body into flames” represents'),
    (r'oneself into Hames\.', 'oneself into flames.'),
    (r'^1 am convinced there is no natural', 'I am convinced there is no natural'),
    (r'Crazy madinan stirring', 'Crazy madman stirring'),
    (r"K'uei-chi's samadhi", 'K’uei-chi’s samadhi'),
    (r'entry for\s+K uei-chi\.', 'entry for K’uei-chi.'),
    (r'obeisance\. Hejust went', 'obeisance. He just went'),
    (r'biographical study of Kuci-?\s*chi,', 'biographical study of K’uei-chi,'),
    (r'the Lotus\s+Sutra\. He asserted', 'the Lotus Sūtra. He asserted'),
    (r'Ostensibly YsQ was', 'Ostensibly Yōsō was'),
    (r'“man from P’u-chou”’ was', '“man from P’u-chou” was'),
    # pp. 123-130, poems 176-210 (spec 010, session 7), each checked on the
    # page. Markers first, as above. p. 124 sets "eating.72" with no quote to
    # close; p. 130 opens a paragraph at "Ikkyū often refers" that the marker
    # digit hid from parse_prose(), left as the Prose block quotes shape.
    (r'Pai-chang stopped eating\.”2\b', 'Pai-chang stopped eating. [72]'),
    (r'constantly said, “You shall all become Buddhas!’ 74\b',
     'constantly said, ‘You shall all become Buddhas!’” [74]'),
    (r'Sung-yüan Yü-lu®> presents', 'Sung-yüan Yü-lu [75] presents'),
    (r'Ku-tsun-su Yü-lu\.\?\? Ikkyū', 'Ku-tsun-su Yü-lu. [77] Ikkyū'),
    (r'realm of the Devil\.’ 79 Ikkyū', 'realm of the Devil.’” [79] Ikkyū'),
    (r'rule was ‘a day of no work', 'rule was “a day of no work'),
    (r'in the universe, “\*\.\.\. when he saw', 'in the universe, “... when he saw'),
    (r'Master Sung-ytian was', 'Master Sung-yüan was'),
    (r'Po-yün \(1025- 72\)', 'Po-yün (1025-72)'),
    (r'before Sung-yuan himself', 'before Sung-yüan himself'),
    (r'\bBuddhaDevil\b', 'Buddha-Devil'),
    (r'\bSungdynasty\b', 'Sung-dynasty'),
    (r'\bChingsu\b', 'Ch’ing-su'),
    (r'to eat this fruit\. Tou-shuai said', 'to eat this fruit.” Tou-shuai said'),
    (r'Ch’ing-su said, “Tz’u-ming\. I', 'Ch’ing-su said, ‘Tz’u-ming. I'),
    (r'understand his Path\? Then,', 'understand his Path?’ Then,'),
    (r'relents and says: ““ “You have a go', 'relents and says: “‘You have a go'),
    (r'Ch’ing-su said: “You can enter', 'Ch’ing-su said: ‘You can enter'),
    # pp. 130-137, poems 216-264 (spec 010, session 8), each checked on the
    # page. Markers first. p. 135 sets "plowed.86" with no quote to close.
    (r'\ba cat\.81\b', 'a cat.” [81]'),
    (r'returning home\.’’82\b', 'returning home.” [82]'),
    (r'Wu-men Kuan\.8\?', 'Wu-men Kuan. [83]'),
    (r'and marvelous\.”’8\?', 'and marvelous.” [87]'),
    (r'night after night singing,', 'night after night singing.'),
    (r'call up Ch Yüan’s', 'call up Ch’ü Yüan’s'),
    (r'little Nan-ch’tian;', 'little Nan-ch’üan;'),
    (r'\bpoetry ;', 'poetry;'),
    (r'in a tea pot drawn', 'in a tea pot” drawn'),
    (r'“cnlightenment poem', '“enlightenment” poem'),
    # Sōki. The glossary-index has "Soki" too, and 006 keeps it verbatim.
    (r'Elder Ki: Soki,', 'Elder Ki: Sōki,'),
    (r'Here Soki is', 'Here Sōki is'),
    (r'In the Jikaishi \(Self', 'In the Jikaishū (Self'),
    (r'“rustic beauty’ or', '“rustic beauty” or'),
    (r'“far out’’;', '“far out”;'),
    (r'“little love song’:', '“little love song”:'),
    (r'the “httle love song”', 'the “little love song”'),
    (r'the “little love song’\? and', 'the “little love song” and'),
    (r'\bMa[fj]ijusri\b', 'Mañjuśri'),
    (r'Sūrangama Sutra,', 'Sūrangama Sūtra,'),
    (r'\bSarangama Sūtra\b', 'Sūrangama Sūtra'),
    (r'that is ch’ing/jo This', 'that is ch’ing/jō This'),
    (r'ing of jd in', 'ing of jō in'),
    (r'“circumstances”’ or', '“circumstances” or'),
    (r'lines as ““Making', 'lines as “Making'),
    (r'“no mind”’ describes', '“no mind” describes'),
    # pp. 137-144, poems 280-344 (spec 010, session 9), each checked on the
    # page. "too many.9" is 91: the general rule would make it [9].
    (r'Power of the Great, the final', 'Power of the Great,” the final'),
    (r'says, What is it\?', 'says, “What is it?'),
    (r'road of Heaven\.’’89\b', 'road of Heaven.” [89]'),
    (r'one body is too many\.9\b', 'one body is too many.” [91]'),
    (r'“Why, of course! Ill soon', '“Why, of course! I’ll soon'),
    (r'said to him, “Come, perch', 'said to him, ‘Come, perch'),
    (r'“Why, of course! Tm just', '‘Why, of course! I’m just'),
    (r'right\?” The perch flushed', 'right?’ The perch flushed'),
    (r'\bthen youd best\b', 'then you’d best'),
    (r'dried fish store\.’ 92\b', 'dried fish store.’” [92]'),
    (r'and on "objects to realize', 'and on “objects” to realize'),
    # pp. 145-150, poems 352-389 (spec 010, session 10), each checked on the
    # page. Hōnen is anchored on 092's own lines: the glossary-index and the
    # bibliography have "Honen" too, and 006 keeps them verbatim.
    (r'The kan “privately carriages pass\s+confuses', 'The kōan “privately carriages pass” confuses'),
    (r'Wei-shan said: ““No words', 'Wei-shan said: “No words'),
    (r'can get through\.97\b', 'can get through.” [97]'),
    (r'^Honen, I have heard', 'Hōnen, I have heard'),
    (r'^Henen\'s One-Sheet', 'Hōnen’s One-Sheet'),
    (r'Honen: \(1133-1212\) Founder of the Jodoshi,', 'Hōnen: (1133-1212) Founder of the Jōdoshū,'),
    (r'Honen’s One-Sheet Document: Contains', 'Hōnen’s One-Sheet Document: Contains'),
    (r'“Namu Amida Butsu’’', '“Namu Amida Butsu”'),
    (r'and that alonc\.', 'and that alone.'),
    (r'Tu Mu \(803- 52\)', 'Tu Mu (803-52)'),
    (r'books in your belly\.,', 'books in your belly.'),
    # pp. 143-144 and 169-170, poems 332, 647 and 690 (spec 014): the notes of
    # three of the six poems it started, re-translated with them. Each checked
    # on the page. "pupils.*Most" is a smudge in the print, not a marker.
    (r'understand this\?’’%', 'understand this?” [96]'),
    (r'sword\?\s+Rinzai said, “Misfortune, misfortune\.’ 11\b',
     'sword?’ Rinzai said, ‘Misfortune, misfortune.’” [111]'),
    (r'his foresight\.1!2', 'his foresight. [112]'),
    (r'The “Three Essentials,’ the', 'The “Three Essentials,” the'),
    (r'translated as “‘clerics’’', 'translated as “clerics”'),
    (r'\bfled to Kokyuan\b', 'fled to Kokyūan'),
    (r'went to the Shnonan at Takigi', 'went to the Shūon’an at Takigi'),
    (r'it is too late\.’ He put', 'it is too late.” He put'),
    (r'the gd “‘sobriquets’”’', 'the gō “sobriquets”'),
    (r'upon his pupils\.\*Most', 'upon his pupils. Most'),
    # Endnote digits fused to the word before them (STYLE.md §4.2): the print
    # sets a bare superscript digit and OCR welds it onto the preceding word
    # or its closing parenthesis. Bracket it -- nothing else in the book
    # writes a bracketed digit, so the form is unambiguous downstream.
    # Excludes "p.61", the one real citation with no space before its digits.
    (r'(?<!\bp)([.?])(\d{1,3})\b', r'\1 [\2]'),
    (r'\)(\d{1,3})\b', r') [\1]'),
    # ...and to a closing quote: "meaning.”11". Punctuation first, so that
    # "“1 know" -- an opening quote on a misread I -- is left alone.
    (r'([.?!,][”’"]{1,2})(\d{1,3})(?=\s|$)', r'\1 [\2]'),
    (r'\bsufh-?\s*cient\b', 'sufficient'),   # dehyphenate() joins it first
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

# Hyphenated forms the print sets whole on a line somewhere. A line-end hyphen
# in one of these is the word's own, not the typesetter's: "Master Fo-/yen"
# came out "Foyen", "Chao-/chou" "Chaochou", "Yüan-/wu" "YGanwu".
ATTESTED_HYPHENS = {h.lower() for h in re.findall(r'[A-Za-z]+-[A-Za-z]+', '\f'.join(pages))}

def join_hyphen(m):
    w1, w2 = m.group(1), m.group(2)
    if (w1.lower() in ('non', 'self', 'well', 'all', 'cross')
            or f'{w1}-{w2}'.lower() in ATTESTED_HYPHENS):
        return f'{w1}-{w2}'
    return f'{w1}{w2}'

def dehyphenate(text):
    return HYPHEN_PAT.sub(join_hyphen, text)

def strip_page_footer(page_text):
    pat = r'\n\s*\S+\s+(?:FOREWORD|PREFACE|INTRODUCTION|POEM\s+NUMBER\s+\d+|I?NOTES\s+TO\s+PAGES.*|BIBLIOGRAPHY|INDEX\s+TO\s+POEMS|GLOSSARY-INDEX|ABBREVIATIONS)\s*$'
    return re.sub(pat, '', page_text.rstrip(), flags=re.IGNORECASE)

cjk_pat = re.compile(r'[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff\uff00-\uffef]')

# Two or more all-caps tokens in a row: the OCR's failed reading of the
# Chinese column -- "ABA RE", "BRETC EER". Used by drop_column() to confirm
# that what sits right of a measured gutter really is the column.
shout_run_pat = re.compile(r'(?<![.\w])(?:\b[A-Z]{2,}\b[ ]?){2,}')

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

# Verse quoted inside a note, which parse_prose() flattens into one line.
# STYLE.md §3.3. Each is confirmed against the scan -- a general verse rule
# turns dozens of quoted kōans into fake verse (spec 010 requirement 4). A
# quote's lines, found run together, get their breaks back and a paragraph of
# their own.
VERSE_QUOTES = [
    # p. 93, poem 7: Hsü-t'ang's death poem.
    ('Eighty-five years',
     'Knowing nothing even about the Patriarchs,',
     'Rowing with my elbow, serving, going,',
     'Erasing my tracks in the Great Void. [4]'),
    # p. 101, poem 35: the Blue Cliff Record's appreciatory verse. The OCR
    # split it in two, so quotes are matched across paragraph breaks.
    ('The staff swallows up heaven and earth,',
     'In vain do you speak of running the peach blossom rapids.',
     'Those with sun-burned tails are not catching the clouds and seizing mist,',
     'Those with bleached gills, why must they lose their livers and their souls? [10]'),
    # p. 103, poem 37: the Lotus Sūtra.
    ('I am the Dharma King',
     'With respect to the Dharma acting completely at will. [13]'),
    # p. 112, poem 66: the little love song.
    ('‘She often called her maid for no reason at all,',
     'Just so that her lover would recognize her voice.’”'),
    # pp. 91-93, the notes to poems 69-71: Hsüeh-tou's tomb, kōan 96, and
    # the appreciatory verse to Yün-men's kōan. Each came out a paragraph per
    # line, or two lines run together.
    ('The Three Sovereigns and Five Emperors, what about them?',
     'His suffering lasted twenty years.',
     'It did not get collected in the Great Storehouse of Sutras.',
     'Up to now, it is scattered wildly over Breast Peak. [39]'),
    ('On Wu-t’ai mountain, clouds steam rice.',
     'Before the old Buddha Hall, the dog pisses at the sky. [40]'),
    ('On the south side, cloud; on the north side, rain,',
     'The forty-seven Saints and six Patriarchs look one another in the eye.',
     'In the land of the barbarians, a monk mounts the lectern.',
     'In the land of great T’ang, they have not yet struck the drum.',
     'Pleasure in pain, pain in pleasure.',
     'Who says gold is like dung? [41]'),
    # p. 101, poem 91: Tu Fu's "Li Chien's House".
    ('About to eat the two tasty fish,',
     'Who would look for the heaviness of other flavors? [49]'),
    # p. 104, poem 108: Ch'u Ssu-tsung in the San T'i Shih.
    ('Pines, cedars in the wind outside, disordered mountains are green.',
     'At a desk, burning incense, facing a stone screen,',
     'I remember last year, after spring rain,',
     'Swallow mud sometimes soiled The Great Mystery as I read. [52]'),
    # p. 107, poem 111: Hsü Chung-ya.
    ('She rises at dawn, fearful of the spring cold,',
     'Lightly raising the vermilion blinds, gazes at the camellia.',
     'Not a handful of willow fluff to gather.',
     'Harmonizing with the wind, it hangs above the polished balustrade. [58]'),
    # p. 111, poem 121: Lan-ts'an's own poem.
    ('I did not pay court to the emperor.',
     'What is there to envy in kings and dukes? [63]'),
    # pp. 143-144, poem 332: T'ao Yüan-ming. 009's PDF read found it run
    # together in pairs (spec 014).
    ('I built my hut beside a traveled road',
     'Yet hear no noise of passing carts and horses.',
     'You would like to know how it is done?',
     'With the mind detached, one’s place becomes remote.',
     'Picking chrysanthemums by the Eastern hedge,',
     'I catch sight of the distant southern hills:',
     'The mountain air is lovely as the sun sets',
     'And flocks of flying birds return together.',
     'In these things is a fundamental truth',
     'I would like to tell but lack the words. [95]'),
    # pp. 141-142, poem 293: Lady Pan's fan poem. Found by spec 016.
    ('To begin I cut fine silk of ch’i.',
     'White and pure as frost or snow,',
     'Shape it to make a paired-joy fan,',
     'round, round as the luminous moon,',
     'to go in and out of my lord’s breast,',
     'when lifted to stir him a gentle breeze.',
     'But always I dread the coming of autumn,',
     'cold winds that scatter the burning heart,',
     'when it will be laid away in a hamper,',
     'love and favor cut off midway. [93]'),
]

# A note's closing paragraph on the poem as a whole, set off in print by a
# blank line. build_translations() drops every blank line in a chunk, since a
# blank line is also where a page ends, so these are put back by their text:
# a blank line is kept only before one of them. Each is confirmed on its page
# (spec 016); the other blank lines in notes are page breaks, labels like
# 024's "(79" and "Pi", or a set title, and must not split.
AFTERWORDS = (
    'This poem has always been held up',                    # p. 67, poem 6
    'The intrusion of the first person pronoun',            # p. 71, poem 17
    'This same theme is taken up by',                       # p. 82, poem 46
    'There are very few important female figures',         # p. 89, poem 68
    'The opening of this set of poems invokes',             # p. 91, poem 71
    'In the first line of this poem, it is no longer',      # p. 93, poem 71
    'Overtly simple, this poem',                            # p. 96, poem 75
    'These poems occur within a group of poems',            # p. 99, poem 90
    'As duplicated in the translation',                     # p. 114, poem 130
    'This poem is the seventh in the same series',          # p. 134, poem 244
    'While the moral of the title is simple',               # p. 142, poem 293
    'For the poet, the sound of the dry leaves',            # p. 145, poem 352
    'Although considered to be doctrinally opposed',        # p. 146, poem 362
    'These are the first poems in the Crazy Cloud',         # p. 156, poem 532
    'This is one of the very few poems in the Crazy Cloud', # p. 158, poem 536
    'This poem and its afternote seem',                     # p. 161, poem 542
    'There is an entry in the Nempu which may refer',       # p. 169, poem 647
)

def split_verse_quotes(paras):
    text = '\n\n'.join(paras)
    for lines in VERSE_QUOTES:
        pat = r'\s*' + r'\s+'.join(map(re.escape, lines)) + r'\s*'
        text = re.sub(pat, lambda m: '\n\n' + '\n'.join(lines) + '\n\n', text)
    return [p for p in text.split('\n\n') if p]

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

    The old cut treated any run of three spaces past column 45 as the gutter,
    and the Introduction is set justified, so it also ate stretched word
    spacing -- 52 lines, including "his craziness" and "balancing act".

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
    # intro_page, not drop_column alone: this page was the one fetched without
    # strip_page_footer, so its running header "35    INTRODUCTION" survived
    # into the text and landed mid-sentence, the sentence having been split
    # across the page break. It is the only running header left in the book.
    p58_lines = intro_page(58).splitlines()
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
    '44': 'Yen-t’ou’s Old Sail Kōan',
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
    '110': 'Wind Bell (I)',
    '111': 'Wind Bell (II)',
    '113': 'Half a Cloud',
    '115': 'Earth House',
    '117': 'Straw Raincoat and Hat',
    '120': 'Congratulations for Yōsō (I)',
    '121': 'Congratulations for Yōsō (II)',
    '126': 'Praising P’u-hua',
    '128': 'Under One’s Feet, the Red Thread',
    '130': 'Self-Appraisal',
    # The set heading on p. 115 and the Index; this was "to Show the Assembly".
    '134': 'Three Poems to Show the Monks of My Circle (I)',
    '135': 'Three Poems to Show the Monks of My Circle (II)',
    '136': 'Three Poems to Show the Monks of My Circle (III)',
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
    '315': 'The Gentleman’s Wealth',
    '332': 'The Last Chrysanthemum in the South Garden',
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
    '537': 'Promise to Be Born in the Time of Maitreya',
    '539': 'Paper Sleeves',
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
    '690': 'Sea Cloud',
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
    '593': '593', 'wk': '771',
    # Six display numbers the OCR garbled past the rule below, so each poem --
    # title, verse, notes -- ran into the file before it. Keyed on the
    # stripped line, and each occurs once in the translation run. Every one
    # checked on its page (spec 014). Not a looser rule: get_num() would then
    # start poems on page numbers and note labels.
    '1 |': '111', 'NIS': '113', 'Bild;': '315', 'Boe': '332',
    '537,': '537', '690,': '690',
}

# Set headings: the OCR'd line, whitespace collapsed, to the printed heading.
# Matched whole, not by prefix -- a note lemma starts "The Scriptures Wipe Away
# Filth:" too, and the spaced-out OCR of "Addressed to a Monk Who Burned Books"
# never matched a prefix at all. Five never matched, so each heading
# ran into the note before it. Every one checked on the page (spec 010).
KNOWN_SETS = {
    "Hsii-t’ang’s Three Pivot Phrases": "Hsü-t’ang’s Three Pivot Phrases",
    "The Scriptures Wipe Away Filth": "The Scriptures Wipe Away Filth: three poems",
    "Living in the Mountains two poems": "Living in the Mountains: two poems",
    "Wind Bell two poems": "Wind Bell: two poems",
    "Three Poems to Show the Monks of": "Three Poems to Show the Monks of My Circle",
    "On Tiger Mount, the Snow Falls on Three": "On Tiger Mount, the Snow Falls on Three Grades of Monks: two poems",
    "Congratulating Elder Ki on the New": "Congratulating Elder Ki on the New Construction of Eagle Tail Monastery and Inquiring after His Leprosy",
    "Picture of an Arhat Reveling in a Brothel": "Picture of an Arhat Reveling in a Brothel: two poems",
    "Addressed to a Monk Who Burned Books": "Addressed to a Monk Who Burned Books: three poems",
    "The Second Year of Kansho—Starvation": "The Second Year of Kanshō—Starvation: three poems",
}

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
        # Cut the column where a gutter is measurable, and nowhere else.
        # There used to be a fallback guess -- "three spaces past column 45"
        # -- for the pages drop_column() leaves alone. Those 21 pages are
        # genuinely one-column, so every cut it made there was English: eight
        # of them, "When Nan-ch'üan saw them" among them. Spec 010, session 2.
        lines = drop_column(strip_page_footer(pages[p_idx])).splitlines()
        all_lines.extend(lines)

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
        # Poem 121's display number OCRs to a bare "2" (p. 134 of the scan).
        # This used to read `idx == 1714 or s == '2'`, and the index arm was a
        # landmine: any change upstream that shifts the line numbering makes
        # 1714 the poem's first line instead, which then takes 121 a second
        # time and trips the monotonic assertion below. Matching the text is
        # enough -- the stray "2" is the only one in the anthology run.
        if s == '2':
            return '121'
        if s in OCR_MAP:
            return OCR_MAP[s]
        if s.isdigit() and int(s) in range(1, 900):
            return s
        return None

    def is_set_header(idx, line):
        return ' '.join(line.split()) in KNOWN_SETS

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
            out.append(f"### {KNOWN_SETS[' '.join(s.split())]}\n")
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
                elif len(chunk) > 3 and "Congratulating Daiyuan" in c0:
                    t_lines = 3
                elif len(chunk) > 2 and any(k in c0 for k in [
                    "Face to Face with the Beautiful", "On the Topic", "Draw a Line", "Go to the Sea",
                    "One’s Eyes Are Not Yet", "Addressed to an Assembly", "The Great Master Yiian-wu",
                    "Chrysanthemums: An Arhat", "Living in the Mountains", "Praising the Dharma Master",
                    "A Layman Reciting", "Remorse         over", "No One Sees", "Spreading Horse Dung",
                    "A Beautiful Woman’s Dark", "Wishing to Thank", "Retreating from Mikanohara",
                    "The Last Chrysanthemum"
                ]):
                    t_lines = 2
                elif len(chunk) > 1 and any(k in c0 for k in [
                    "Praising Monk", "Straw-Sandal", "Peach Blossom", "The Buddha’s", "Pleasure in Pain",
                    "Pain in Pleasure", "Rinzai Burned", "Praising the Fish-Basket", "Frogs", "Shakuhachi",
                    "Snowball", "Instructing the Cook", "From the Mountains", "Wind Bell", "Straw Raincoat",
                    "Praising P’u-hua", "Under One’s Feet", "Self-Appraisal", "Self-A ppraisal", "On a Brothel",
                    "Addressed to a Monk in the Hall", "Addressed to a Monk at Daitokuji", "Sakyamuni Practicing",
                    "Inscription for", "Pai-chang Fasting", "Presented to a Gathering",
                    "Nirvana Hall", "Composing a Poem", "Fisherman", "Addressed to a Monk Who Killed",
                    "About Disturbances", "Thanking a Man", "Composed When Ill", "Acts of Grace",
                    "The Correct Skill", "Reducing Desires", "Taking a Metaphor", "Praising Saint",
                    "Ridiculing Literature", "Recollecting the Past", "The Stick", "Deluded Enlightenment",
                    "Lamenting Soldiers", "Hell", "1 Hate Incense", "Praising Master Rinzai",
                    "Lady Mori Rides", "Calling My Hand", "Lady Mori's Afternoon", "Night Conversation",
                    "Po Lo-t ien", "Cause and Effect", "Sonrin, Forest",
                    "Half a Cloud", "The Gentleman’s Wealth", "Promise to Be Born", "Sea Cloud"
                ]):
                    t_lines = 1
                else:
                    t_lines = 0
            
            v_lines = chunk[t_lines:]
            
            # Special handling for poems with attached notes without 'Notes:' header
            trailing_notes = []
            afternote = []
            if num in ('541', '542'):
                # Four verses, then text no item start begins: 541's notes,
                # whose "Notes" has no colon, and 542's prose afternote, whose
                # own "Notes:" comes after it. Counted in verses, not raw lines:
                # each poem wraps a verse onto an indented second line, and a
                # raw-line cut pushed verse 4 out of the stanza (spec 014).
                starts = [vi for vi, vl in enumerate(v_lines)
                          if len(vl) - len(vl.lstrip()) < 2]
                cut = starts[4] if len(starts) > 4 else len(v_lines)
                v_lines, rest = v_lines[:cut], v_lines[cut:]
                if num == '541':
                    trailing_notes = rest
                else:
                    afternote = rest
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
            
            for p in parse_prose('\n'.join(afternote)) if afternote else []:
                out.append(p + "\n")

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
            # Parse note paragraphs, keeping the blank line before an afterword
            n_lines = [lines[j] for j in range(pos+1, next_pos)
                       if lines[j].strip()
                       or (j+1 < len(lines) and lines[j+1].strip().startswith(AFTERWORDS))]
            # If the header line had text after colon
            after_colon = re.sub(r'^(?:Notes:|Note:)\s*', '', s).strip()
            if after_colon:
                n_lines = [after_colon] + n_lines
            note_paras = parse_prose('\n'.join(n_lines))
            # Unguarded: num is None on a Notes chunk, and a guard on it kept
            # the poem 7 fix dead through two specs. The quotes are guard enough.
            note_paras = split_verse_quotes(note_paras)
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
