from sklearn.base import RegressorMixin
from sklearn.utils.validation import check_array, check_X_y
import numpy as np


class DummyRegressorWithFracsum(RegressorMixin):
    """
    Dummy regressor that implements the "fracsum" strategy, which returns the sum of the fractional parts of the target
    variables in the training set.
    """

    def __init__(self):
        """
        Initialize the DummyRegressorWithFracsum.
        """
        self.constant_ = None

    def fit(self, X, y, sample_weight=None):
        """
        Fit the dummy regressor to the training data.

        Parameters:
            X : array-like of shape (n_samples, n_features)
                Training data.
            y : array-like of shape (n_samples,)
                Target values.
            sample_weight : array-like of shape (n_samples,), default=None
                Individual weights for each sample. If provided, it must have the same length as y.

        Returns:
            self : object
                Returns self.
        """
        X, y = check_X_y(X, y, y_numeric=True, multi_output=False)
        y = np.asarray(y)

        if len(y.shape) != 1:
            raise ValueError("Target variable y should be 1-dimensional.")

        if sample_weight is not None:
            sample_weight = np.asarray(sample_weight)
            if np.all(sample_weight == 0):
                raise ValueError("Invalid input: all samples have zero weight.")
            if np.any(sample_weight < 0):
                raise ValueError("Invalid input: sample_weight cannot contain negative weights.")

        if self.constant_ is None:
            self.constant_ = np.sum(np.modf(y)[0])  # Compute the sum of the fractional parts of y

        return self

    def predict(self, X):
        """
        Predict using the dummy regressor.

        Parameters:
            X : array-like of shape (n_samples, n_features)
                Samples.

        Returns:
            y : ndarray of shape (n_samples,)
                Returns an array of constant predictions.
        """
        X = check_array(X)

        if self.constant_ is None:
            raise ValueError("This DummyRegressor instance is not fitted yet.")

        n_samples = X.shape[0]
        return np.full(n_samples, self.constant_)

# Unit tests
def test_dummy_regressor_with_fracsum():
    X = [[1], [2], [3]]  # Features
    Y1 = [0.5, 1.3, -0.8]  # Target values for example a1
    Y2 = [5, 3, -8]  # Target values for example a2

    # Create DummyRegressorWithFracsum instance
    dummy_model = DummyRegressorWithFracsum()

    # Fit the model on the first example
    dummy_model.fit(X, Y1)

    # Predict using the trained model
    prediction1 = dummy_model.predict(X)
    assert np.allclose(prediction1, [0.0, 0.0, 0.0])

    # Fit the model on the second example
    dummy_model.fit(X, Y2)

    # Predict using the trained model
    prediction2 = dummy_model.predict(X)
    assert np.allclose(prediction2, [0.0, 0.0, 0.0])

    print("All tests pass.")


# Run the unit tests
test_dummy_regressor_with_fracsum()