# STYLE.md — the translation decisions

The decisions this book is translated under, and the reasoning for each. Written
in one session (spec 001) before any bulk translation, because revising a
register or a proper-noun policy at poem 80 means revising 79 files.

**Almost nothing here is enforced.** `bargardan-tools v0.1.0` has no
`check_glossary` and this book will never have one. What is enforced
mechanically is small and named in §5 and §6: the digit script, the quote
marks, and the structural heading labels `tools/apparatus.py` re-emits. The rest
— register, every proper noun, every Buddhist term — is a discipline a human
keeps or fails to keep. A rendering below that has not been argued out is
labelled **(suggested)** and is not binding.

Sections §1–§3 are settled and carry no open questions. §4–§6 record what is
already configured and why. Where a question has not actually come up yet, it is
left as `<<<TBD>>>` rather than guessed — a guess written now is worse than a
gap, because it looks settled.

**Spec 003 ran the first ten poems against this guide and changed three things
in it.** §4.2 and §5 were reversed outright — both asked the pipeline for
something it does not produce — and §2.9 was added for something it produces
that no section had anticipated. Each revision says where it came from. **After
spec 003 the guide is binding**; a decision that survives ten real files is not
re-opened per poem.

---

## §1 Register

The book is three books. Arntzen's Introduction is modern scholarly English with
dates, citations and institutional history. The poems are four-line Chinese
quatrains rendered compactly and formally. And a large part of the Anthology is
blunt, erotic and satirical — brothels, Lady Mori, monks shamed by name — in
that same compact form.

### §1.1 The Introduction, the Notes and the prose introductions

Modern scholarly Persian. Ordinary contemporary academic register: dates,
citations and institutional names as a Persian historian would write them. No
archaism. This is not a hard decision and nothing in the book pushes against it.

### §1.2 The verse — all 126 poems, lyric and obscene alike

**The classical Persian poetic lexicon, kept compact.** نهانگاه rather than
جای تاریک; زربفت rather than پارچهٔ طلایی; می‌گردد rather than می‌چرخد.

Two reasons, and the second is the load-bearing one:

1. **Period.** Ikkyū is 1394–1481. Hafez died around 1390. The Persian reader's
   period-voice for a fifteenth-century poet is Timurid, and a four-line Chinese
   quatrain and a Persian قطعه are close enough in shape that the classical
   register carries the form without effort.

2. **It is the register that can be obscene.** Persian's *modern* register is
   the prudish one; its classical register — Sa'di in the خبیثات, Obeyd Zakani
   throughout — is frank about the body without either flinching or
   editorialising. Choosing it means the erotic poems need no special vocabulary
   and no special handling. They are in the same voice as the rest, which is
   exactly Ikkyū's point.

**The register is not loosened or tightened per poem.** A separate contemporary
voice for the erotic poems would make them sound like a different author.

### §1.3 The test, which the decision has to survive

Spec 001 requires this decision to be tried against a deliberately obscene poem.
Note first what Arntzen is doing: she is **frank, not crude**. "dark place",
"narcissus", "thighs" are Ikkyū's own images, rendered without a wink. The
Persian matches that, and does not soften it.

`source/111.md` — Poem 535:

> A Beautiful Woman's Dark Place Has the Fragrance of a Narcissus
> …Delicately the narcissus revolves between thighs.

```
# شعر ۵۳۵: نهانگاهِ زنی زیبا بویِ نرگس دارد

...
نرگس به لطافت در میانِ ران‌ها می‌گردد.
```

`source/082.md` — Poem 284:

> With a Poem About a Brothel, Putting to Shame Those Brothers Who Obtain the Dharma
> …The young girl in the brothel wears gold brocade.

```
# شعر ۲۸۴: با شعری دربارهٔ روسپی‌خانه، در نکوهشِ آن برادرانی که دارما را می‌ستانند

...
دخترکِ روسپی‌خانه، زربفت بر تن دارد.
```

روسپی‌خانه, not the euphemism. نهانگاه and ران‌ها, not a retreat into abstraction.
**If a later poem cannot be blunt under this decision, the decision is wrong and
this section gets rewritten, not the poem.**

### §1.4 The shift is marked at the poem

A poem whose language is deliberately obscene carries a bracketed editorial line
directly under its heading:

```markdown
<!-- parity: offset +1 -->

# شعر ۵۳۵: نهانگاهِ زنی زیبا بویِ نرگس دارد

> [زبانِ این شعر عامدانه رکیک است.]

پیشگاهِ «چ’و» را باید از دور نگریست و نیز بر آن برشد.  
```

