# Sensoring Protobuff

Protocol Buffers (Protobuf) definitions for cross-platform data transmission with serialized structured data.

## How to use

You should add this repository as a submodule of your project with a specific tag and then import the corresponding language version.

## Updating this repository

Before tagging a new version, updating all the compiled versions with this script is necessary.

```bash
./compile.sh
```

It requires `python3` and `protoc`.

## Protocol Buffers Defined

* `Transaction`: Represents a transaction
