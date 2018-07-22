# Anonymization of French legal cases

[![Build Status](https://travis-ci.com/ELS-RD/anonymisation.svg?token=9BHyni1rDpKLxVsHDRNp&branch=master)](https://travis-ci.com/ELS-RD/anonymisation)

The purpose of this projet is to apply Named Entity Recognition to extract specific information from legal cases like 
names, addresses, etc.  
These information will be used by anonymization system.  

## Scope

The only legal cases massively acquired by ELS not anonymized are those from appeal Courts.  
The database is called **Jurica**.  
The input are XML files from **Jurica** generated by Temis covering the period 2008-2018.

The project is focused on finding mentions of entities and guessing their types.  
It doesn't manage pseudo-anonymization (replacing entities text by initials), deciding what to hide, etc.  

In the future, this project will be put in production.  
Deployment is not covered by this project.  
However, technical constrains (ex.: memory foot print, avoiding costly hardware) are already taken into account. 

## Challenge

Many SOTA algorithms are available as open source project.  
Therefore, developping a NER algorithm is not in the scope.

The main focus of this work is to generate a large high quality training set, by:

- leveraging the extractions from Temis
- using some easy to describe patterns (by regex)
- looking for other occurrences of entities discovered with other strategies
- create some variation of the discovered entities and search for them (remove first or last name, change the case, etc.)
- extending any discovered patterns to the neighbor words
- building dictionaries of names and look for them

## Type of tokens recognized

- `PARTIE_PP`: natural person (include first name unlike Temis)
- `PARTIE_PM`: organization (not done by Temis)
- `AVOCAT`: lawyers (not done by Temis)
- `MAGISTRAT`: judges (not done by Temis)
- `GREFFIER`: court clerks (not done by Temis)
- `ADRESSE`: addresses (very badly done by Temis)

To add in the future:

- phone numbers
- social security numbers
- credit card number
- RG

All the types to add may be managed by some simple regexes.

## Algorithm

Main NER algorithm is from [Spacy](https://spacy.io/) library and is best described in this [video](https://www.youtube.com/watch?v=sqDHBH9IjRU).
  
Basically it is a **CNN + HashingTrick / Bloom filter + L2S** approach over it.  
The L2S part is very similar to classical dependency parser algorithm (stack + actions).

Advantages:
- few feature extraction (suffix and prefix, 3 letters each, and the word shape, all done by Spacy)
- quite rapid on CPU
- low memory foot print (for possible [Lambda deployment](https://github.com/ryfeus/lambda-packs))
- very few dependencies

Project is done in Python and can't be rewritten in something else because Spacy only exists in Python.

Other approaches (LSTM, etc.) may have shown slightly better performance but are much slower to train and during inference.  
For these reasons, and the specific need to run it over a GPU (costly option), they are not in our scope.

## Resources

Very few resources are used outside the cases:

- a dictionary of first names ([open data](https://opendata.paris.fr/explore/dataset/liste_des_prenoms_2004_a_2012/?disjunctive.annee&disjunctive.prenoms))
- a dictionary of postal code and cities of France ([open data](https://www.data.gouv.fr/fr/datasets/base-officielle-des-codes-postaux/))

Both resources are stored on the Git repository (`resources/` folder).  
Both are not strategic to the success of the learning but gives a little help.

## Commands

* To learn

```python
python3 train.py
```

* To view results on a local web page ([`http://localhost:5000`](http://localhost:5000))

```python
python3 entities_viewer.py
```

* To view differences with Temis (only on shared types)

```python
python3 display_errors.py
```

All the project configuration is done through `resources/config.ini` file (mainly paths to some files).

### TODO:

- Nom du tribunal + chambre // Date de l'arrêt // RG
- implement prediction with multi thread (pipe) V2.1 ? https://github.com/explosion/spaCy/issues/1530
- search for phone number, social security number, etc. 
- Add rapporteurs / experts (close to word rapport)
- date de naissance


Number of tags: 1773909
Warning: Unnamed vectors -- this won't allow multiple vectors models to be loaded. (Shape: (0, 0))
  0%|          | 0/145040.8 [00:00<?, ?it/s]
Iter 1
 10%|▉         | 14504/145040.8 [2:09:49<18:59:21,  1.91it/s]{'ner': 57.427544362485946}

Iter 2
 20%|██        | 29009/145040.8 [4:18:30<17:04:46,  1.89it/s]{'ner': 36.54777899100043}

Iter 3
 30%|███       | 43515/145040.8 [6:27:13<11:37:35,  2.43it/s]{'ner': 32.62351346588014}

Iter 4
 40%|████      | 58019/145040.8 [8:39:24<15:51:11,  1.52it/s]{'ner': 30.822936655417266}

Iter 5
 50%|█████     | 72525/145040.8 [10:52:50<9:14:25,  2.18it/s] {'ner': 29.70916408157069}

Iter 6
 60%|██████    | 87029/145040.8 [13:06:14<8:45:25,  1.84it/s]{'ner': 28.97088341355564}

Iter 7
 70%|███████   | 101534/145040.8 [15:19:42<6:31:44,  1.85it/s]{'ner': 28.445833063707028}

Iter 8
 80%|████████  | 116039/145040.8 [17:33:06<4:28:08,  1.80it/s]{'ner': 27.971498231318378}

Iter 9
 90%|█████████ | 130544/145040.8 [19:46:28<2:23:44,  1.68it/s]{'ner': 27.52150698761693}

--------------
Number of tags: 1775635
Warning: Unnamed vectors -- this won't allow multiple vectors models to be loaded. (Shape: (0, 0))

Iter 1
 50%|█████     | 14382/28763.26 [2:04:41<1:49:30,  2.19it/s]{'ner': 59.536253356406405}

Iter 2
100%|█████████▉| 28763/28763.26 [4:10:13<00:00,  1.89it/s]{'ner': 39.26536671542931}
28764it [4:10:13,  2.14it/s]        
-------------------
Number of tags: 1789948
Warning: Unnamed vectors -- this won't allow multiple vectors models to be loaded. (Shape: (0, 0))

Iter 1
 25%|██▍       | 14454/57816.04 [2:06:59<6:06:57,  1.97it/s]{'ner': 67.71795046884715}

Iter 2
 50%|█████     | 28909/57816.04 [4:13:19<4:05:11,  1.96it/s]{'ner': 46.69826582446979}

Iter 3
 75%|███████▌  | 43365/57816.04 [6:19:56<1:36:55,  2.49it/s]{'ner': 42.69678843677113}

Iter 4
57819it [8:29:44,  1.85it/s]{'ner': 40.70850695853477}
57820it [8:29:44,  2.42it/s]
----------------------
Number of tags: 1828754
Warning: Unnamed vectors -- this won't allow multiple vectors models to be loaded. (Shape: (0, 0))
  0%|          | 0/58912.84 [00:00<?, ?it/s]
Iter 1
 25%|██▍       | 14728/58912.84 [2:09:00<6:18:45,  1.94it/s]{'ner': 67.85554110441444}

Iter 2
 50%|█████     | 29458/58912.84 [4:21:36<3:27:16,  2.37it/s]{'ner': 46.97043271907819}

Iter 3
 75%|███████▌  | 44187/58912.84 [6:34:35<1:50:43,  2.22it/s]{'ner': 43.03420076370094}

Iter 4
58916it [8:51:00,  2.00it/s]
{'ner': 41.01037724554021}
-------
Number of tags: 1838488
Warning: Unnamed vectors -- this won't allow multiple vectors models to be loaded. (Shape: (0, 0))
  0%|          | 0/147282.1 [00:00<?, ?it/s]
Iter 1
 10%|▉         | 14728/147282.1 [2:08:14<18:56:38,  1.94it/s]{'ner': 66.24498462381916}

Iter 2
 20%|██        | 29458/147282.1 [4:17:05<14:30:56,  2.25it/s]{'ner': 45.65171872189785}

Iter 3
 30%|███       | 44187/147282.1 [6:26:10<12:32:49,  2.28it/s]{'ner': 41.7875151321731}

Iter 4
 40%|████      | 58915/147282.1 [8:38:55<13:11:23,  1.86it/s]{'ner': 39.87230896325718}

Iter 5
 50%|█████     | 73645/147282.1 [10:52:38<8:17:44,  2.47it/s] {'ner': 38.66143961688948}

Iter 6
 60%|██████    | 88373/147282.1 [13:06:16<8:45:27,  1.87it/s]{'ner': 37.84853459032075}

Iter 7
 70%|███████   | 103103/147282.1 [15:20:09<4:59:31,  2.46it/s]{'ner': 37.12548023300906}

Iter 8
 80%|████████  | 117832/147282.1 [17:33:47<3:32:43,  2.31it/s]{'ner': 36.63719058544939}

Iter 9
 90%|█████████ | 132560/147282.1 [19:47:40<2:16:39,  1.80it/s]{'ner': 36.07416604219725}

Iter 10
147289it [22:01:32,  1.91it/s]{'ner': 35.80839124857698}
147290it [22:01:32,  2.25it/s]
---------
Number of tags: 1838747
Warning: Unnamed vectors -- this won't allow multiple vectors models to be loaded. (Shape: (0, 0))
  0%|          | 0/58912.84 [00:00<?, ?it/s]
Iter 1
 25%|██▌       | 14729/58912.84 [2:07:57<5:11:57,  2.36it/s]{'ner': 67.09906184357169}

Iter 2
 50%|█████     | 29457/58912.84 [4:16:38<4:24:54,  1.85it/s]{'ner': 46.027869963762896}

Iter 3
 75%|███████▌  | 44187/58912.84 [6:25:35<1:47:29,  2.28it/s]{'ner': 42.25843731397822}

Iter 4
58915it [8:38:10,  1.88it/s]{'ner': 40.20154718467688}
58916it [8:38:10,  2.29it/s]
---------
Tiret dans les noms d avocats
 Me Carine Chevalier - Kasprzak ...
-------
Noms qui commencent par [de MAJ...]
retirer le de/le... a la fin des noms
--- 

rechercher marocaine dans les références Témis
-> la mention marocaine est parfois en majuscules...


Identifier les règles vides