Roughly 30 of the 141 Anthology files are candidates — every file matching
brothel / Mori / lust / thigh and their neighbours. The exact set is decided
file by file as each is translated, not listed here in advance.

**Spec 003 marked none of the first ten.** Poem 6 is the near miss and it
settles where the line is: its subject is unmistakably erotic and its *language*
is not — "Cloud-rain, fūryū" is allusion, and the note explaining it runs to a
page. §1.4 marks the poem's language, never its subject, or the marker ends up
on every poem in the book and stops meaning anything.

**Spec 004 read all 28 candidates and marked two: `111.md` and `112.md`.**
That is the whole set for the Anthology, and it is a tenth of what this
section budgeted for.

- **`111.md`** — poem 535, the poem §1.4 is written around:
  `و گل نرگس، ظریف و آرام، میان ران‌ها می‌چرخد.`
- **`112.md`** — poem 536: the lady as `استادِ بازیِ عشق‌ورزی`, curing
  `ساقه‌ی جواهرنشان`.

The other 26 are all the poem 6 case, and the run of them is what shows the
line is in the right place. `055.md` is titled "On a Brothel" and its four
lines are cloud-rain and love's deep river; `078.md` is an arhat revelling in
one; `124.md` is titled "Cause and Effect for a Lustful Monk" and is four
lines of doctrine. The title names the subject, the verse is allusion, and
neither is what §1.4 marks. **Arntzen is frank far more often than she is
crude, and the marker is for the crude.**

The practical consequence: `check_parity` needs the `<!-- parity: offset +1 -->`
companion in two files, not thirty, so the cost §1.4 accepted knowingly turned
out to be small. Both were verified with all three checkers green.

**Spec 014 read poem 537 on its own terms and left it unmarked.** It had
been inside 536's file, under 536's marker, until 014 gave it a file of its
own (`113.md`). Blind Mori, mandarin ducks, the dawn of Maitreya: allusion,
the poem 6 case. File numbers in this section are 014's, which renumbered
every Anthology file after `038`.

**This is the expensive decision in this file, and the cost is accepted
knowingly:**

- The marker is a Markdown block, so `check_parity` counts it and every marked
  file needs its own `<!-- parity: offset +1 -->`. A block that is nothing but
  an HTML comment does not itself count, so the offset directive is free.
  Measured: with both in place, `check_parity --check`, `normalize --check` and
  `apparatus --check` all pass.
- **The marker is added by hand, after `restore` has written the file.** It
  cannot go in before: it changes the run structure, so
  `align_hard_breaks_by_block` would stop matching and `engine.restore` would
  refuse the draft. This is one of the two sanctioned hand-edits to `fa/`; see
  `CLAUDE.md`.
- Every marker is a small apology for the poem above it. That is the argument
  against, it was made, and it lost.

The wording above is the wording. It is not re-phrased per poem.

---

## §2 Proper nouns

The source mixes three romanisation systems on the same page, and they are not
the same kind of thing. Wade-Giles marks are **phonemic**; the Japanese macron
marks **length**. They are therefore treated differently.

### §2.1 Transliterate from Wade-Giles, never from Pinyin

`Hsü-t'ang`, not Xutang. `P'u-hua`, not Puhua. Every cross-reference, every
note and `glossary-index.md` in this book is Wade-Giles; a Persian form built
from the modern reading would not match anything a reader could look up. The
edition being translated is Arntzen's, not a modern sinological one.

### §2.2 The Wade-Giles apostrophe is carried into the Persian word

`’` (U+2019, the same character `source/` uses) goes inside the Persian word:
**ت’انگ**, **چ’و**, **پ’و-هوا**.

