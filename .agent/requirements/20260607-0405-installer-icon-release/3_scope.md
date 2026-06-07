# Scope

In scope:
- Add a Windows installer build path.
- Use the existing `assets/generated/app-icons/onoko-arcana-app-icon-v1.ico` as the executable, installer, and shortcut icon.
- Keep the local zip as a fallback artifact if useful.
- Add validation that the installer artifact exists and release hashes are generated.
- Update release docs so users download the installer first.

Out of scope:
- Paid or store distribution.
- Microsoft Store submission.
- Auto update rollout.
- Code signing without a certificate.
- Minor Arcana or runtime feature expansion.
