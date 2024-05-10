# UCMA | Core

This repository encapsulates abstract classes and interfaces to simplify the process of plugin development. Use it to easily create a custom plugin.

**Install**

``` bash
poetry add git+https://github.com/Universal-code-metrics-analyzer/core.git@v0.1.0
```

## Git processor plugin

Subclass `core.git_processor.GitProcessor` and implement methods:
- `get_root_tree`
- `process_tree`
- `process_blob`
- [optional] `cleanup`

Expose entrypoint:

``` toml
[tool.poetry.plugins."ucma.git_processor.plugin"]
export = "path.to:Subclass"
```

Examples:

- [fs-git-processor](https://github.com/Universal-code-metrics-analyzer/fs-git-processor)
- [gitlab-git-processor](https://github.com/Universal-code-metrics-analyzer/gitlab-git-processor)

## Metrics calculator plugin

Subclass `core.metrics_calculator.MetricsCalculator` and implement methods:
- `calculate`

Expose entrypoint:

``` toml
[tool.poetry.plugins."ucma.metrics_calculator.plugin"]
export = "path.to:Subclass"
```

Examples:

- [mock-metrics-calculator](https://github.com/Universal-code-metrics-analyzer/mock-metrics-calculator)

## Report generator plugin

Subclass `core.report_generator.ReportGenerator` and implement methods:
- `generate`

Expose entrypoint:

``` toml
[tool.poetry.plugins."ucma.report_generator.plugin"]
export = "path.to:Subclass"
```

Examples:

- [json-report-generator](https://github.com/Universal-code-metrics-analyzer/json-report-generator)