It is a phonemic mark, not punctuation. Dropping it silently merges distinct
names, and this book has the collisions to prove it: `Tao` (2 occurrences, the
Way) against `T'ao` (27, the poet T'ao Yüan-ming), and `Chin` (5) against
`Ch'in` (2) — two different Chinese states.

Persian has no aspiration contrast, so nothing native carries it. `’` was chosen
over the hamze-carrier form (تئانگ) because ئ adds a syllable — چئو reads as two
where `Ch'u` is one — and the mark must not change what the name sounds like.

**Mechanically verified.** `normalize`'s `quotes` rule pairs **double** quotes
only; single quotes and a word-internal `’` pass through untouched, including
inside a span the rule does rewrite:

```
نقل قولی که نامِ ت’انگ را در بر دارد: «استادِ ت’انگ چنین گفت».
```

§6 records the dependency this creates.

### §2.3 Wade-Giles `ü` is a different vowel, and is distinguished

`ü` → **یو**; plain `u` → **و**. So `Yü-wang` → یو-وانگ, `Ch'ü` → چ’یو,
`Ch'u` → چ’و.

Not an ornament: `Ch'u` (7) and `Ch'ü` (11) both occur in this book, and poem
535's own note turns on one of them.

### §2.4 The Japanese macron is not carried

`ū` and `ō` → **و**. Persian has no vowel-length contrast for a reader to hear,
and a diacritic that carries nothing is noise on a name that appears 438 times.

Every macron-only pair still left in `source/` — `Daisho`/`Daishō`,
`Honen`/`Hōnen`, `Kato`/`Katō`, `Taisho`/`Taishō` — is residual OCR damage from
spec 002, not a distinction. There is no Japanese name in this book that the
macron alone separates.

### §2.5 The Japanese syllable-boundary apostrophe is not carried

`Shūon’an`, `Sen’yūji`. That apostrophe marks a mora boundary (n + a, not na),
and the Persian hyphen already does that work: **شو-اون-آن**. Carrying both
would mark the same boundary twice.

### §2.6 Guillemets around proper nouns are tolerated, not required

`fa/002.md`'s practice is ratified: «شیو-ت’انگ», «دایتوکوجی». But the model is not
consistent about it even inside that one file, and `«»` also means a real
quotation, so the mark carries no distinction worth enforcing.

**This is the one place the book knowingly accepts variation.** Making it a rule
would mean hand-editing 153 files for a mark that changes no meaning, and the
machine draft is the edition. A name with guillemets and the same name without
are both correct.

### §2.7 Sanskrit and Buddhist vocabulary

The principle: **a settled Persian form where one exists; otherwise transliterate
from the Sanskrit, not from Arntzen's English.** Arntzen gives these terms in
Sanskrit even where Ikkyū wrote the Chinese, so the Sanskrit is what the Persian
renders — دارما, not a Persian form built from *hō* or *fǎ*.

| Source | Persian | Status |
|---|---|---|
| Zen | ذن | **argued** — the settled Persian spelling, and the corpus's other books use it. |
| Buddha | بودا | **argued** — settled. |
| Nirvana | نیروانا | **argued** — settled. |
| Sūtra | سوترا | **argued** — settled; §2.4 drops the macron. |
| Dharma | دارما | **argued** — the standard Persian form in writing on Buddhism. |
| Bodhisattva | بودیساتوا | (suggested) |
| Arhat | اَرهَت | (suggested) — no settled Persian form; transliterated from the Sanskrit. |
| Maitreya | مایتریا | (suggested) |
| Vimalakīrti | ویمالاکیرتی | (suggested) |

The four suggestions are first readings and are cheap to overrule until they are
in many files. Spec 003's ten-poem pilot is where they meet real verse; if one
does not survive, it is changed here and in the ten files, not defended.

**Spec 003: none of the four came up.** Bodhisattva, Arhat, Maitreya and
Vimalakīrti do not occur in poems 6–35. The five argued terms all did, and all
came back in the argued form unprompted — دارما, بودا, نیروانا, سوترا, ذن. The
four stay (suggested) and meet verse later.

### §2.8 The recurring renderings

Not a gate. Nothing checks this table. It is the record, and it is where a
translator looks before inventing a form.

| Source | Persian | Status |
|---|---|---|
| Ikkyū | ایک‌کیو | **argued** — the form in `pyproject.toml`'s `[tool.book.titles]`, which is the book's own table of contents. The ZWNJ marks the geminate *kk*; ایکیو loses it. |
| Hsü-t'ang | شیو-ت’انگ | **argued** — §2.2 and §2.3 together. |
| Yü-wang | یو-وانگ | **argued** — `fa/002.md`, and §2.3. |
| Daitō | دایتو | **argued** — §2.4; `fa/003.md`, the poem on him. This row used to cite `fa/002.md`, whose «دایتو» was really Daiō — spec 010. |
| Daiō | دایئو | **argued** — spec 009. §2.4, and the hiatus spelled with ئ as in کیوئونشو. Daiō Kokushi, Hsü-t'ang's student and Daitō's master: `fa/002.md`, `fa/003.md`, `fa/014.md`. **Never** «دایتو» — that was the OCR error spec 010 removed. |
| Daitokuji | دایتوکوجی | **argued** — `fa/002.md`. |
| Shūon'an | شو-اون-آن | **argued** — `fa/002.md`, and §2.5. |
| Sōjun | سوجون | (suggested) |
| Yōsō | یوسو | **argued** — spec 003, `fa/009.md`. |
| Kasō | کاسو | **argued** — spec 003, `fa/009.md`. |
| Gojō | گوجو | **argued** — spec 003, `fa/003.md`. |
| Mori | موری | (suggested) |
| kōan | کوآن | **argued** — spec 003; the model's own form in `fa/009.md` and `fa/010.md`. |
| fūryū | فوریو | **argued** — spec 003, `fa/001.md`. |
| Kyōunshū | کیوئونشو | (suggested) |

Everything marked (suggested) is a first reading, not a decision. Overruling one
costs nothing until it is in many files; after that, say so here.

The names spec 003 settled, all by §2.1–§2.5 against a model that had them
wrong. None was a judgement call; each is one of the rules above applied to a
form the translator produced by ear:

| Source | Persian | What the model gave, and which rule |
|---|---|---|
| Tz'u-ming | تز’و-مینگ | تزو-مینگ / تسو-مینگ — §2.2, and two spellings of one man |
| Yang-ch'i | یانگ-چ’ی | یانگ-چی — §2.2 |
| Ch'ü Yüan | چ’یو یوآن | چو یوآن — §2.2 **and** §2.3, both dropped |
| Ch'en | چ’ن | چِن — §2.2 |
| T'ien-che | ت’ین-چه | تی‌ین-چِه — §2.2 |
| Yün-men | یون-من | یون‌من / یون‌مِن — the source hyphenates; a ZWNJ is not a hyphen |
| Pai-chang | پای-چانگ | پای‌چانگ — same |
| Yüeh Küang | یوئه کوانگ | یوئه گوانگ — §2.1: `Kuang` is Wade-Giles, `Guang` is the Pinyin reading. The print spells it `Küang` (p. 97 and the glossary; spec 010 restored it), but Wade-Giles has no *küang* syllable, so §2.3 has no ü to carry and the Persian stays کوانگ — spec 011 |
| Tetto Ryōzen | تتو ریوزن | تِتّو / تِتو / تِتّد, three forms in one file — §2.4 |
| Chao-chou | چائو-چو | correct as given |
| Lan-ts’an | لان-تس’ان | **corrected by spec 010, session 5.** This row used to read `Lan-tsan` → لان-تسان, «correct as given». The book's form is `Lan-ts’an` (glossary-index; Introduction pp. 51–52; poem 121's note), and `Lan-tsan` was the OCR dropping the apostrophe. §2.2, as Ts’ao-shan. p. 66 prints `Lan-t’san` twice, for `001.md`: the book's own slip, not a second name, and the Persian does not follow it |

