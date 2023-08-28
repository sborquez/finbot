# Cloud Pub/Sub

Setup for the cloud infrastructure.

## Quick start

1. Define the variables in the `settings.sh` file.
2. Run `build.sh`

## Variables

## Scripts

These scripts are used to setup the cloud infrastructure.

```bash
.

├── build_steps/        # Steps used by the build script
│   ├── 01_setup.sh     # Create the project and enable the APIs
│   ├── 02_pubsub.sh    # Create the Pub/Sub topic and subscription
├── build.sh        # Build the cloud infrastructure
├── destroy.sh      # Destroy the cloud infrastructure
├── settings.sh    # Variables used by the build and destroy scripts
└── README.md       # This file
```

