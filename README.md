## Descrizione della sfida 🪐

_(Disclaimer: questa sezione iniziale è puramente flavuor ed era stata usata per la sfida "Hackapizza". Leggere la sezione successiva per avere tutto il necessario per completare il test tecnico)_

**Benvenuti** nel **Ciclo Cosmico 789**, dove l'umanità ha superato non solo i confini del proprio sistema solare, ma anche quelli delle dimensioni conosciute. In questo vasto intreccio di realtà e culture, la gastronomia si è evoluta in un'arte che trascende spazio e tempo. 

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F6840884%2Fd4cd3a9d619dec67942e5344dcacf9e4%2F9gw32h.gif?generation=1737047022355670&alt=media)

Ristoranti di ogni tipo arricchiscono il tessuto stesso del multiverso: dai sushi bar di **Pandora** che servono prelibati sashimi di **Magikarp** e ravioli al **Vaporeon**, alle taverne di **Tatooine** dove l’**Erba Pipa** viene utilizzata per insaporire piatti prelibati, fino ai moderni locali dove lo **Slurm** compone salse dai sapori contrastanti - l'universo gastronomico è vasto e pieno di sorprese.

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F6840884%2F888315aac2d2bdd249e8df8fc79f8043%2Fimage.png?generation=1737046855158236&alt=media)

L'espansione galattica ha portato con sé nuove responsabilità. La **Federazione Galattica** monitora attentamente ogni ingrediente, tecnica di preparazione e certificazione necessaria per garantire che il cibo servito sia sicuro per tutte le specie senzienti. Gli **chef** devono destreggiarsi tra regolamenti complessi, gestire ingredienti esotici che esistono simultaneamente in più stati quantici e rispettare le restrizioni alimentari di centinaia di specie provenienti da ogni angolo del **multiverso**.

Nel cuore pulsante di questo arcipelago cosmico di sapori, si erge un elemento di proporzioni titaniche, un'entità che trascende la mera materialità culinaria: la **Pizza Cosmica**. Si narra che la sua mozzarella sia stata ricavata dalla **Via Lattea** stessa e che, per cuocerla, sia stato necessario il calore di tre soli. Nessuno conosce le sue origini e culti religiosi hanno fondato la loro fede attorno al suo mistero.

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F6840884%2F0c07b3e6f34ac48b9bb627387ce71531%2FTesto%20del%20paragrafo%20(1).png?generation=1737047186767633&alt=media)

***Che la forza sia con voi.***

## Test Tecnico 

### Specifiche tecniche 💻

Ti sarà richiesto di creare una repository Github che contenga il codice per risolvere in maniera parziale o totale la sfida di Hackapizza.

Il sistema GenAI che creerai dovrà essere in grado di rispondere alle domande presenti in questo [csv](./dataset/domande.csv). Le domande sono ordinate per difficoltà e per tipologia.

Le domande sono in linguaggio naturale ma hanno come risposta univoca una lista di piatti. Ad esempio, la prima domanda "Quali sono i piatti che includono le Chocobo Wings come ingrediente?", ha come risposta \["Galassia di Sapori: Il Viaggio Senza Tempo"\], mentre la domanda 10 "Quali piatti eterei sono preparati usando sia la Cottura Olografica Quantum Fluttuante che la Decostruzione Interdimensionale Lovecraftiana?" ha come risposta i piatti \["Risotto dei Multiversi", "La Mucca Che Stordisce l'Universo", "Sogni di Abisso Cosmico"\]


### Descrizione Knowledge Base 📋

Dentro la cartella [knowledge_base](./dataset/knowledge_base), ci sono tutti i file necessari per l'applicativo GenAI per rispondere alle domande.   

All'interno troverai i seguenti file e cartelle:

- `Manuale di Cucina.pdf`
    
    Manuale di cucina che include:
    
    - L’elenco e la descrizione delle certificazione che uno chef può acquisire
    - L’elenco degli ordini professionali gastronomici a cui uno chef può aderire
    - L’elenco e la descrizione delle tecniche culinarie di preparazione esistenti
    - \[Hint\] La maggior parte del documento descrive nel dettaglio le tecniche disponibili. Ci sono circa 10 macrocategorie di tecniche culinarie dove ciascuna di esse comprende circa 5 tecniche. Alcuni utenti potrebbero richiedere piatti con una specifica macrocategoria di tecnica o una specifica tecnica.
    - \[Hint\] La maggior parte del testo è flavuor e non serve per rispondere alle domande.
    - \[Hint\] Gli ordini professionali sono perlopiù usati da alcuni utenti che esprimono una preferenza verso una specifica tecnica. Questa tecnica in genere è riportata nei menu attraverso l'uso di  emoji + glossario.

- `Menu (30 ristoranti)`
    
    - Documenti in pdf contenenti i menù di 30 ristoranti differenti
    - I menu descrivono in linguaggio naturale il ristorante, riportando il nome dello Chef, il nome del ristorante, (laddove presente) il pianeta su cui c'è il ristorante e le licenze culinarie che ha lo chef
    - Ogni menu contiene 10 piatti
    - Ogni piatto contiene gli ingredienti usati e le tecniche di preparazione
    - Alcuni menu possiedono anche una descrizione in linguaggio naturale della preparazione
    - Laddove via siano certi ordini professionali, i menu lo citano

- `planets_distance_matrix.csv`
    Un csv che contiene la matrice delle distanze in anni luce tra i pianeti su cui si trovano i diversi ristoranti.    
    \[Hint\] Alcune domande fanno riferimento a volere dei piatti all'interno di una certa distanza. Ogni ristorante (eccetto uno) si trova su un pianeta.

- `Codice Galattico.pdf`
    
    Un documento legislativo contenente:
    
    - Limiti quantitativi applicati all’utilizzo di alcuni ingredienti nella preparazione dei piatti
    - \[Hint\] Alcuni utenti potrebbero chiedere che il loro piatto rispetti tali limiti, pertanto è necessario controllare la presenza di tali ingredienti e fare una crossref sulla quantità
    - Vincoli relativi alle certificazioni che gli chef hanno bisogno di acquisire per poter utilizzare specifiche tecniche di preparazione dei piatti
    - \[Hint\] Alcuni utenti potrebbero chiedere che lo chef che prepara il piatto abbia le certificazioni a norma per cucinare tale piatto, pertanto è necessario controllare per ogni tecnica se lo chef ha la certificazione al livello corretto
    - \[Hint\] Questo documento, le informazioni da estrarre e da rielaborare, sono le più difficili del test tecnico e hanno impatto solo sulle ultime 4 domande del [csv](./dataset/domande.csv).

- `Blog post`

    - Pagine HTML che contengono informazioni supplementari su alcuni ristoranti
    - \[Hint\] Sono necessari solo per un numero limitatissimo di domande, da usare congiuntamente con il Codice Galattico.pdf


### Evaluation
Per aiutarvi nel test tecnico, dentro la cartella [dataset](./dataset/ground_truth) troverai il necessario per fare l'evaluation. Tuttavia la ground truth (almeno di considerazioni particolari) non va usata all'interno del sistema GenAI. Il dataset è già diviso in public / private nel caso vogliate fare validation/test dataset.

Per lanciare l'evaluation delle tua soluzione, vi consigliamo di usare il seguente comando:
```python
python src/evaluation.py --submission path/to/your_submission.csv
```