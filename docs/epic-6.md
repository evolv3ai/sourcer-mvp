# Epic 6: MVP Packaging and Documentation

> This document is a granulated shard from the main "Sourcer Product Requirements Document (PRD)" focusing on "Epic 6: MVP Packaging and Documentation".

- **Goal:** Package the application for user installation and provide basic usage documentation.
- **Story 10: As an AI Early Adopter, I want a simple way to install Sourcer on my Windows machine so that I can start using it quickly.**
    - Acceptance Criteria:
        - An installer package (e.g., MSI, EXE) or a well-documented manual setup process (e.g., using pip with a requirements file within a Python environment) is provided for Windows.
        - The installation process includes all necessary local AI model dependencies.
        - Post-installation, the application is launchable via a shortcut or command.
        - Notes for Architect/Scrum Master: This is a significant risk area. Simplicity is key for MVP. Investigate tools like PyInstaller or similar, or a very clear script-based setup.
- **Story 11: As an AI Early Adopter, I want basic instructions on how to use Sourcer's MVP features so that I can understand its capabilities.**
    - Acceptance Criteria:
        - A README file or simple help guide is included.
        - Instructions cover installation, launching, initiating voice/text queries, and understanding the output.
        - Lists the 10-15 common objects the MVP is trained to recognize. [cite: 553]
        - Notes any known limitations of the MVP. [cite: 553]