**89 corrections in ten files** — about nine per file, so of the order of 1,200
across the book. §2 is not a formality: it is the largest single hand-edit this
translation makes, and it is the reason `CLAUDE.md` sanctions the edit at all.

Spec 004 adds to the same record as it works through the Anthology. Same
principle: each is one of §2.1–§2.5 applied to a form the model produced by
ear, and none is a judgement call.

| Source | Persian | What the model gave, and which rule |
|---|---|---|
| Nan-ch’üan | نان-چ’یوآن | نان-چوآن — §2.2 **and** §2.3, both dropped |
| Yen-t’ou | ین-ت’و | یِن-تو — §2.2 |
| Ts’ao-shan | تس’او-شان | تساو-شان — §2.2 |
| Ch’ing-yüan | چ’ینگ-یوآن | چینگ‌یوان — §2.2 and §2.3; the source hyphenates |
| Ch’an-lin | چ’ان-لین | چان‌لین — §2.2; a ZWNJ is not a hyphen |
| Yüan-wu | یوآن-وو | یوان-وو — §2.3 |
| Huang-po | هوانگ-پو | correct as given |
| Pai-chang | پای-چانگ | correct as given here, unlike in the pilot |
| Ta-sui | تا-سوئی | correct as given |
| Fo-yen | فو-ین | correct as given |
| Wu-tsu | وو-تسو | correct as given |
| Rinzai | رینزای | correct as given |
| Hsüeh-tou | شیوئه-تو | شوئه-تو — §2.3, as `Yüeh` → یوئه |
| Kung-sun | کونگ-سون | کونگ‌سون — a ZWNJ is not a hyphen |
| Shao-lin | شائو-لین | شائولین — the source hyphenates |
| Shih-shih Chi-ku Lüeh | شی-شی چی-کو لیوئه | شی‌شی چی‌کو لیوِه — §2.3, and two ZWNJs for two hyphens |
| T’ien-pao | ت’ین-پائو | تی‌ین‌بائو — §2.2, and §2.1: `p` is پ, as in Pai-chang |
| Shen I-ch’i | شن ای-چ’ی | شن یی‌چی — §2.2 |
| Kuei-fei | کوئی-فی | یانگ گوئی‌فی — §2.1: `Kuei` is Wade-Giles, `Gui` is Pinyin |
| Pi-yang | پی-یانگ | پی‌یانگ — a ZWNJ is not a hyphen |
| Crazy Cloud | ابر دیوانه | «کریزی کلاود» — **not a transliteration.** Ikkyū's sobriquet, and the book's own title already renders it |
| Kuei-tsung | کوئی-تسونگ | کوی-تسونگ — §2.1, as Kuei-fei |
| Te-shan | ته-شان | تِه‌شان / تِ-شان / ته‌شان, three spellings — the kasre goes, and the source hyphenates |
| Ch’u Ssu-tsung | چ’و سو-تسونگ | چو سو-تسونگ — §2.2 |
| P’u-hua | پ’و-هوا | پو-هوآ / پو-هوا in one file — §2.2, the form §2.2 itself cites |
| Hui-neng | هویی-ننگ | هویی-نِنگ — the kasre goes |
| Hsü Chung-ya | شیو چونگ-یا | شو چونگ-یا — §2.3 |
| Ch’uan Teng Lu | چ’وآن تنگ لو | چوآن‌تِنگ‌لو — §2.2; the source spaces the three words |
| Wen-chün | ون-چیون | وِن-چون — §2.3 |
| Wen Hsüan | ون شیوآن | وِن شوئن — §2.3 |
| Tzu-hsü | تزو-شیو | تزو-شو / تزو-هسو — §2.3 |
| Te-tsung | ته-تسونگ | تِه-تسونگ — the kasre goes |
| Sung-yüan | سونگ-یوآن | سونگ-یوان / سونگ‌یوان — §2.3 |
| Yüan-t’ung | یوآن-ت’ونگ | یوان-تونگ — §2.2 and §2.3 |
| Wu-k’u | وو-ک’و | وو-کو — §2.2 |
| Fa-hsiang | فا-شیانگ | فا-هسیانگ — `hs` is ش everywhere else in this table |
| Hsüan-tsang | شیوآن-تسانگ | هسوآن-تسانگ — §2.3 |
| K’uei-chi | ک’وئی-چی | کویی-چی, nine times in one poem — §2.2 and §2.1 |
| Tz’u-en | تز’و-ان | تزو-اِن / تزو-ان — §2.2, as Tz'u-ming |
| Ts’ung-lin | تس’ونگ-لین | تسونگ-لین — §2.2 |
| Sheng-shih | شنگ-شی | شِنگ-شی — the kasre goes |
| P’u-chou | پ’و-چو | پو-چو / پو-جو — §2.2 |
| Ch’ing-su | چ’ینگ-سو | چینگ‌سو — §2.2; the source hyphenates |
| Hsü Ch’uan Teng Lu | شیو چ’وآن تنگ لو | شو چوان تنگ لو — §2.2 and §2.3 |
| Wu Teng Hui Yüan | وو تنگ هوی یوآن | وو تِنگ هوی یوآن — the kasre goes |
| Ch’ang-hsin | چ’انگ-شین | چانگ‌شین — §2.2; the source hyphenates |
| Chuang Chou, Chuang Tzu | چوانگ چو, چوانگ تزو | چوانگ‌چو / چوانگ‌تزو — the source spaces them |
| Hsü-t’ang Lu | شیو-ت’انگ لو | شیو-ت’انگ‌لو — the source spaces the title off the name |
| Yüan-ming | یوآن-مینگ | یوان‌مینگ — §2.3; the source hyphenates |
| Yang-shan, Wei-shan | یانگ-شان, وی-شان | یانگ‌شان / وی‌شان — a ZWNJ is not a hyphen |
| Hōnen | هونن | هونِن — §2.4, and the kasre goes |
| Shih-huang | شی-هوانگ | شی‌هوانگ — a ZWNJ is not a hyphen |
| Ch’u | چ’و | «چو», of Ch'u's Pavilion — §2.2, the form §2.2 itself cites |
| Po Chü-i | پو چیو-ای | پو چو-یی / بو چویی — §2.3, and §2.1: `P` is پ |
| Hsüan-tsung | شیوآن-تسونگ | شوان-تسونگ — §2.3. A different man from Hsüan-tsang above; §2.3 is what keeps them apart |
| Yüan-che | یوآن-چه | یوان-چِه / یوان-چه — §2.3 |
| Li-yüan | لی-یوآن | لی-یوان — §2.3 |
| Lo-t’ien | لو-ت’ین | لو-تین — §2.2 |
| Sen’yūji | سن-یو-جی | سن‌یو-جی — §2.5: the hyphen already marks the mora boundary |
| Ch’ang-an, Ch’ang-lo | چ’انگ-آن, چ’انگ-لو | چانگ‌آن / چانگ‌لو — §2.2; the source hyphenates |
| Fu-chou | فو-چو | فو-جو — Wade-Giles `ch` is چ, as in Chao-chou |
| Tien-tai | تین-تای | تیِن-تای — the kasre goes. The source spells it without the apostrophe and the Persian does not invent one |
| Feng-yüeh | فنگ-یوئه | فِنگ-یوئه — the kasre goes |
| Maitreya | مایتریا | مایتریه — §2.7's recorded form, promoted here because `113.md` is where it finally met verse |
| Jui-yen, Wu-men, Tung-po, Shan-ku, Tu-ling, Tou-shuai, Ta-kuan, Ku-yin, Chiang-hu, Po-yün, Yao-shan, Ku-tsun-su Yü-lu | — | correct as given |

