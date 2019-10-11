import numpy as np
import pandas as pd

from rdt import HyperTransformer


def get_input_data():
    data = pd.DataFrame({
        'integer': [1, 2, 1, 3, 1],
        'float': [0.1, 0.2, 0.1, np.nan, 0.1],
        'categorical': ['a', 'b', np.nan, 'b', 'a'],
        'bool': [False, np.nan, False, True, False],
        'datetime': [
            np.nan, '2010-02-01', '2010-01-01', '2010-02-01', '2010-01-01'
        ]
    })
    data['datetime'] = pd.to_datetime(data['datetime'])

    return data


def get_transformed_data():
    return pd.DataFrame({
        'integer': [1, 2, 1, 3, 1],
        'float': [0.1, 0.2, 0.1, 0.125, 0.1],
        'float#1': [0.0, 0.0, 0.0, 1.0, 0.0],
        'categorical': [0.6, 0.2, 0.9, 0.2, 0.6],
        'bool': [0.0, -1.0, 0.0, 1.0, 0.0],
        'bool#1': [0.0, 1.0, 0.0, 0.0, 0.0],
        'datetime': [
            1.2636432e+18, 1.2649824e+18, 1.262304e+18,
            1.2649824e+18, 1.262304e+18
        ],
        'datetime#1': [1.0, 0.0, 0.0, 0.0, 0.0]
    })


def get_transformers():
    return {
        'integer': {
            'class': 'NumericalTransformer',
            'kwargs': {
                'dtype': int,
            }
        },
        'float': {
            'class': 'NumericalTransformer',
            'kwargs': {
                'dtype': float,
            }
        },
        'categorical': {
            'class': 'CategoricalTransformer'
        },
        'bool': {
            'class': 'BooleanTransformer'
        },
        'datetime': {
            'class': 'DatetimeTransformer'
        },
    }


def test_hypertransformer_with_transformers():
    data = get_input_data()
    transformers = get_transformers()

    ht = HyperTransformer(transformers)
    ht.fit(data)
    transformed = ht.transform(data)

    expected = get_transformed_data()

    np.testing.assert_allclose(transformed.values, expected.values)

    reversed_data = ht.reverse_transform(transformed)

    pd.testing.assert_frame_equal(data, reversed_data)
