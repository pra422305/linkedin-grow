import joblib


def load_metadata(artifact_path):
    artifact = joblib.load(artifact_path)
    return artifact.get("metadata", {})


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("artifact")
    args = parser.parse_args()
    print(load_metadata(args.artifact))