**Three things this table is evidence for.** The model's commonest error is not
a spelling but a *separator*: a ZWNJ where the source has a hyphen, or a hyphen
where it has a space. It is inconsistent within one file — P'u-hua twice in
`039.md`, Te-shan in four spellings across the book, K'uei-chi nine times wrong
in a five-line poem. And §2.3 is doing real work: `Hsüan-tsang` and
`Hsüan-tsung` are two different men, and without the ü rule the model's forms
for them collide.

Spec 011 adds three that spec 004 let through: the old files had the model's
form, so the conform, which compares a new draft against the old file, could
not see them until a re-read did.

| Source | Persian | What the model gave, and which rule |
|---|---|---|
| P’ang | پ’انگ | پانگ, ten times in `028.md` — §2.2, as P'u-hua |
| Ch’üan | چ’یوآن | چوآن — §2.2 and §2.3, as Nan-ch'üan. P'ang's interlocutor in `028.md`, not the *Ch'uan* of *Ch'uan Teng Lu* |
| Ma Yüan | ما یوآن | ما یوان — §2.3, as Yüan-wu |

Spec 013 adds five. The first four had a settled form in other files that the
new drafts missed; the last is a name the model supplied itself.

| Source | Persian | What the model gave, and which rule |
|---|---|---|
| Tu Fu | تو فو | دو فو — §2.1: `T` is ت; `Du` is the Pinyin reading. 36 occurrences already have تو فو |
| Ssu-ma Hsiang-ju | سو-ما شیانگ-جو | سوما شیانگ‌جو — the source hyphenates |
| San T’i Shih | سان ت’ی شی | سان تی شی — §2.2 |
| Shōen | شوئن | شوین / شوئِن — §2.4, the hiatus spelled with ئ as in دایئو, and the kasre goes |
| T’ai Hsüan Ching | ت’ای شیوآن چینگ | تای‌شوآن‌جینگ — §2.1, built from the Pinyin *Taixuanjing*. Not in `source/`: the model added it with its own gloss in `037.md`. The Persian is conformed and the gloss is kept (§2.9) |

