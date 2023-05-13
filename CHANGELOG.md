# Changelog

## 0.4.0

    * Introduce pipelines
        * Export pipelines to json
        * Load pipelines and rerun for different inputs
    * Add capability to define a custom function as a genie

## 0.3.1

    * Make the return type a basemodel with multiple attributes instead of the result directly
    * Accept a single base input during init instead of a dictionary
    * Add support for copying the input before running executor so that the input is not modified
    * Fix bug where code will throw an error is a cached file is removed by the user
    * Update starter notebook with kaggle data science salaries example

## 0.3.0

  * BREAKING CHANGE: modify the api to have a single genie initialization with invocations using that object
  * remove set_cache_dir method and make this a part of genie initialization

## 0.2.1

  * Fixed bug where genie would not work if the output is not cached

## 0.2.0

  * Added support for caching genie outputs across notebook sessions

## 0.1.0

  * Initial release
  * Launched Genie and PandasGenie capabilities
