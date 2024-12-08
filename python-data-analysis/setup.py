from setuptools import setup, find_packages

setup(
    name="ai_survey_data",
    version="0.1",
    packages=find_packages(),  # Automatically find packages (e.g., modules/)
    install_requires=[
        "pandas",
        "matplotlib",
    ],
    include_package_data=True,
    description="A project for analyzing AI survey data.",
    author="Your Name",
    author_email="your_email@example.com",
    license="MIT",
)