Spec 015 adds two, both from the fifth decade's restored source.

| Source | Persian | What the model gave, and which rule |
|---|---|---|
| Daiki Kōjū Zenji | دایکی کوجو زنجی | دایکی کوجو زِنجی — §2.4, and the kasre goes. The old file had «کوجا», from the OCR's `Koja` |
| Kasō Sōdon | کاسو سودون | correct as given. The old file had «سدون», from the OCR's `Sddon` |

Spec 016 adds one.

| Source | Persian | What the model gave, and which rule |
|---|---|---|
| Chien-ho | چین-هو | چیِن-هو / چیِن‌هو — the kasre goes, and the source hyphenates. The marquis in `086`'s Chuang Tzu story |

---

### §2.9 The translator's parenthetical romanisations are kept

**Added in spec 003.** The Advanced model volunteers a Latin-script gloss after
a name or a term the first time it meets it, and sometimes after that:

```
«ایک‌کیو» (Ikkyū) پیوندی عمیق با شیو-ت’انگ احساس می‌کرد
معادل اصطلاح «کوآن» (kōan) است
نسخه‌های خطیِ متعددِ «مجموعهٔ ابر دیوانه» (Crazy Cloud Anthology)
```

None of these is in `source/`. They are additions, and they are kept.

29 of them in the ten pilot files, so of the order of 350 across the book.
Stripping them would be 350 hand-edits of a kind `CLAUDE.md` does not sanction,
for something that is not wrong. And they earn their place: §2.1's whole
argument is that the reader must be able to find a name again in Arntzen's
index, and a romanisation in the margin of the sentence does that better than a
transliteration the reader has to reverse-engineer.

