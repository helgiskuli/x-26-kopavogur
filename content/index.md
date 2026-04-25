# Verification audit — `index.html`

Síðast yfirfarið: 2026-04-25. Þetta er lesúttekt; `index.html`, CSS og sýnilegt efni voru ekki breytt.

## Samantekt

- Heildarfjöldi claim-recorda í `data/claims.index.seed.json`: 106
- `verified`: 23
- `partially_verified`: 23
- `needs_source` + `needs_primary_source`: 23
- `needs_calculation`: 2
- `should_be_marked_analysis`: 19
- Önnur áhætta: 15 tímaháð atriði, 1 atriði sem þarf mýkra orðalag

## Forgangsatriði fyrir birtingu

1. Skipta almennri footer-heimild út fyrir rekjanlegar heimildir per fullyrðingu eða source-id kerfi.
2. Staðfesta beinar tilvitnanir í frumheimildum: Orri/DV, Einar/Mbl., Jónas, Pétur og Framsóknar-tilvitnun.
3. Merkja allar niðurstöður um „átakalínur“, „tómarúm“, „lykilstöðu“ og hægri/vinstri stöðu sem greiningu höfundar.
4. Endurreikna eða endurmerkja „−3 ma.“ sem bókun minnihluta + útreikning höfundar; ekki sem opinbera fjármálatölu.
5. Endurskoða stefnuskrártöfluna sama dag og birt er, þar sem hún er tímaháð.
6. Fyrir Borgarlínu þarf eina afstöðusönnun per flokk; annars á samantektin að vera `partially_verified`.

## Heimildastig

- Opinberar staðreyndir: þurfa Kópavog, Ísland.is/Landskjörstjórn, Borgarlínuna, Betri samgöngur, ASHB eða opinber fjárhagsgögn.
- Framboðslistar: opinber auglýsing Kópavogsbæjar er sterkari heimild en flokksíður.
- Flokksafstaða: þarf formlega flokksíðu, frambjóðendagrein eða staðfesta flokksyfirlýsingu; fjölmiðlaviðtal er ekki sama heimildastig.
- Bein tilvitnun: þarf upprunalega grein, viðtal eða flokkspóst; annars `needs_primary_source`.
- Greining höfundar: þarf ekki ytri heimild sem staðreynd, en verður að vera merkt sem greining.
- Tímaháð atriði: allt sem byggir á „staðan 23. apríl 2026“ þarf endurskoðun fyrir birtingu.

## Opinberar grunnheimildir

- Kópavogur — sveitarstjórnarkosningar 2026: `https://www.kopavogur.is/is/stjornsysla/sveitarstjornarkosningar-2026`
- Kópavogur — framboðslistar 2026: `https://www.kopavogur.is/is/frettir-tilkynningar/frambodslistar-2026`
- Kópavogur — auglýsing um framboðslista PDF: `https://www.kopavogur.is/static/files/Kosningar/2026_sveitarstjornarkosningar/auglysing-um-frambodslista-2026.pdf`
- Ísland.is/Landskjörstjórn — sveitarstjórnarkosningar 2026: `https://island.is/v/sveitarstjornarkosningar-2026`
- Kópavogur — sex tíma gjaldfrjáls leikskóli: `https://www.kopavogur.is/is/frettir-tilkynningar/sex-tima-gjaldfrjals-leikskoli-og-aukinn-sveigjanleiki`
- Kópavogur — gjaldskrá leikskóla 2026: `https://www.kopavogur.is/is/ibuar/0-til-6-ara/leikskolar`
- Borgarlínan — Fossvogsbrú: `https://www.borgarlinan.is/framkvaemdir/fossvogsbru`
- Borgarlínan — frumdragaskýrsla 1. lotu: `https://www.borgarlinan.is/utgefid-efni/skyrslur/frumdragaskyrsla`
- Fjárhagsgögn: `data/fjarhagsgogn/` og úrvinnsla í `fjarmal.html`

## Page header

Claim-records: `idx-001`–`idx-007`.

- Staðfest: sjö framboð, kjördagur 16. maí 2026 og samanburður við átta lista árið 2022.
- Þarf aðgreiningu: „stærstu átakalínurnar“ er greining höfundar, ekki staðreynd.
- Þarf betri heimild: „byggir á heimasíðum flokkanna, fréttum og viðtölum“ er of almenn heimildalýsing.
- Tímaháð: „Apríl 2026“ og heimildastaða þurfa dagsetta skoðun.

## Framboðslistarnir

Claim-records: `idx-008`–`idx-024`.

- Staðfest með opinberum framboðslista: B, C, D, J, M, S og V og oddvitar þeirra.
- Staðfest með samanburði við opinbera lista: Píratar, Vinir Kópavogs og Flokkur fólksins eru ekki á framboðslista 2026.
- Þarf heimild: núverandi D+B-meirihluti á að fá opinbera heimild úr bæjarstjórn/málefnasamningi.
- Þarf frumheimild: fullyrðing um að samstarf VG og Fyrir Kópavog hafi liðast í sundur 31. mars.
- Hluta-staðfest: „engir nýir íbúalistar komu í staðinn“ er ályktun út frá opinberum listum og þarf þannig að vera merkt.
- Greining: „Sósíalistar fylla tómarúm vinstra megin“ og „Miðflokkurinn hægra megin“ eru analysis-conclusions.

