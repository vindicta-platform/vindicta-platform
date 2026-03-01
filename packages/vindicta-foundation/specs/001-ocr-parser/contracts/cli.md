# CLI Contract: parse-warscribe

The OCR Parser provides a CLI entrypoint for parsing Warscribe game results.

## Command Signature

```bash
parse-warscribe IMAGE_PATH [OPTIONS]
```

## Arguments

| Argument     | Type | Required | Description                                                  |
| ------------ | ---- | -------- | ------------------------------------------------------------ |
| `IMAGE_PATH` | path | Yes      | Path to the local screenshot image file (e.g. `sample.jpg`). |

## Options

| Option           | Type | Default | Description                                                                |
| ---------------- | ---- | ------- | -------------------------------------------------------------------------- |
| `--output`, `-o` | path | None    | Output file path for the JSON. Defaults to `stdout`.                       |
| `--pretty`       | flag | False   | Pretty-print the output JSON (indent=2).                                   |
| `--confidence`   | int  | 40      | Minimum OCR confidence threshold (0-100).                                  |
| `--dump-lines`   | flag | False   | Dump raw extracted OCR text lines (for debugging) instead of parsing JSON. |

## Exit Codes

- `0`: Success
- `1`: File not found or unreadable image
- `2`: Invalid CLI arguments

## I/O Contract

**Standard Output (`stdout`)**:
- By default, emits the minimized JSON representation of the `GameResult` model.
- If `--pretty` is passed, emits formatted JSON.
- If `--dump-lines` is passed, emits numbered text lines (`001: Text...`).

**Standard Error (`stderr`)**:
- Emits progress logs (e.g., `Processing: path/to/image.jpg`).
- Emits success markers if written to file (e.g., `Written to result.json`).
- CLI usage errors (from `click`).