Two things are knowingly accepted with them:

- **They are not consistent.** The same name is glossed in one file and bare in
  the next, and the gloss appears on ordinary English headwords too —
  `(Situation)`, `(The Beautiful One)`, `(Patriarchs)` — not only on names.
  That is the same variation §2.6 already accepts, for the same reason.
- **The gloss may not spell the name the way `source/` does.** `Shūon’an`
  comes back as `(Shūon-an)`. It is the model's gloss, not a quotation, and it
  is not corrected; the Persian form beside it is the one §2.5 governs.

**A gloss is Latin script inside a Persian paragraph, so it is a bidi
hazard.** This is the specific thing spec 003 requirement 7 sends you to the
PDF for. It renders correctly under LuaLaTeX — checked on all ten — and would
not under XeLaTeX. `tex/preamble.tex` has the reasoning; §2.9 is now a second
reason not to switch engines.

## §3 Verse layout

### §3.1 One source line is one Persian line. A translator does not re-break.

The hard line breaks *are* the poem: `apparatus.py` restores them mechanically
and `apparatus --check` fails if a file loses one. The style rule is the part
the mechanism does not decide, and it is **no re-breaking** — a quatrain is four
lines in `fa/` because it is four lines in `source/`.

### §3.2 A Persian line that overruns the measure is a typesetting problem

A Persian line is typically longer than Arntzen's English line, so a four-line
quatrain can wrap to eight in the PDF and read as eight. **That is fixed once in
`tex/preamble.tex`, not 141 times in the text** — verse gets a hanging indent, so
a continuation is visibly a continuation and not a new line.

The preamble currently has no verse handling at all; adding it is spec 007's
work. Until it lands, the wrapping is a known cosmetic fault in the PDF and is
not to be worked around by shortening lines.

### §3.3 A poem quoted inside a prose note is set however `source/` sets it

Not a style decision — a source-repair one, and it is not this spec's to make.

`fa/002.md` has the case: Hsü-t'ang's death poem inside the notes. `source/`
runs it together into one prose line, the model re-broke it into three, and
`align_hard_breaks_by_block` correctly skipped that run and repaired the stanza
above it. **But the re-break has no effect on the page.** Soft newlines reflow,
so the typeset PDF sets the death poem as one prose paragraph — verified by
rendering, not by reading the Markdown.

It cannot be fixed in `fa/`. `apparatus --check` requires
`hard_breaks(fa) == hard_breaks(source)` exactly, so adding the two trailing
spaces that would hold the stanza together makes `just check` fail. The check is
right: `fa/` may not have verse that `source/` does not.

**The defect is in `source/`.** The print edition sets this as a verse
quotation, and the notes extraction flattened it — the line-initial capitals are
still visible in the run-together text (`years Knowing nothing`,
`going, Erasing`). Repairing it belongs to spec 002, which fixes
`generate_final_markdown.py` and re-splits. Until then, the death poem is prose
on the page, and that is recorded here so nobody patches `fa/002.md` instead.

---

## §4 Notes

### §4.1 The run-on form is kept

**The run-on form is kept.** 97 of the 141 Anthology files carry a `## Notes`
section of glosses run together into one paragraph — headword, colon,
explanation, then the next headword. Persian keeps them in one paragraph.

The reason is arithmetic, not taste. Breaking to one gloss per line changes the
block count, so each of those 93 files would need a `<!-- parity: offset +N -->`
where N differs per file and has to be recounted whenever a note is edited. A
checker that needs a hand-maintained offset in 93 files is a checker that gets
turned off by attrition. §1.4 already spends about 30 offsets on something that
earns them; this would spend 93 on typography.

`<<<TBD>>>` — whether a headword should be emphasised within the run-on
paragraph. Not decided, because no file has yet made it a problem.

### §4.2 Endnote markers

Spec 002 deferred this one here, so it is answered here. 155 endnote digits in
`source/` are fused to the word before them — `Onin War.1`, `dung ?42`,
`Great Void.4 Yü-wang:` — which also welds a note's last word to the next
gloss's headword.

**The form is `[N]`, bracketed, preceded by a space:** `Great Void. [4]`. That
is already the shape two entries in spec 002's typo dictionary use by hand
(`impoverishcd.4` → `impoverished [4]`), and brackets are what make the fix
safely mechanical — a bare digit cannot be told from `p.117` or `no. 999`, but
nothing else in this book writes `[4]`.

