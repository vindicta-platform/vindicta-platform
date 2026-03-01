# Contributing to Vindicta Foundation

Thank you for your interest in contributing to the Vindicta Foundation! To ensure the integrity of the platform, stabilize our multi-agent workflows, and prevent concurrency conflicts, we enforce strict branching and contribution guidelines.

## 🌿 Branching Strategy & Contribution Flow

All development must adhere to **Trunk-Based Development** while enforcing strict namespace boundaries using a fork-based model.

### 1. Feature Development (Fork-Based)
All new features, architectural changes, or significant model additions **must** be developed on a personal fork of the repository.
1. **Fork the Repository**: Create a personal fork of `vindicta-platform/vindicta-foundation`.
2. **Branching**: Create a feature branch (e.g., `feat/my-new-model`) on your fork.
3. **Iterative Development**: Merge iterative changes and test them locally on your fork.
4. **Pull Request**: Open a Pull Request from your personal fork to the `main` branch of the upstream `vindicta-foundation` repository.

*This entirely eliminates cross-contamination and namespace clashing on the primary remote repository, especially when multiple autonomous agents are working concurrently.*

### 2. Chores & Bug Fixes (Direct Branching)
Maintainers and admins are permitted to push branches directly to the primary upstream repository for small chores, hotfixes, or localized documentation updates (e.g., `chore/dependency-update` or `fix/typo`).
- **Discouraged**: While allowed for speed, this bypasses the safety of the fork model and is strongly discouraged for anything beyond minor adjustments.

## 🤖 AI Agent Workflow Rules

If you are deploying an AI Agent (like Speckit or Quantum Leap) to generate code for this repository, you must ensure it complies with the following workspace rules:

1. **Strict Commit Isolation**: Agents must never globally stage files (`git add .`). They must only stage the explicit files they have scoped to prevent grabbing another developer's uncommitted work.
2. **Signed Commits**: All automated and manual commits must have verified SSH signatures.
3. **Main Branch Protection**: Commits directly to the `main` branch of the upstream repository are strictly prohibited. Agents must commit to a dedicated branch or fork and use our templated Pull Request pipelines.

## 📝 Pull Request Standards

All Pull Requests must use a properly formatted description file (no inline CLI bodies) containing the following sections:
- **Summary**: High-level overview.
- **Changes**: Specific bullet points on what was altered.
- **Why**: The root cause or business value.
- **Verification**: Proof of local testing.

For AI agents, utilize the built-in `.agent/workflows/pr.md` command to enforce this structure.
