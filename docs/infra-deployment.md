# Infrastructure and Deployment Overview

> This document is a granulated shard from the main "Sourcer MVP Architecture Document" focusing on "Infrastructure and Deployment Overview".

  - **Cloud Provider(s):** Not applicable for MVP core functionality (local processing). GitHub for code hosting and releases. [cite: 170]
  - **Core Services Used:** N/A for runtime. GitHub Releases for distributing the installer.
  - **Infrastructure as Code (IaC):** N/A. [cite: 171]
  - **Deployment Strategy:** [cite: 171]
      - Installer (`.exe`) built using `PyInstaller` and `Inno Setup`.
      - Distribution via GitHub Releases. [cite: 172]
      - CI/CD using GitHub Actions: [cite: 172]
          - On push/PR to `main`: Run linters, type checkers, unit tests.
          - On tag (e.g., `v0.1.0`): Build application with `PyInstaller`, create installer with `Inno Setup`, create GitHub Release, and upload installer.
  - **Environments:** [cite: 174]
      - `Development`: Local developer machines.
      - `Release`: Packaged installer distributed to users. [cite: 175]
  - **Environment Promotion:** N/A in the traditional sense. Promotion is from a successful `main` branch build to a tagged release.
  - **Rollback Strategy:** Users would need to uninstall the newer version and reinstall a previous version downloaded from GitHub Releases.