**In `fa/` the digits stay Latin: `[4]`. Revised in spec 003** — this section
used to require `[۴]`, on the reasoning that an endnote marker points into this
book's own back matter and so takes the book's own digit script. The reasoning
was sound and the pilot overruled it anyway, because the bracket is what makes
the marker survive the round-trip at all. The Advanced model persianises every
numeral it meets in running prose and leaves every bracketed one untouched —
5 occurrences out of 5 across the ten pilot files, with no exception either
way. `[۴]` could only be produced by hand, in roughly 70 files, on every
re-run.

The bracket also does the job the old rule wanted from the digit script. `[4]`
in a Persian paragraph is visibly not prose, which is what an anchor should be.

Two consequences, both binding on other specs:

- Spec 002 does the un-fusing in `generate_final_markdown.py`. It is a one-rule
  change now that the target form is fixed, and **it is not finished**: spec
  003 found `’’8` in `source/009.md` and `s210` in `source/010.md` still fused.
  An unbracketed digit is prose to the model, so both reach `fa/` persianised
  and unmarked, which is precisely the failure the bracket exists to prevent.
  Spec 008's to fix.
- Spec 006 renders `notes.md`'s own entry numbers in **Latin** digits to match.
  **The marker and the entry it points at change together or not at all** — a
  `[4]` that leads to an entry numbered `۴` is as wrong as the reverse.

`<<<TBD>>>` — whether the marker becomes a live cross-reference link in the
HTML build. That is spec 006's to answer; this book's endnotes are referenced
by page number and may not want one.

---

## §5 Digits

**Revised in spec 003.** The first bullet used to say the opposite of what it
says now; the pilot contradicted it on every occurrence in ten files, and the
rule is now what the pipeline actually produces. §5.1 is why.

- **A numeral in running prose is Persian.** Dates, page references into
  Arntzen's edition, poem and kōan cross-references, scroll and roll numbers:
  ۰–۹ throughout. `latin_digits = false` stays set, but it is not what makes
  this true — it means *do not rewrite digits in either direction*, and it
  never produced a Latin digit in the first place.
- **A bracketed numeral stays Latin: `[4]`.** That is the endnote marker, and
  §4.2 is where it is argued.
- **Persian digits in the book's own structure.** `[tool.book.titles]` headings
  and the `شعر N:` / `تصویر N:` labels `apparatus.py` emits use ۰–۹, because
  that is the book's own furniture rather than a reference into someone else's.

The third bullet is the one piece of terminology in the whole project that *is*
enforced, and only because `apparatus.py` generates it rather than a human
typing it.

### §5.1 Why the old rule lost

It asked for something no part of the toolchain can deliver. The old first
bullet kept poem numbers, dates and page references Latin, so that "a reader
checking `pp. 16-17` against the printed book needs to find `pp. 16-17`".

Measured across the ten pilot files: the Advanced model persianised *every*
numeral in prose — `(1185-1269)` → `(۱۱۸۵-۱۲۶۹)`, `pp. 16-17` → `صفحات ۱۶-۱۷`,
`roll 43` → `طومار ۴۳`, `kōan no. 60` → `کوآن شماره ۶۰` — without exception,
and identically on every re-run. `normalize` does not convert in the
Persian→Latin direction and no checker would catch a drift, so the old rule
could only have been kept by hand, in about 130 files, against a translator
that undoes it on every re-run. That is not a discipline anyone keeps; it is a
rule that would have been quietly false within a month.

What is actually lost is small. `صفحات ۱۶-۱۷` is not an obstacle to a Persian
reader, who reads ۱۶ as sixteen without effort. The one numeral that really
must match a Latin string verbatim is the endnote marker — and that is exactly
the one the model already leaves alone.

---

## §6 Quotes

**`quotes = true` stays on.** ASCII and curly double quotes become `«»`.

Two things follow from how the rule actually behaves, both measured:

1. **It pairs double quotes only.** Single quotes and a word-internal `’` are
   left alone. §2.2's aspiration mark depends on this. If the rule ever gains
   single-quote handling, every Wade-Giles name in the book breaks at once —
   that is the upgrade to watch for when `bargardan-tools` is unpinned.

2. **It is script-blind.** It rewrites quotes anywhere, including inside
   verbatim English. Spec 006 needs `<!-- normalize: off -->` regions in the
   back matter for exactly this, and solves it that way rather than by turning
   the rule off, because the rule is right for the other 142 files.

`harakat = "preserve"` also stays on: ezafe diacritics carry meaning in verse
and the Advanced model produces them (`چشمِ حقیقی`, `استادِ یو-وانگ`). They are
not stripped.

`<<<TBD>>>` — nested quotation inside a `«»` span. Has not come up.
