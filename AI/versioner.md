# Versions historie af video behandling

Gennemprojektet har der været flere forskellige tilgange til at prøve at gå fra billede til kurve. De fleste har været uden succes, men en enkelt virkede i begrænset omfang. Desværre var det omfang så begrænset at det ikke gjorde en forskel for hvor brugbart programmet var.

## iteration 1, `Otte.py` og `Greenscreen.py`

For `Greenscreen.py` var konceptet simpelt, isoler nudlen ved at fjerne alle pixels der ikke var orange nok.
Programmet `Greenscreen.py` er skrevet i python og bruger bibliotekerne `CV2` og `numpy`.
Programmet kører følgende funktioner:
- `cv2.VideoCapture()` for at hente et billede fra kameraet.
- `cv2.inRange` laver et billede hvor hver pixel der er "mellem" to farver er hvide og alle pixels der ligger uden for farve rækkevidden er sorte.
- `remove_isolated_pixels()` for at fjerne små klumper af pixels fra billedet.
- `cv2.boundingRect()` som finder koordinaterne til den firkant der kan laves om billedet udfra det mest extreme x og y værdier.

Den anden fil `Otte.py` bruger samme biblioteker og har ikke yderligere funktionalitet en `Greenscreen.py`, dog var det der koordinat placering først blev implementeret og flettet ind i `Greenscreen.py`.

Programmet fungerer ved at en ottendedel af billed-inputtet og var et proof-of-concept til senere idéer.

Samfletningen blev implenteret ved at bruge metoden med at opdele billedet på et subbillede defineret af den kasse `cv2.boundingRect()` har genereret.

## iteration 2, `Greenscreen.py` og `Orangescreen.py`

I andet iteration blev koordinat placeringen forbedret, `Orangescreen.py` virkede som testgrund for de nye ændringer koordinat placering blev forbedret så vidt vi kunne se. Vi lavede flere test hvor vi visuelt inspicerede resultatet fra programmet, dog fangede vi ikke mange af de mangler der senere blev fundet i programmet. De fejl der blev fundet var, at der ikke var høj nok præcisition og at nudlen ikke kunne blive vendt på højkant.

## iteration 3, `Rotate.py`

Her ses første intruduktion af `cv2.minAreaRect()` som laver den firkant med mindst muligt areal der kan omslutte et objekt. Jeg havde overset en vigtig detalje det jeg læste dokumentationen eller misforstået den betydning, da det senere har været skyld i meget spild arbejde. Når `cv2.minAreaRect()` giver en liste af data er udfaldsrummet begrænset til 0 til -90 grader. Der giver matematisk mening men reduktionen af original dataet har mange afledte effekter på hvad man kan regne.

Programmet i store træk:
- Samme som `Greenscreen.py` optil og inkluderende `remove_isolated_pixels()`
- Derefter kører `cv2.findContours()` som laver en liste af konturer om det billeder som er angivet.
- Konturerne reduceres til ekstreme konturer: `cv2.convexHull()`
- Baseret på de ekstreme punkter finder `cv2.minAreaRect()` en firkant.

## iteration 4-5, `Rotate.py`

`Rotate.py` kunne køre men virkede ikke hensigtsmæssigt, for at fikse problemet blev der tilført nogle filtrer som gjorde det nemmere for kontur funktionen at finde kanter. Sobel filteret er en "Edge dectection" filter som gør kanter mere tydelige.

```py
sx = cv2.Sobel(absolute,cv2.CV_32F,1,0)
sy = cv2.Sobel(absolute,cv2.CV_32F,0,1)
```

Sobel filteret virkede men var ikke nok. det blev løst ved at få pixels som ikke var forbundet til at hænge sammen. Er der 5 pixels horisontalt på række forbinder den følgende kode dem med andre pixels op til 30 pixels væk.

```py
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 30))
threshed = cv2.morphologyEx(absolute, cv2.MORPH_CLOSE, rect_kernel)
```

## iteration 6-7, `Rotate.py` og `Rotate_live.py`

`Rotate.py` får en ny funktion `crop_minAreaRect()` og lavet til kode der kan køre med video i `Rotate_live.py`

## iteration 8, `Rotate.py`

En punkt rotations funktion bliver implementeret, koden var baseret på et online indslag og har flere fejl.

## iteration 9-10, ændringer på mange filer, "Stor ændring"

