import pandas as pd

def prep_json(json):
    dataset = pd.DataFrame.from_dict(json, orient='index').T
    dataset.fillna(0)
    dataset = dataset.replace("", 0)
    dictSfr = {}
    dictCyl = {}
    dictAs = {}
    dictSfrDicht = {}
    dictCylDicht = {}
    dictAsDicht = {}
    dictSfr1 = {}
    dictCyl1 = {}
    dictAs1 = {}
    dictSfr1Dicht = {}
    dictCyl1Dicht = {}
    dictAs1Dicht = {}

    for index, row in dataset.iterrows():
        if row['Oogmetingen/Cyl ver'] < 0:
            sfr = row['Oogmetingen/Sfr ver'] + row['Oogmetingen/Cyl ver']
            cyl = row['Oogmetingen/Cyl ver'] - 2 * row['Oogmetingen/Cyl ver']
            key = index
            dictSfr[key] = sfr
            dictCyl[key] = cyl
            if row['Oogmetingen/As ver'] <= 90:
                dictAs[key] = row['Oogmetingen/As ver'] + 90
            elif row['Oogmetingen/As ver'] > 90:
                dictAs[key] = row['Oogmetingen/As ver'] - 90
        if row['Oogmetingen/Cyl dicht'] < 0:
            sfrDicht = row['Oogmetingen/Sfr dicht'] + row['Oogmetingen/Cyl dicht']
            cylDicht = row['Oogmetingen/Cyl dicht'] - 2 * row['Oogmetingen/Cyl dicht']
            key = index
            dictSfrDicht[key] = sfrDicht
            dictCylDicht[key] = cylDicht
            if row['Oogmetingen/As dicht'] <= 90:
                dictAsDicht[key] = row['Oogmetingen/As dicht'] + 90
            elif row['Oogmetingen/As dicht'] > 90:
                dictAsDicht[key] = row['Oogmetingen/As dicht'] - 90
        if row['Oogmetingen/Cyl ver/L'] < 0:
            sfr1 = row['Oogmetingen/Sfr ver/L'] + row['Oogmetingen/Cyl ver/L']
            cyl1 = row['Oogmetingen/Cyl ver/L'] - 2 * row['Oogmetingen/Cyl ver/L']
            key = index
            dictSfr1[key] = sfr1
            dictCyl1[key] = cyl1
            if row['Oogmetingen/As ver/L'] <= 90:
                dictAs1[key] = row['Oogmetingen/As ver/L'] + 90
            elif row['Oogmetingen/As ver/L'] > 90:
                dictAs1[key] = row['Oogmetingen/As ver/L'] - 90
        if row['Oogmetingen/Cyl dicht/L'] < 0:
            sfr1Dicht = row['Oogmetingen/Sfr dicht/L'] + row['Oogmetingen/Cyl dicht/L']
            cyl1Dicht = row['Oogmetingen/Cyl dicht/L'] - 2 * row['Oogmetingen/Cyl dicht/L']
            key = index
            dictSfr1Dicht[key] = sfr1Dicht
            dictCyl1Dicht[key] = cyl1Dicht
            if row['Oogmetingen/As dicht/L'] <= 90:
                dictAs1Dicht[key] = row['Oogmetingen/As dicht/L'] + 90
            elif row['Oogmetingen/As dicht/L'] > 90:
                dictAs1Dicht[key] = row['Oogmetingen/As dicht/L'] - 90

    dataset['Oogmetingen/Sfr ver'].update(pd.Series(dictSfr))
    dataset['Oogmetingen/Cyl ver'].update(pd.Series(dictCyl))
    dataset['Oogmetingen/As ver'].update(pd.Series(dictAs))
    dataset['Oogmetingen/Sfr dicht'].update(pd.Series(dictSfrDicht))
    dataset['Oogmetingen/Cyl dicht'].update(pd.Series(dictCylDicht))
    dataset['Oogmetingen/As dicht'].update(pd.Series(dictAsDicht))
    dataset['Oogmetingen/Sfr ver/L'].update(pd.Series(dictSfr1))
    dataset['Oogmetingen/Cyl ver/L'].update(pd.Series(dictCyl1))
    dataset['Oogmetingen/As ver/L'].update(pd.Series(dictAs1))
    dataset['Oogmetingen/Sfr dicht/L'].update(pd.Series(dictSfr1Dicht))
    dataset['Oogmetingen/Cyl dicht/L'].update(pd.Series(dictCyl1Dicht))
    dataset['Oogmetingen/As dicht/L'].update(pd.Series(dictAs1Dicht))

    dataset[['Geslacht']] = dataset[['Geslacht']].replace({'Vrouw': 0, 'Man': 1, 'Overige': 0, 0: 0})

    # zet de datums om naar datetime, n/a de out of bounds waarden en versnel het proces door het originele formaat te gebruiken
    dataset[['Geboortedatum']] = pd.to_datetime(dataset['Geboortedatum'], errors='coerce', infer_datetime_format=True)
    dataset[['Oogmetingen/Datum']] = pd.to_datetime(dataset['Oogmetingen/Datum'], errors='coerce',
                                                    infer_datetime_format=True)

    # Bereken leeftijd op moment van meting voor makkelijkere correlatie
    dataset["Measurement_Age"] = (dataset["Oogmetingen/Datum"] - dataset["Geboortedatum"]).astype("<m8[D]")

    # verwijder deze kolommen want we hebben ze niet meer nodig
    dataset = dataset.drop(columns=['Geboortedatum', 'Oogmetingen/Datum'])

    dataset.columns = ['Sex', 'Sph-Far-R', 'Cyl-Far-R', 'Axis-Far-R', 'Add-R', 'Sph-Close-R', 'Cyl-Close-R',
                       'Axis-Close-R', 'Sph-Far-L', 'Cyl-Far-L', 'Axis-Far-L', 'Add-L', 'Sph-Close-L', 'Cyl-Close-L',
                       'Axis-Close-L', 'Measurement_Age']
    dataset['Add'] = dataset['Add-R']
    dataset = dataset[
        ['Sex', 'Measurement_Age', 'Add', 'Sph-Far-R', 'Cyl-Far-R', 'Axis-Far-R', 'Sph-Close-R', 'Cyl-Close-R',
         'Axis-Close-R', 'Sph-Far-L', 'Cyl-Far-L', 'Axis-Far-L', 'Sph-Close-L', 'Cyl-Close-L', 'Axis-Close-L']]

    return dataset #.to_json(orient='index')