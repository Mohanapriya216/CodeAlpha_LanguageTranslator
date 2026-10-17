
import argostranslate.package as package

print("Updating Argos Translate model list...")
package.update_package_index()

available_packages = package.get_available_packages()

targets = ["ar", "zh", "fr", "de", "hi", "it", "ja", "ko", "es"]

for target in targets:
    model = next(
        (
            item
            for item in available_packages
            if item.from_code == "en" and item.to_code == target
        ),
        None,
    )

    if model is None:
        print(f"Model unavailable: English -> {target}")
        continue

    print(f"\nDownloading English -> {target}...")
    try:
        package.install_from_path(model.download())
        print(f"Installed English -> {target} successfully!")
    except Exception as error:
        print(f"Could not install English -> {target}: {error}")

print("\nModel installation process finished.")
