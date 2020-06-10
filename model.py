import numpy as np
import pandas as pd

from sklearn.ensemble import (RandomForestRegressor)

from sklearn.model_selection import (train_test_split)


pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',1000)

dataset = pd.read_csv('Data/Measurements-Transformed')

for coll in dataset.columns:
    coll = np.nan_to_num(coll)
pd.DataFrame(dataset).fillna(0, inplace=True)
np.where(np.isnan(dataset))

#drop rijen waar < n meting van zijn en houd van de overige de top n meest recente waardes
n = 2
dataset = dataset.groupby('ID').filter(lambda x: len(x) > (n-1))
dataset = dataset.groupby('ID').head(n)

#2 rijen naast elkaar zetten

dataset = dataset.merge(dataset ,on=['ID', 'Sex'], suffixes=['_x', ''])
dataset = dataset.sort_values(by=['ID', 'Measurement_Age_x'])
dataset = dataset.drop_duplicates(subset=['ID', 'Sex'], keep='first')
dataset.head()

#Drop kolom ID
dataset.drop(['ID'],axis=1, inplace=True)

##################################"
# Splitsen in features en targets

y = dataset['Sph-Far-R'].values
X = dataset.drop(['Add', 'Sph-Far-R', 'Cyl-Far-R', 'Axis-Far-R', 'Sph-Close-R', 'Cyl-Close-R', 'Axis-Close-R', 'Sph-Far-L',
                  'Cyl-Far-L', 'Axis-Far-L', 'Sph-Close-L', 'Cyl-Close-L', 'Axis-Close-L'],axis=1)

# Splitsen in training set en test set

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

#random forest regressor
number_of_trees = 200
max_number_of_depth = 10
max_number_of_features = 6

RFR_model_sph_far_r = RandomForestRegressor(n_estimators=number_of_trees, max_features=max_number_of_features, max_depth=max_number_of_depth)
RFR_model_sph_far_r.fit(X_train,y_train)

RFR_model_sph_far_r.score(X_test,y_test)

#################################"
# Splitsen in features en targets

y = dataset['Cyl-Far-R'].values
X = dataset.drop(['Add', 'Sph-Far-R', 'Cyl-Far-R', 'Axis-Far-R', 'Sph-Close-R', 'Cyl-Close-R', 'Axis-Close-R', 'Sph-Far-L',
                  'Cyl-Far-L', 'Axis-Far-L', 'Sph-Close-L', 'Cyl-Close-L', 'Axis-Close-L'],axis=1)

# Splitsen in training set en test set

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)


#random forest regressor
number_of_trees = 200
max_number_of_depth = 10
max_number_of_features = 6

RFR_model_cyl_far_r = RandomForestRegressor(n_estimators=number_of_trees, max_features=max_number_of_features, max_depth=max_number_of_depth)
RFR_model_cyl_far_r.fit(X_train,y_train)

RFR_model_cyl_far_r.score(X_test,y_test)


###################################
# Splitsen in features en targets

y = dataset['Sph-Far-L'].values
X = dataset.drop(['Add', 'Sph-Far-R', 'Cyl-Far-R', 'Axis-Far-R', 'Sph-Close-R', 'Cyl-Close-R', 'Axis-Close-R', 'Sph-Far-L',
                  'Cyl-Far-L', 'Axis-Far-L', 'Sph-Close-L', 'Cyl-Close-L', 'Axis-Close-L'],axis=1)

# Splitsen in training set en test set

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)


#random forest regressor
number_of_trees = 200
max_number_of_depth = 20
max_number_of_features = 6

RFR_model_sph_far_l = RandomForestRegressor(n_estimators=number_of_trees, max_features=max_number_of_features, max_depth=max_number_of_depth)
RFR_model_sph_far_l.fit(X_train,y_train)

RFR_model_sph_far_l.score(X_test,y_test)


####################################
# Splitsen in features en targets

y = dataset['Cyl-Far-L'].values
X = dataset.drop(['Add', 'Sph-Far-R', 'Cyl-Far-R', 'Axis-Far-R', 'Sph-Close-R', 'Cyl-Close-R', 'Axis-Close-R', 'Sph-Far-L',
                  'Cyl-Far-L', 'Axis-Far-L', 'Sph-Close-L', 'Cyl-Close-L', 'Axis-Close-L'],axis=1)

# Splitsen in training set en test set

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)


#random forest regressor
number_of_trees = 200
max_number_of_depth = 10
max_number_of_features = 6

RFR_model_cyl_far_l = RandomForestRegressor(n_estimators=number_of_trees, max_features=max_number_of_features, max_depth=max_number_of_depth)
RFR_model_cyl_far_l.fit(X_train,y_train)

RFR_model_cyl_far_l.score(X_test,y_test)




def get_forecast(user, years=15):
    result = {}
    targets = ["Sfr ver R","Cyl ver R","Sfr ver L", "Cyl ver L"]
    n = 0

    models = [RFR_model_sph_far_r, RFR_model_cyl_far_r, RFR_model_sph_far_l, RFR_model_cyl_far_l]
    for model in models:
        values = user
        age = values.iat[0, 1]
        pred = []
        ages = []
        values = values.assign(Measurement_Age_x=[age])

        for x in range(0, years):
            values['Measurement_Age_x'] = values['Measurement_Age_x'].add(365)
            age2 = values.iat[0, -1]
            x = model.predict(values)
            ages.append(age2)
            pred.append(x[0])

        ages = [x / 365 for x in ages]
        ages = [x.round() for x in ages]
        dictionary = dict(zip(ages, pred))
        result[targets[n]] = dictionary
        n += 1

    return result