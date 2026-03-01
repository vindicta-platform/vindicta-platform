# CLI Reference

Command-line interface for the Vindicta Platform.

---

## Installation

```bash
uv pip install git+https://github.com/vindicta-platform/Vindicta-CLI.git
```

## Global Options

```bash
vindicta [OPTIONS] COMMAND
```

| Option | Description |
|--------|-------------|
| `--version` | Show version |
| `--help` | Show help |
| `--verbose` | Verbose output |

---

## Commands

### dice

Roll dice with CSPRNG.

```bash
vindicta dice roll 2d6
vindicta dice roll 3d6 --count 10
```

### warscribe

Work with WARScribe notation.

```bash
vindicta warscribe register --unit "Captain" --id "CPT-01"
vindicta warscribe action "[MOVE: CPT-01 -> Zone-A]"
vindicta warscribe transcript <match-id>
```

### match

Match management.

```bash
vindicta match new --player-list my.json --opponent-list opp.json
vindicta match score --turn 2 --primary 15
vindicta match end --winner player
vindicta match summary <match-id>
```

### oracle

AI predictions.

```bash
vindicta oracle predict --my-list my.json --opponent-list opp.json
vindicta oracle sleepers --faction "Tyranids"
```

### economy

Credit management.

```bash
vindicta economy balance
vindicta economy history --last 10
```