## Leikskólakerfið — Kópavogsmódelið

Claim-records: `idx-025`–`idx-056`.

- Staðfest opinbert baseline: innleiðing haustið 2023, sex tímar/30 klst. gjaldfrjálst og hvatar til styttri dvalar.
- Þarf aðskilnað: opinber baseline-gögn mega ekki blandast saman við meirihlutaframinguna um árangur.
- Tilvitnanir: Ásdís/Vísir og Einar/Vísir eru rekjanlegri en Orri/DV; Orri þarf frumheimild áður en hann er birtur sem bein tilvitnun.
- Flokksafstaða: D og B eru `partially_verified`; S er betur studd; C, V og J þurfa skýrari flokksheimildir.
- Núverandi „Heimild vantar“ við S/C/V/J er rétt source-status, en ekki endanleg heimild.
- Mýkja þarf PISA-fullyrðingu Miðflokksins eða vísa í nákvæm próf/gögn.
- Tímaháð: fullyrðingar um óbirta/fullbirta stefnuskrá þurfa endurskoðun við birtingu.

## Borgarlínan og samgöngusáttmálinn

Claim-records: `idx-057`–`idx-071`.

- Staðfest opinbert: Fossvogsbrú/Hamraborg er hluti af fyrstu lotu Borgarlínu.
- Aðeins hluta-staðfest: „fimm flokkar styðja“ og „Miðflokkurinn einn á móti“ þurfa eina heimild per flokk.
- Þarf heimildir: Framsókn, Viðreisn og VG hafa ekki nægilega skýrar heimildir í auditinu fyrir stuðningi við sáttmálann.
- Þarf frumheimild: Mbl.-tilvitnun Einars Jóhannesar frá 14. október 2025.
- Þarf aðskilnað: Arnarnesvegur, Reykjanesbraut í stokk, slökkvistöð og viðbragðstímar eru fjögur ólík heimildaatriði.
- Tímaháð: „J hefur ekki birt sérstaka samgöngustefnu“ og sambærileg staða þarf endurskoðun.

## Rekstur og sjálfbærni bæjarins

Claim-records: `idx-072`–`idx-088`.

- Staðfest með fjárhagsgögnum: fasteignaskattur A-flokks lækkaði yfir kjörtímabilið, 0,151% er í áætlun 2026 og útsvar er 14,93%.
- Þarf útreikning: „−3 ma.“ var ekki endurbyggt sem hrein opinber tala; það á að merkja sem minority framing + author calculation nema full bókun og reikniregla finnist.
- Þarf útreikning: „um einn milljarður“ í fasteignaskattslækkunum þarf að sýna stofn, ár og samanburð.
- Þarf frumheimild: bókun minnihlutans um ósjálfbæran rekstur án lóðasölu.
- Þarf heimildir: tilvitnanir Jónasar og Péturs, fullyrðing um bæjarstjóramódel og Framsóknarorðalag.
- Greining: „lykilspurning“ og skil milli meirihluta/minnihluta eru analysis-conclusions.

## Aðgengi að stefnuskrám

Claim-records: `idx-089`–`idx-097`.

Staðan er tímaháð og á ekki að birta sem föst staðreynd án skoðunardags. Flokkun í auditinu:

| Flokkur | Flokkun | Staða |
| --- | --- | --- |
| Framsókn | candidate articles only / local page | `stale_or_time_sensitive` |
| Viðreisn | local issue page / candidate articles only | `stale_or_time_sensitive` |
| Sjálfstæðisflokkur | local issue page | `needs_source` fyrir „í vinnslu“ |
| Sósíalistar | local issue page / candidate content | `stale_or_time_sensitive` |
| Miðflokkurinn | national/general party page + local content | `partially_verified` |
| Samfylkingin | local issue page / candidate articles only | `partially_verified` |
| VG og óháð | national/general party page / unclear local page | `partially_verified` |

## Niðurstaðan í hnotskurn

Claim-records: `idx-098`–`idx-105`.

- Staðfest: Píratar, Vinir Kópavogs og Flokkur fólksins eru ekki á opinberum framboðslista.
- Þarf frumheimild: fullyrðing um VG/Fyrir Kópavog samstarf.
- Greining: „baráttan snýst um árangur D+B“, „veiking frjálslyndra afla“, „Viðreisn gæti haft lykilstöðu“ og áhrif 3 ma. frásagnar eru ekki staðreyndir.
- Tímaháð: Viðreisn-stefnuskrárstaða þarf endurskoðun fyrir birtingu.

## Footer

Claim-record: `idx-106`.

- Núverandi footer-heimild er of almenn fyrir síðu með beinum tilvitnunum, talnagögnum, opinberum staðreyndum og pólitískri greiningu.
- Ráðlegging: nota sýnilegan heimildakafla eða source-id tengingu við hverja fullyrðingu áður en homepage er endurskrifuð.
