================
fancy_decorators


.. image:: https://img.shields.io/pypi/v/fancy_decorators.svg
        :target: https://pypi.python.org/pypi/fancy_decorators

.. image:: https://img.shields.io/travis/aadi350/fancy_decorators.svg
        :target: https://travis-ci.com/aadi350/fancy_decorators

.. image:: https://readthedocs.org/projects/fancy-decorators/badge/?version=latest
        :target: https://fancy-decorators.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Contains helpful decorators for common data-science tasks


* Free software: MIT license
* Documentation: https://fancy-decorators.readthedocs.io.


Logging Metrics
-----------------


This decorator allows ease-of-automation in typical grid-search tasks

The general pattern of usage is as follows

.. code:: python

        from fancy_decorators import log_metrics
        # Step I: Define a configuration for parameter search, note the keys in this dictionary must match the name of the parameter in your evaluate function 
        conf = # a dictionary of parameter values

        # Step II: Create your pandas dataframe for storing results
        midx = MultiIndex.from_product(conf.values(), names=conf.keys()
        metrics = DataFrame(index=midx)

        # Step III: Build your function which takes in a single parameter value and returns a dictionary
        @log_metrics(conf=conf, metrics=metrics)
        def foo(X_train, y_train, some_parameter):
        # do something that uses the parameter
        # calculate a metric
        return {'metric_name': metric_value}


Use-Case: Single-Parameter
````````````````````````````````````

This example shows a single-dimensional search for a support-vector classification model. In this example, we wish to search for the optimal regularization parameter using `sklearn` `SVC`. (It is assumed that `X_train, X_test, y_train, y_test` are already initialized and have data).

.. code:: python

        from fancy_decorators import log_metrics

        import numpy as np
        from pandas import DataFrame, MultiIndex
        from sklearn.svm import SVC
        from sklearn import metrics

        # Step I: Define a dictionary of parameters
        conf = {
                'C': [0.3, 0.5, 0.7]
        }

        # Step II: Create a pandas dataframe for storing results
        metrics_df = DataFrame(index=MultiIndex.from_product(conf.values(), names=conf.keys()))

        # Step III: Define your function and decorate
        @log_metrics(conf, metrics_df)
        def evaluate(X_train, y_train, X_test, y_test, C):
                clf = SVC(C=C)
                fit = clf.fit(X_train, y_train)

                y_pred = fit.predict(X_test)

                metric_accuracy = metrics.accuracy_score(y_test, y_pred)

                return {
                        'accuracy': metric_accuracy # returing a dictionary is ABSOLUTELY necessary!
                }

After the above is initialized, calling `evaluate(X_train, y_train, X_test, y_test)`, wihout specifying any value for `C` results in the following being stored in metrics: 

.. code::

        accuracy
        C	
        0.3	0.7375
        0.5	0.7375
        0.7	0.7375


Use-Case: Multi-Parameter
`````````````````````````````````

Extrapolating from the above, the pattern is similar:

.. code-block:: python

        from fancy_decorators import log_metrics

        import numpy as np
        from pandas import DataFrame, MultiIndex
        from sklearn.svm import SVC
        from sklearn import metrics

        # Step I: Define a dictionary of parameters
        # ensure that the names of the keys align with your function kwargs
        conf = {
        'C': [0.3, 0.5, 0.7],
        'degree': [1, 3, 10]
        }

        # Step II: Create a pandas dataframe for storing results
        metrics_df = DataFrame(index=MultiIndex.from_product(conf.values(), names=conf.keys()))

        # Step III: Define your function and decorate
        @log_metrics(conf, metrics_df)
        def evaluate(X_train, y_train, X_test, y_test, C, degree):
                clf = SVC(C=C, degree)
                fit = clf.fit(X_train, y_train)  
                y_pred = fit.predict(X_test)  
                metric_accuracy = metrics.accuracy_score(y_test, y_pred)  
                return {'accuracy': metric_accuracy }

Calling the above results in the following being stored in `metrics_df`:

.. code::

                accuracy
        C	degree	
        0.3	1	0.7375
        3	0.7375
        10	0.7375
        0.5	1	0.7375
        3	0.7375

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
