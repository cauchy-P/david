"""Train and evaluate a simple KNN classifier on the Iris dataset."""

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


def main() -> None:
    iris = load_iris()
    X, y = iris.data, iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    for name, array in (
        ("X_train", X_train),
        ("X_test", X_test),
        ("y_train", y_train),
        ("y_test", y_test),
    ):
        print(f"{name} shape: {array.shape}, size: {array.size}")

    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X_train, y_train)

    sample = [[5, 2.9, 1, 0.2]]
    prediction = knn.predict(sample)
    print(f"\nPrediction for {sample}: {prediction} ({iris.target_names[prediction][0]})")


if __name__ == "__main__":
    main()
