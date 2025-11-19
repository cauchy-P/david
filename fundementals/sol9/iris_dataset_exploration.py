"""Explore the Iris dataset using scikit-learn.

This script prints the metadata (description, target names, feature names) and
examines the structure of both the feature matrix and the target vector.
"""

from sklearn import datasets


def describe_array(name: str, array) -> None:
    """Print basic information about a NumPy array."""
    print(f"\n{name} information")
    print("-" * 40)
    print(f"Shape: {array.shape}")
    print(f"Dimensions (ndim): {array.ndim}")
    print(f"Data type: {array.dtype}")
    print(f"First five entries:\n{array[:5]}")


def main() -> None:
    iris = datasets.load_iris()

    print("===== Iris Dataset Description =====")
    print(iris["DESCR"])

    print("\n===== Target Names =====")
    print(iris["target_names"])

    print("\n===== Feature Names =====")
    print(iris["feature_names"])

    describe_array("Feature data", iris["data"])
    describe_array("Target data", iris["target"])


if __name__ == "__main__":
    main()
